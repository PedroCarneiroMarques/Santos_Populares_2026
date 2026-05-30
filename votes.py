import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Union

import pandas as pd
import streamlit as st

from config import VOTES_DB

DateLike = Union[pd.Timestamp, str]


def _date_key(vote_date: DateLike) -> str:
    return pd.Timestamp(vote_date).strftime("%Y-%m-%d")


def today() -> pd.Timestamp:
    return pd.Timestamp.now().normalize()


def _ensure_db(db_path: Path = VOTES_DB) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        cols = {row[1] for row in conn.execute("PRAGMA table_info(votes)").fetchall()}
        if not cols:
            conn.execute(
                """
                CREATE TABLE votes (
                    voter_id TEXT NOT NULL,
                    vote_date TEXT NOT NULL,
                    local TEXT NOT NULL,
                    voted_at TEXT NOT NULL,
                    PRIMARY KEY (voter_id, vote_date)
                )
                """
            )
        elif "vote_date" not in cols:
            conn.execute(
                """
                CREATE TABLE votes_daily (
                    voter_id TEXT NOT NULL,
                    vote_date TEXT NOT NULL,
                    local TEXT NOT NULL,
                    voted_at TEXT NOT NULL,
                    PRIMARY KEY (voter_id, vote_date)
                )
                """
            )
            conn.execute("DROP TABLE votes")
            conn.execute("ALTER TABLE votes_daily RENAME TO votes")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_votes_date_local ON votes(vote_date, local)")


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


def cast_vote(
    local: str,
    vote_date: DateLike,
    voter_id: Optional[str] = None,
    db_path: Path = VOTES_DB,
) -> None:
    voter_id = voter_id or get_voter_id()
    day = _date_key(vote_date)
    now = datetime.now(timezone.utc).isoformat()
    with _connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO votes (voter_id, vote_date, local, voted_at) VALUES (?, ?, ?, ?)
            ON CONFLICT(voter_id, vote_date) DO UPDATE SET
                local = excluded.local,
                voted_at = excluded.voted_at
            """,
            (voter_id, day, local, now),
        )


def clear_vote(
    vote_date: DateLike,
    voter_id: Optional[str] = None,
    db_path: Path = VOTES_DB,
) -> None:
    voter_id = voter_id or get_voter_id()
    day = _date_key(vote_date)
    with _connect(db_path) as conn:
        conn.execute(
            "DELETE FROM votes WHERE voter_id = ? AND vote_date = ?",
            (voter_id, day),
        )


def get_user_vote(
    vote_date: DateLike,
    voter_id: Optional[str] = None,
    db_path: Path = VOTES_DB,
) -> Optional[str]:
    voter_id = voter_id or get_voter_id()
    day = _date_key(vote_date)
    with _connect(db_path) as conn:
        row = conn.execute(
            "SELECT local FROM votes WHERE voter_id = ? AND vote_date = ?",
            (voter_id, day),
        ).fetchone()
    return row[0] if row else None


def get_vote_counts(vote_date: DateLike, db_path: Path = VOTES_DB) -> Dict[str, int]:
    day = _date_key(vote_date)
    with _connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT local, COUNT(*) AS votes
            FROM votes
            WHERE vote_date = ?
            GROUP BY local
            ORDER BY votes DESC, local ASC
            """,
            (day,),
        ).fetchall()
    return {local: votes for local, votes in rows}


def get_vote_leaderboard(
    vote_date: DateLike,
    limit: int = 10,
    db_path: Path = VOTES_DB,
) -> pd.DataFrame:
    counts = get_vote_counts(vote_date, db_path)
    if not counts:
        return pd.DataFrame(columns=["local", "votes"])
    df = pd.DataFrame([{"local": k, "votes": v} for k, v in counts.items()])
    return df.sort_values(["votes", "local"], ascending=[False, True]).head(limit).reset_index(drop=True)


def total_votes(vote_date: DateLike, db_path: Path = VOTES_DB) -> int:
    day = _date_key(vote_date)
    with _connect(db_path) as conn:
        row = conn.execute(
            "SELECT COUNT(*) FROM votes WHERE vote_date = ?",
            (day,),
        ).fetchone()
    return int(row[0]) if row else 0
