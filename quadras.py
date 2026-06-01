import hashlib
import random
import re
from typing import List, Optional

import streamlit as st

from config import QUADRAS_DIR

random.seed()

_RE_QUADRA_BLOCKS = re.compile(r"\n\s*\n")
_RE_MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^\)]+)\)")


def _load_quadras(filename: str) -> tuple[str, List[str], str]:
    raw = (QUADRAS_DIR / filename).read_text(encoding="utf-8")
    quadras = [block.strip() for block in _RE_QUADRA_BLOCKS.split(raw.strip()) if block.strip()]
    sig = hashlib.md5(raw.strip().encode("utf-8")).hexdigest()
    return raw, quadras, sig


_, QUADRAS_HERO, HERO_SIG = _load_quadras("quadras_hero.txt")
_, QUADRAS_MANJERICO, MANJERICO_SIG = _load_quadras("quadras_manjerico.txt")


def render_quadra_html(text: str) -> str:
    html = _RE_MARKDOWN_LINK.sub(
        r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', text
    )
    return html.replace("\n", "<br>")


def _pick(quadras: List[str], exclude: Optional[str] = None) -> str:
    if not quadras:
        return ""
    pool = [q for q in quadras if q != exclude] if exclude and len(quadras) > 1 else quadras
    return random.choice(pool)


def get_hero_quadra() -> str:
    if st.session_state.get("hero_sig") != HERO_SIG or "hero_quadra" not in st.session_state:
        st.session_state["hero_sig"] = HERO_SIG
        st.session_state["hero_quadra"] = _pick(QUADRAS_HERO, st.session_state.get("hero_quadra"))
    return st.session_state["hero_quadra"]


def _shuffle_cycle(n: int, avoid_first: Optional[int] = None) -> List[int]:
    """Return a shuffled cycle of indices. Quadras are drawn with list.pop()
    (from the end), so ``avoid_first`` is kept off the last position to prevent
    an immediate repeat across the seam of two cycles."""
    order = list(range(n))
    random.shuffle(order)
    if avoid_first is not None and len(order) > 1 and order[-1] == avoid_first:
        order[0], order[-1] = order[-1], order[0]
    return order


def _ensure_manjerico_deck() -> None:
    if not st.session_state.get("manjerico_deck"):
        st.session_state["manjerico_deck"] = _shuffle_cycle(
            len(QUADRAS_MANJERICO), avoid_first=st.session_state.get("manjerico_idx")
        )


def _advance_manjerico() -> str:
    if not QUADRAS_MANJERICO:
        st.session_state["manjerico_quadra"] = ""
        return ""
    _ensure_manjerico_deck()
    idx = st.session_state["manjerico_deck"].pop()
    st.session_state["manjerico_idx"] = idx
    chosen = QUADRAS_MANJERICO[idx]
    st.session_state["manjerico_quadra"] = chosen
    return chosen


def init_manjerico_quadra() -> None:
    if st.session_state.get("manjerico_sig") != MANJERICO_SIG or "manjerico_quadra" not in st.session_state:
        st.session_state["manjerico_sig"] = MANJERICO_SIG
        st.session_state["manjerico_deck"] = _shuffle_cycle(len(QUADRAS_MANJERICO))
        _advance_manjerico()


def next_manjerico_quadra() -> str:
    return _advance_manjerico()
