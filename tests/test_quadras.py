"""Tests for the manjerico quadra cycle logic."""
import random

from quadras import _shuffle_cycle


def test_cycle_is_a_full_permutation():
    for n in (1, 2, 5, 37):
        cycle = _shuffle_cycle(n)
        assert sorted(cycle) == list(range(n))


def test_cycle_avoids_immediate_repeat_at_seam():
    random.seed(0)
    for _ in range(200):
        cycle = _shuffle_cycle(5, avoid_first=3)
        assert cycle[-1] != 3


def test_single_quadra_cycle_is_stable():
    assert _shuffle_cycle(1) == [0]
    assert _shuffle_cycle(1, avoid_first=0) == [0]


def test_full_cycle_has_no_repeats_before_exhaustion():
    random.seed(1)
    n = 37
    deck = _shuffle_cycle(n)
    drawn = [deck.pop() for _ in range(n)]
    assert sorted(drawn) == list(range(n))
