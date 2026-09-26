import math

import pytest
from pydantic import ValidationError

from app.engines.pattern import PatternHeightError, validate_pattern_cm
from app.engines.wallpaper_math import roll_count
from app.schemas.roll import RollPatternUpdate


def test_validate_accepts_zero_and_positive():
    assert validate_pattern_cm(0) == 0.0
    assert validate_pattern_cm("64") == 64.0


@pytest.mark.parametrize("bad", [-1, -0.01, float("nan"), float("inf"), float("-inf"), "abc", None])
def test_validate_rejects_bad_values(bad):
    with pytest.raises(PatternHeightError):
        validate_pattern_cm(bad)


def test_engine_rejects_negative_pattern_instead_of_clamping():
    with pytest.raises(PatternHeightError):
        roll_count(16.0, 2.7, 0.53, 10.0, -5)


def test_schema_rejects_negative():
    with pytest.raises(ValidationError):
        RollPatternUpdate(pattern_cm=-1)


def test_schema_accepts_zero():
    assert RollPatternUpdate(pattern_cm=0).pattern_cm == 0.0
    assert math.isfinite(RollPatternUpdate(pattern_cm=64).pattern_cm)
