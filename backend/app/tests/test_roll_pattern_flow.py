import pytest
from fastapi import HTTPException

from app import db, seed
from app.repositories import history, rolls
from app.services import estimate_service, history_service, roll_service


@pytest.fixture
def isolated_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    seed.init_db()
    return tmp_path


def test_update_persists(isolated_db):
    row = roll_service.update_pattern(2, 30.0)
    assert row["pattern_cm"] == 30.0
    assert rolls.get_roll(2)["pattern_cm"] == 30.0
    assert rolls.update_pattern_cm(999, 1.0) is None


def test_negative_rejected_with_422(isolated_db):
    with pytest.raises(HTTPException) as exc:
        roll_service.update_pattern(2, -5)
    assert exc.value.status_code == 422
    assert rolls.get_roll(2)["pattern_cm"] == 64


def test_missing_roll_404(isolated_db):
    with pytest.raises(HTTPException) as exc:
        roll_service.update_pattern(999, 1.0)
    assert exc.value.status_code == 404


def test_recompute_after_pattern_change(isolated_db):
    roll_service.update_pattern(2, 30)
    calc = estimate_service.run_estimate(2, 2, False, "")
    # 墙 20m x 2.8m，花高 30cm：条长 3.1，每卷 floor(10/3.1)=3，卷数 ceil(38/3)=13
    assert calc["drop_len_m"] == 3.1
    assert calc["strips_per_roll"] == 3
    assert calc["rolls"] == 13
    assert calc["roll"]["pattern_cm"] == 30.0


def test_history_pinned_after_later_change(isolated_db):
    roll_service.update_pattern(2, 64)
    saved = estimate_service.run_estimate(2, 2, True, "基线单")
    run_id = saved["run_id"]
    assert run_id is not None
    assert saved["drop_len_m"] == 3.44
    assert saved["strips_per_roll"] == 2
    assert saved["rolls"] == 19

    roll_service.update_pattern(2, 30)
    fresh = estimate_service.run_estimate(2, 2, False, "")
    assert (fresh["drop_len_m"], fresh["strips_per_roll"], fresh["rolls"]) == (3.1, 3, 13)

    pinned = history_service.get_run(run_id)["result"]
    assert pinned["drop_len_m"] == 3.44
    assert pinned["strips_per_roll"] == 2
    assert pinned["rolls"] == 19
    assert pinned["pattern_cm"] == 64
    assert pinned["pattern_m"] == 0.64


def test_missing_run_404(isolated_db):
    with pytest.raises(HTTPException) as exc:
        history_service.get_run(99999)
    assert exc.value.status_code == 404


def test_legacy_snapshot_without_pattern_cm(isolated_db):
    legacy = {"drops": 31, "drop_len_m": 2.7, "pattern_m": 0.0, "strips_per_roll": 3, "rolls": 11}
    run_id = history.insert_run(1, 1, legacy, "")
    assert history_service.get_run(run_id)["result"]["rolls"] == 11
    assert all("result" in r for r in history.list_runs())
