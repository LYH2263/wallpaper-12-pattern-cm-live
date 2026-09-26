"""花高（pattern repeat height）领域校验。"""

import math


def validate_pattern_cm(value) -> float:
    """花高以厘米计，允许 0（素色）与正数，拒绝负数、NaN/无穷与非数值。"""
    if isinstance(value, bool):
        raise ValueError("pattern_cm must be a number")
    try:
        cm = float(value)
    except (TypeError, ValueError):
        raise ValueError("pattern_cm must be a number")
    if not math.isfinite(cm):
        raise ValueError("pattern_cm must be finite")
    if cm < 0:
        raise ValueError("pattern_cm must be >= 0")
    return cm
