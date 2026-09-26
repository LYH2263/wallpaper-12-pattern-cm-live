from fastapi import HTTPException

from app.modules.pattern_height import validate_pattern_cm
from app.repositories import rolls as rolls_repo


def update_pattern(roll_id: int, pattern_cm) -> dict:
    if not rolls_repo.get_roll(roll_id):
        raise HTTPException(404, "roll not found")
    try:
        cm = validate_pattern_cm(pattern_cm)
    except ValueError as e:
        raise HTTPException(422, str(e))
    return rolls_repo.update_pattern_cm(roll_id, cm)
