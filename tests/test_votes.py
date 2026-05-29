"""Tests for the arraial voting system."""
from pathlib import Path

import pytest

from votes import cast_vote, clear_vote, get_user_vote, get_vote_counts, get_vote_leaderboard, total_votes


@pytest.fixture
def vote_db(tmp_path: Path) -> Path:
    return tmp_path / "votes.db"


def test_cast_and_count_votes(vote_db: Path):
    cast_vote("Arraial A", voter_id="user-1", db_path=vote_db)
    cast_vote("Arraial B", voter_id="user-2", db_path=vote_db)
    cast_vote("Arraial A", voter_id="user-3", db_path=vote_db)

    counts = get_vote_counts(vote_db)
    assert counts["Arraial A"] == 2
    assert counts["Arraial B"] == 1
    assert total_votes(vote_db) == 3


def test_user_can_change_vote(vote_db: Path):
    cast_vote("Arraial A", voter_id="user-1", db_path=vote_db)
    cast_vote("Arraial C", voter_id="user-1", db_path=vote_db)

    assert get_user_vote("user-1", vote_db) == "Arraial C"
    assert get_vote_counts(vote_db) == {"Arraial C": 1}
    assert total_votes(vote_db) == 1


def test_clear_vote(vote_db: Path):
    cast_vote("Arraial A", voter_id="user-1", db_path=vote_db)
    clear_vote("user-1", vote_db)

    assert get_user_vote("user-1", vote_db) is None
    assert total_votes(vote_db) == 0


def test_leaderboard_order(vote_db: Path):
    cast_vote("Arraial B", voter_id="u1", db_path=vote_db)
    cast_vote("Arraial A", voter_id="u2", db_path=vote_db)
    cast_vote("Arraial A", voter_id="u3", db_path=vote_db)

    board = get_vote_leaderboard(5, vote_db)
    assert board.iloc[0]["local"] == "Arraial A"
    assert board.iloc[0]["votes"] == 2
