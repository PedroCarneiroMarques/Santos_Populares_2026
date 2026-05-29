import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import streamlit as st

from config import VOTES_DB


def _ensure_db(db_path: Path = VOTES_DB) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS votes (
                voter_id TEXT PRIMARY KEY,
                local TEXT NOT NULL,
                voted_at TEXT NOT NULL
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_votes_local ON votes(local)")


@contextmanager
def _connect(db_path: Path = VOTES_DB):
    _ensure_db(db_path)
    conn = sqlite3.connect(db_path)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def get_voter_id() -> str:
    if "voter_id" not in st.session_state:
        st.session_state.voter_id = str(uuid.uuid4())
    return st.session_state.voter_id


def cast_vote(local: str, voter_id: Optional[str] = None, db_path: Path = VOTES_DB) -> None:
    voter_id = voter_id or get_voter_id()
    now = datetime.now(timezone.utc).isoformat()
    with _connect(db_path) as conn:
        conn.execute(
            "INSERT INTO votes (voter_id, local, voted_at) VALUES (?, ?, ?) "
            "ON CONFLICT(voter_id) DO UPDATE SET local = excluded.local, voted_at = excluded.voted_at",
            (voter_id, local, now),
        )


def clear_vote(voter_id: Optional[str] = None, db_path: Path = VOTES_DB) -> None:
    voter_id = voter_id or get_voter_id()
    with _connect(db_path) as conn:
        conn.execute("DELETE FROM votes WHERE voter_id = ?", (voter_id,))


def get_user_vote(voter_id: Optional[str] = None, db_path: Path = VOTES_DB) -> Optional[str]:
    voter_id = voter_id or get_voter_id()
    _ensure_db(db_path)
    with _connect(db_path) as conn:
        row = conn.execute("SELECT local FROM votes WHERE voter_id = ?", (voter_id,)).fetchone()
    return row[0] if row else None


def get_vote_counts(db_path: Path = VOTES_DB) -> Dict[str, int]:
    _ensure_db(db_path)
    with _connect(db_path) as conn:
        rows = conn.execute(
            "SELECT local, COUNT(*) AS votes FROM votes GROUP BY local ORDER BY votes DESC, local ASC"
        ).fetchall()
    return {local: votes for local, votes in rows}


def get_vote_leaderboard(limit: int = 10, db_path: Path = VOTES_DB) -> pd.DataFrame:
    counts = get_vote_counts(db_path)
    if not counts:
        return pd.DataFrame(columns=["local", "votes"])
    df = pd.DataFrame([{"local": k, "votes": v} for k, v in counts.items()])
    return df.sort_values(["votes", "local"], ascending=[False, True]).head(limit).reset_index(drop=True)


def total_votes(db_path: Path = VOTES_DB) -> int:
    _ensure_db(db_path)
    with _connect(db_path) as conn:
        row = conn.execute("SELECT COUNT(*) FROM votes").fetchone()
    return int(row[0]) if row else 0
