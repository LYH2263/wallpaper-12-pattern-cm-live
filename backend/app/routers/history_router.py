from fastapi import APIRouter
from app.repositories import history as repo
from app.services import history_service

router = APIRouter()


@router.get("/runs")
def list_runs(limit: int = 50):
    return {"items": repo.list_runs(limit)}


@router.get("/runs/{run_id}")
def get_run(run_id: int):
    return history_service.get_run(run_id)
