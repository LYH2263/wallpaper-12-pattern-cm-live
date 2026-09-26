from fastapi import HTTPException

from app.repositories import rolls as repo


def update_pattern(roll_id: int, pattern_cm: float) -> dict:
    if repo.update_pattern_cm(roll_id, pattern_cm) == 0:
        raise HTTPException(404, "roll not found")
    return repo.get_roll(roll_id)
