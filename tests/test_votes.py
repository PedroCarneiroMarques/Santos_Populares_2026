"""Tests for the daily arraial voting system."""
from pathlib import Path

import pandas as pd
import pytest

from voting import (
    cast_vote,
    clear_vote,
    get_user_vote,
    get_vote_counts,
    get_vote_leaderboard,
    total_votes,
)

DAY_A = "2026-06-13"
DAY_B = "2026-06-14"


@pytest.fixture
def vote_db(tmp_path: Path) -> Path:
    return tmp_path / "votes.db"


def test_cast_and_count_votes_for_one_day(vote_db: Path):
    cast_vote("Arraial A", DAY_A, voter_id="user-1", db_path=vote_db)
    cast_vote("Arraial B", DAY_A, voter_id="user-2", db_path=vote_db)
    cast_vote("Arraial A", DAY_A, voter_id="user-3", db_path=vote_db)

    counts = get_vote_counts(DAY_A, vote_db)
    assert counts["Arraial A"] == 2
    assert counts["Arraial B"] == 1
    assert total_votes(DAY_A, vote_db) == 3


def test_votes_are_isolated_by_day(vote_db: Path):
    cast_vote("Arraial A", DAY_A, voter_id="user-1", db_path=vote_db)
    cast_vote("Arraial B", DAY_B, voter_id="user-1", db_path=vote_db)

    assert get_user_vote(DAY_A, "user-1", vote_db) == "Arraial A"
    assert get_user_vote(DAY_B, "user-1", vote_db) == "Arraial B"
    assert total_votes(DAY_A, vote_db) == 1
    assert total_votes(DAY_B, vote_db) == 1


def test_user_can_change_vote_same_day(vote_db: Path):
    cast_vote("Arraial A", DAY_A, voter_id="user-1", db_path=vote_db)
    cast_vote("Arraial C", DAY_A, voter_id="user-1", db_path=vote_db)

    assert get_user_vote(DAY_A, "user-1", vote_db) == "Arraial C"
    assert get_vote_counts(DAY_A, vote_db) == {"Arraial C": 1}
    assert total_votes(DAY_A, vote_db) == 1


def test_clear_vote_only_for_that_day(vote_db: Path):
    cast_vote("Arraial A", DAY_A, voter_id="user-1", db_path=vote_db)
    cast_vote("Arraial B", DAY_B, voter_id="user-1", db_path=vote_db)
    clear_vote(DAY_A, "user-1", vote_db)

    assert get_user_vote(DAY_A, "user-1", vote_db) is None
    assert get_user_vote(DAY_B, "user-1", vote_db) == "Arraial B"


def test_leaderboard_order(vote_db: Path):
    cast_vote("Arraial B", DAY_A, voter_id="u1", db_path=vote_db)
    cast_vote("Arraial A", DAY_A, voter_id="u2", db_path=vote_db)
    cast_vote("Arraial A", DAY_A, voter_id="u3", db_path=vote_db)

    board = get_vote_leaderboard(DAY_A, 5, vote_db)
    assert board.iloc[0]["local"] == "Arraial A"
    assert board.iloc[0]["votes"] == 2


def test_accepts_timestamp(vote_db: Path):
    cast_vote("Arraial A", pd.Timestamp(DAY_A), voter_id="user-1", db_path=vote_db)
    assert total_votes(pd.Timestamp(DAY_A), vote_db) == 1
