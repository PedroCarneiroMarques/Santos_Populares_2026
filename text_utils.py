import re
from typing import List, Optional, Tuple

import pandas as pd

from config import MESES_PT

_RE_WHITESPACE = re.compile(r"[ \t]+")
_RE_DATE_LABEL = re.compile(r"(\d{1,2})\s+de\s+([\wÀ-ÿçÇãÃõÕáàâéêíóôúü-]+)", re.IGNORECASE)
_RE_BULLET_PREFIX = re.compile(r"^[\-–—•]+\s*")
_RE_DOUBLE_SEP = re.compile(r"\s*·\s*·\s*")
_RE_MULTI_SPACE = re.compile(r"\s{2,}")

EMPTY_CELL_VALUES = frozenset({".", "-", "—"})

_ACCENT_MAP = str.maketrans({
    "á": "a", "à": "a", "â": "a", "ã": "a", "ä": "a",
    "é": "e", "è": "e", "ê": "e", "ë": "e",
    "í": "i", "ì": "i", "î": "i", "ï": "i",
    "ó": "o", "ò": "o", "ô": "o", "õ": "o", "ö": "o",
    "ú": "u", "ù": "u", "û": "u", "ü": "u", "ç": "c",
    "Á": "A", "À": "A", "Â": "A", "Ã": "A", "Ä": "A",
    "É": "E", "È": "E", "Ê": "E", "Ë": "E",
    "Í": "I", "Ì": "I", "Î": "I", "Ï": "I",
    "Ó": "O", "Ò": "O", "Ô": "O", "Õ": "O", "Ö": "O",
    "Ú": "U", "Ù": "U", "Û": "U", "Ü": "U", "Ç": "C",
})

_WEEKDAY_SHORT = {
    "segunda-feira": "Seg", "terca-feira": "Ter", "terça-feira": "Ter",
    "quarta-feira": "Qua", "quinta-feira": "Qui", "sexta-feira": "Sex",
    "sabado": "Sáb", "sábado": "Sáb", "domingo": "Dom",
}


def normalize_text(value) -> str:
    if pd.isna(value):
        return ""
    return _RE_WHITESPACE.sub(" ", str(value).replace("\r", "\n")).strip()


def normalize_key(text: str) -> str:
    return normalize_text(text).translate(_ACCENT_MAP).lower().strip()


def clean_display_text(value) -> str:
    txt = normalize_text(value).replace("\n", " · ")
    txt = _RE_DOUBLE_SEP.sub(" · ", txt)
    return _RE_MULTI_SPACE.sub(" ", txt).strip(" ·")


def abbreviate_label(text: str, max_len: int = 14) -> str:
    text = clean_display_text(text)
    return text if len(text) <= max_len else text[: max_len - 1].rstrip() + "…"


def parse_date_label(label: str) -> Optional[pd.Timestamp]:
    label = normalize_text(label).replace("(Feriado)", "").replace("Feriado", "").strip()
    match = _RE_DATE_LABEL.search(label)
    if not match:
        return None
    month = MESES_PT.get(match.group(2).capitalize())
    if not month:
        return None
    return pd.Timestamp(year=2026, month=month, day=int(match.group(1)))


def split_multiline_cell(value: str) -> List[str]:
    txt = normalize_text(value)
    if not txt or txt in EMPTY_CELL_VALUES:
        return []
    lines = [_RE_BULLET_PREFIX.sub("", line).strip() for line in txt.split("\n") if line.strip()]
    if len(lines) > 1:
        return [line for line in lines if line and line not in EMPTY_CELL_VALUES]
    return [] if not lines or lines[0] in EMPTY_CELL_VALUES else lines


def coerce_date_range(value, min_date, max_date) -> Tuple:
    if isinstance(value, tuple) and len(value) == 2:
        return value[0], value[1]
    if isinstance(value, tuple) and len(value) == 1:
        return value[0], value[0]
    return min_date, max_date


def format_pt_date(ts: pd.Timestamp) -> str:
    return ts.strftime("%d/%m")


def relative_label(ts: pd.Timestamp, anchor: pd.Timestamp) -> str:
    days = (ts.normalize() - anchor.normalize()).days
    return {0: "Hoje", 1: "Amanhã"}.get(days, "Depois")


def short_weekday_pt(value: str) -> str:
    return _WEEKDAY_SHORT.get(normalize_key(value), clean_display_text(value)[:3].title())
