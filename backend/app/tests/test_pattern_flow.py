import pytest

from app import seed
from app.repositories import history, rolls
from app.services import roll_service
from app.services.estimate_service import run_estimate


@pytest.fixture
def db(monkeypatch, tmp_path):
    monkeypatch.setattr("app.db.DB_PATH", str(tmp_path / "t.db"))
    seed.init_db()
    return tmp_path


def test_update_pattern_cm_persists(db):
    assert rolls.update_pattern_cm(2, 0) == 1
    assert rolls.get_roll(2)["pattern_cm"] == 0
    assert rolls.update_pattern_cm(999, 10) == 0


def test_service_404_for_missing_roll(db):
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc:
        roll_service.update_pattern(999, 10)
    assert exc.value.status_code == 404


def test_get_run_missing_is_none(db):
    assert history.get_run(999) is None


def test_changing_pattern_does_not_rewrite_archived_runs(db):
    # wall 2 = 20m x 2.8m, roll 2 = 0.53 x 10m seeded with pattern_cm 64
    run_a = run_estimate(2, 2, save=True, note="A-64")
    snap_a = history.get_run(run_a["run_id"])["result"]
    assert snap_a["drop_len_m"] == 3.44
    assert snap_a["strips_per_roll"] == 2
    assert snap_a["rolls"] == 19
    assert snap_a["pattern_cm"] == 64

    # iterate the pattern height on the same roll, then re-measure the same wall
    roll_service.update_pattern(2, 0)
    live = run_estimate(2, 2, save=False, note="")
    assert live["drop_len_m"] == 2.8
    assert live["strips_per_roll"] == 3
    assert live["rolls"] == 13
    run_b = run_estimate(2, 2, save=True, note="B-0")
    snap_b = history.get_run(run_b["run_id"])["result"]

    # the older order stays pinned to the values written at its time
    pinned_a = history.get_run(run_a["run_id"])["result"]
    assert pinned_a["drop_len_m"] == 3.44
    assert pinned_a["strips_per_roll"] == 2
    assert pinned_a["rolls"] == 19
    assert pinned_a["pattern_cm"] == 64
    assert snap_b["drop_len_m"] == 2.8
    assert snap_b["strips_per_roll"] == 3
    assert snap_b["rolls"] == 13
    assert snap_b["pattern_cm"] == 0
