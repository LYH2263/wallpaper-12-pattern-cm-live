import math

import pytest

from app.modules.pattern_height import validate_pattern_cm


@pytest.mark.parametrize("value", [-1, -0.01, -100.0])
def test_negative_rejected(value):
    with pytest.raises(ValueError):
        validate_pattern_cm(value)


@pytest.mark.parametrize("value", [0, 0.0, 1, 30, 64.0, 30.5, "0", "64", "30.5"])
def test_zero_and_positive_accepted(value):
    out = validate_pattern_cm(value)
    assert out == float(value)
    assert isinstance(out, float)


@pytest.mark.parametrize("value", [None, "", "abc", object()])
def test_non_numeric_rejected(value):
    with pytest.raises(ValueError):
        validate_pattern_cm(value)


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf, float("nan")])
def test_non_finite_rejected(value):
    with pytest.raises(ValueError):
        validate_pattern_cm(value)


@pytest.mark.parametrize("value", [True, False])
def test_bool_rejected(value):
    with pytest.raises(ValueError):
        validate_pattern_cm(value)
