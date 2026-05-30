"""Tests for accumulated arraial scoring."""
from artists import accumulate_arraial_score, get_artist_score


def test_single_artist_unchanged():
    assert accumulate_arraial_score(["Toy"]) == get_artist_score("Toy")


def test_accumulates_unique_artists():
    score = accumulate_arraial_score(["Toy", "Quim Barreiros"])
    assert score == 10.0


def test_ignores_duplicates():
    single = accumulate_arraial_score(["Toy", "Toy"])
    assert single == get_artist_score("Toy")


def test_partial_accumulation_below_cap():
    score = accumulate_arraial_score(["Banda FBO", "Non Stop"])
    assert score == get_artist_score("Banda FBO") + get_artist_score("Non Stop")
    assert score < 10.0
