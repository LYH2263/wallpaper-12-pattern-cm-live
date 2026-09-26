from app.db import connect, get_conn


def list_rolls():
    conn = connect()
    try:
        return [dict(r) for r in conn.execute("SELECT * FROM rolls ORDER BY id").fetchall()]
    finally:
        conn.close()


def get_roll(rid: int):
    conn = connect()
    try:
        row = conn.execute("SELECT * FROM rolls WHERE id=?", (rid,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def update_pattern_cm(rid: int, pattern_cm: float) -> int:
    with get_conn() as conn:
        cur = conn.execute("UPDATE rolls SET pattern_cm=? WHERE id=?", (pattern_cm, rid))
        return cur.rowcount
