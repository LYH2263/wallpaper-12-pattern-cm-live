"""Pattern height (repeat) validation: shared domain rule for the engine and API schemas."""

import math


class PatternHeightError(ValueError):
    """Raised when the pattern height is not a finite, non-negative number of centimetres."""


def validate_pattern_cm(value) -> float:
    try:
        v = float(value)
    except (TypeError, ValueError):
        raise PatternHeightError("pattern_cm must be a number")
    if not math.isfinite(v):
        raise PatternHeightError("pattern_cm must be finite")
    if v < 0:
        raise PatternHeightError("pattern_cm must be >= 0")
    return v
