from fastapi import APIRouter, HTTPException
from app.repositories import rolls as repo
from app.schemas.roll import RollPatternUpdate
from app.services import roll_service

router = APIRouter()


@router.get("/rolls")
def list_rolls():
    return {"items": repo.list_rolls()}


@router.get("/rolls/{roll_id}")
def get_roll(roll_id: int):
    row = repo.get_roll(roll_id)
    if not row:
        raise HTTPException(404)
    return row


@router.patch("/rolls/{roll_id}/pattern")
def update_roll_pattern(roll_id: int, body: RollPatternUpdate):
    return roll_service.update_pattern(roll_id, body.pattern_cm)
