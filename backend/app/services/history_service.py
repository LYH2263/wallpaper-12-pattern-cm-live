from fastapi import HTTPException

from app.repositories import history as history_repo


def get_run(run_id: int) -> dict:
    """按历史编号回看：返回写入当时冻结的结果，绝不重新测算。"""
    row = history_repo.get_run(run_id)
    if not row:
        raise HTTPException(404, "run not found")
    return row
