from functools import lru_cache
from typing import Dict, Iterable, List

from text_utils import clean_display_text, normalize_key, normalize_text

DEFAULT_PROFILE: Dict[str, float] = {
    "legado": 4.0, "mass_market": 4.0, "relevancia_atual": 4.0, "fit_santos": 4.5,
}

PROFILE_LABELS = {
    "legado": "Legado", "mass_market": "Popularidade",
    "relevancia_atual": "Atualidade", "fit_santos": "Fit Santos",
}

ARTIST_PROFILES: Dict[str, Dict[str, float]] = {
    "Anselmo Ralph": {"legado": 8.0, "mass_market": 8.5, "relevancia_atual": 7.5, "fit_santos": 6.0},
    "Banda FBO": {"legado": 3.5, "mass_market": 4.0, "relevancia_atual": 4.0, "fit_santos": 5.0},
    "D.A.M.A.": {"legado": 7.5, "mass_market": 8.5, "relevancia_atual": 7.5, "fit_santos": 6.0},
    "Deixa Rola": {"legado": 4.0, "mass_market": 5.0, "relevancia_atual": 5.5, "fit_santos": 7.0},
    "Deixa Rolá": {"legado": 4.0, "mass_market": 5.0, "relevancia_atual": 5.5, "fit_santos": 7.0},
    "Delfins": {"legado": 9.0, "mass_market": 8.5, "relevancia_atual": 5.5, "fit_santos": 6.5},
    "Descendentes": {"legado": 3.5, "mass_market": 4.0, "relevancia_atual": 4.0, "fit_santos": 5.0},
    "Dupla Mete Ca Sets": {"legado": 3.0, "mass_market": 4.0, "relevancia_atual": 4.5, "fit_santos": 6.0},
    "Dupla Mete Cá Sets": {"legado": 3.0, "mass_market": 4.0, "relevancia_atual": 4.5, "fit_santos": 6.0},
    "Fernando Correia Marques": {"legado": 8.5, "mass_market": 7.5, "relevancia_atual": 5.5, "fit_santos": 8.0},
    "Grande Noite de Santos": {"legado": 3.0, "mass_market": 4.0, "relevancia_atual": 5.0, "fit_santos": 7.5},
    "Inset Coin": {"legado": 3.0, "mass_market": 3.5, "relevancia_atual": 4.0, "fit_santos": 4.5},
    "Ivandro": {"legado": 4.5, "mass_market": 7.0, "relevancia_atual": 8.0, "fit_santos": 5.0},
    "Kiko Is Hot": {"legado": 3.0, "mass_market": 4.5, "relevancia_atual": 5.0, "fit_santos": 5.5},
    "Las Ketchup": {"legado": 8.0, "mass_market": 8.5, "relevancia_atual": 4.5, "fit_santos": 7.0},
    "Luis Fialho": {"legado": 4.5, "mass_market": 5.0, "relevancia_atual": 5.5, "fit_santos": 5.5},
    "Luís Fialho": {"legado": 4.5, "mass_market": 5.0, "relevancia_atual": 5.5, "fit_santos": 5.5},
    "Marchas Populares": {"legado": 8.5, "mass_market": 7.0, "relevancia_atual": 7.0, "fit_santos": 10.0},
    "Mega Santos": {"legado": 2.5, "mass_market": 4.0, "relevancia_atual": 4.5, "fit_santos": 6.0},
    "Miguel Azevedo": {"legado": 8.0, "mass_market": 8.0, "relevancia_atual": 6.0, "fit_santos": 8.0},
    "Nego do Borel": {"legado": 5.0, "mass_market": 7.0, "relevancia_atual": 5.5, "fit_santos": 4.5},
    "Non Stop": {"legado": 3.0, "mass_market": 3.5, "relevancia_atual": 4.5, "fit_santos": 4.5},
    "Noz Pimba": {"legado": 3.5, "mass_market": 4.5, "relevancia_atual": 4.5, "fit_santos": 7.5},
    "Pimbamix": {"legado": 3.5, "mass_market": 4.5, "relevancia_atual": 4.0, "fit_santos": 7.0},
    "Queres e Pimba": {"legado": 3.5, "mass_market": 4.5, "relevancia_atual": 4.5, "fit_santos": 7.5},
    "Queres é Pimba": {"legado": 3.5, "mass_market": 4.5, "relevancia_atual": 4.5, "fit_santos": 7.5},
    "Quim Barreiros": {"legado": 10.0, "mass_market": 9.5, "relevancia_atual": 8.0, "fit_santos": 10.0},
    "Radio 105.4": {"legado": 2.5, "mass_market": 3.5, "relevancia_atual": 4.5, "fit_santos": 5.0},
    "Rádio 105.4": {"legado": 2.5, "mass_market": 3.5, "relevancia_atual": 4.5, "fit_santos": 5.0},
    "Rosinha": {"legado": 7.5, "mass_market": 7.5, "relevancia_atual": 6.0, "fit_santos": 9.0},
    "Ruth Marlene": {"legado": 8.0, "mass_market": 8.0, "relevancia_atual": 5.5, "fit_santos": 9.0},
    "Sagres - A Revelar": {"legado": 2.0, "mass_market": 3.0, "relevancia_atual": 4.0, "fit_santos": 4.0},
    "Sagres - Over the rule": {"legado": 2.0, "mass_market": 3.0, "relevancia_atual": 4.0, "fit_santos": 4.0},
    "Santa Manel": {"legado": 3.5, "mass_market": 4.5, "relevancia_atual": 4.5, "fit_santos": 7.0},
    "Santamaria": {"legado": 9.0, "mass_market": 9.0, "relevancia_atual": 6.5, "fit_santos": 7.5},
    "Sergio Rossi": {"legado": 6.0, "mass_market": 6.5, "relevancia_atual": 5.5, "fit_santos": 8.0},
    "Sertaneijinho": {"legado": 3.0, "mass_market": 4.0, "relevancia_atual": 4.5, "fit_santos": 5.0},
    "Show Daqui Para Fora": {"legado": 3.0, "mass_market": 4.0, "relevancia_atual": 4.5, "fit_santos": 4.5},
    "Sons do Minho": {"legado": 6.5, "mass_market": 6.0, "relevancia_atual": 5.5, "fit_santos": 8.0},
    "Sérgio Rossi": {"legado": 6.0, "mass_market": 6.5, "relevancia_atual": 5.5, "fit_santos": 8.0},
    "Tanya": {"legado": 6.0, "mass_market": 6.5, "relevancia_atual": 5.0, "fit_santos": 7.0},
    "Tio Jel": {"legado": 4.5, "mass_market": 5.5, "relevancia_atual": 5.5, "fit_santos": 6.0},
    "Toy": {"legado": 10.0, "mass_market": 9.5, "relevancia_atual": 8.0, "fit_santos": 9.5},
    "Tributo aos Xutos": {"legado": 4.0, "mass_market": 5.5, "relevancia_atual": 4.5, "fit_santos": 5.0},
    "Tributo Popular": {"legado": 3.5, "mass_market": 4.5, "relevancia_atual": 4.0, "fit_santos": 7.0},
    "Van Zee": {"legado": 4.5, "mass_market": 7.0, "relevancia_atual": 8.0, "fit_santos": 4.5},
    "Vira Milho": {"legado": 3.5, "mass_market": 4.5, "relevancia_atual": 4.5, "fit_santos": 7.0},
    "Vozes em Liberdade": {"legado": 3.5, "mass_market": 4.0, "relevancia_atual": 4.5, "fit_santos": 5.0},
}

_PROFILES_NORM = sorted(
    [(normalize_key(name), profile) for name, profile in ARTIST_PROFILES.items()],
    key=lambda item: len(item[0]),
    reverse=True,
)

_CATEGORY_RULES = (
    (("marcha", "marchas"), "Marchas"),
    (("dj", "set"), "DJ / Club"),
    (("tributo",), "Tributo"),
    (("pimba", "barreiros", "rossi", "azevedo", "toy", "rosinha"), "Popular / Pimba"),
    (("banda", "show"), "Concerto"),
    (("sagres", "mega santos", "rádio", "radio"), "Ativação / Marca"),
)


def get_artist_profile(name: str) -> Dict[str, float]:
    key = normalize_key(name)
    for artist_key, profile in _PROFILES_NORM:
        if artist_key in key:
            return profile
    return DEFAULT_PROFILE


@lru_cache(maxsize=512)
def get_artist_score(name: str) -> float:
    profile = get_artist_profile(name)
    score = (
        profile["legado"] * 0.35
        + profile["mass_market"] * 0.25
        + profile["relevancia_atual"] * 0.20
        + profile["fit_santos"] * 0.20
    )
    return round(min(10.0, max(0.0, score)), 1)


def accumulate_arraial_score(acts: Iterable[str]) -> float:
    """Soma notoriedade de artistas únicos, limitada a 10, para valorizar cartazes completos."""
    seen: set[str] = set()
    total = 0.0
    for act in acts:
        cleaned = clean_display_text(act)
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        total += get_artist_score(cleaned)
    return round(min(10.0, total), 1)


def get_headliner_name(items: List[str]) -> str:
    return "Cartaz variado" if not items else clean_display_text(max(items, key=get_artist_score))


@lru_cache(maxsize=512)
def get_headliner_profile(name: str) -> str:
    profile = get_artist_profile(name)
    return PROFILE_LABELS[max(profile, key=profile.get)]


def classify_event(name: str) -> str:
    text = normalize_text(name).lower()
    for keywords, label in _CATEGORY_RULES:
        if any(keyword in text for keyword in keywords):
            return label
    return "Espetáculo"
