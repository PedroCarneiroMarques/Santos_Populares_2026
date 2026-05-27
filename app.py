import re
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
import plotly.express as px
import plotly.io as pio
import streamlit as st


st.set_page_config(
    page_title="Guia Oficial das Festas de Lisboa",
    page_icon="🎈",
    layout="wide",
    initial_sidebar_state="expanded",
)

pio.templates.default = "plotly_white"

COLORS = {
    "bg": "#F4E6C8",
    "surface": "#FFF7E8",
    "surface_alt": "#F9EED8",
    "border": "#D8B98A",
    "border_strong": "#B88746",
    "text": "#3E2615",
    "muted": "#6E4B2A",
    "soft": "#8C6337",
    "accent": "#C62828",
    "accent_soft": "#FBE0D6",
    "section_tint": "#F3D94C",
    "shadow": "0 8px 22px rgba(92,54,18,.14)",
}

CHART_COLORS = ["#C62828", "#F2C300", "#1565C0", "#2E7D32", "#EF6C00", "#8E24AA"]

MESES_PT = {
    "Janeiro": 1,
    "Fevereiro": 2,
    "Março": 3,
    "Abril": 4,
    "Maio": 5,
    "Junho": 6,
    "Julho": 7,
    "Agosto": 8,
    "Setembro": 9,
    "Outubro": 10,
    "Novembro": 11,
    "Dezembro": 12,
}

DIAS_SEMANA_PT = {
    "Monday": "segunda-feira",
    "Tuesday": "terça-feira",
    "Wednesday": "quarta-feira",
    "Thursday": "quinta-feira",
    "Friday": "sexta-feira",
    "Saturday": "sábado",
    "Sunday": "domingo",
}

ARTIST_PROFILE_SCORES: Dict[str, Dict[str, float]] = {
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

QUADRAS_RAW = r"""Hoje é dia de Santo António
e das marchas populares,
a seguir São João
são pessoas aos milhares.


Santo António sem ricos
E toda a gente a saltar
Enfeitado de manjericos
Que eu vou comprar.


Santo António enfeitado
Dá cá um balão!
Pois quero um encarnado
Para dar ao meu irmão.


No Santo António enfeitado
Há cravos e manjericos
Sardinhas de cheiros encantados
Para os pobres e para os ricos.


A treze temos Santo António
A vinte e quatro S. João
A vinte e nove S. Pedro
E recebemo-los com uma grande emoção.


S. Pedro com as chaves do céu
Com o cordeiro S. João
E S. António
Com o menino na mão.


No dia de S. João
Vamos todos cantar
Brincar com um balão
Até ele rebentar.


No dia de S. Pedro
Vamos todos à sardinha
Neste ano vou escolher
A que for mais pequenina.


No dia de S. João
Vamos p'rá rua festejar
Lançar balões para o céu
Sempre, sempre a pular.


A noite de S. João
É uma noite de folia
Vejo o fogo de artifício
Sempre com muita alegria.


Santo António, São João
No Santo António
E no S. João
Como as sardinhas
E deixo o pão.


Nas noites de Sto. António
Vou saltar uma latada
E vou cantar, divertir-me
Com a minha namorada.


No mês dos santos populares
Vou p'rá rua, vou cantar
Não quero estar em casa
Quero é ir pular.


Santo António, Santo António
Que tens tu de especial?
Só sei que na tua festa
Há alegria no arraial.


Ó meu rico Santo António
És um santo popular
Na tua festa não falta
Sardinha para assar.


Santo António e S. João
Vão ao desafio cantar
Nas barracas das sardinhas
Espero poder passar.


Santo António, Santo António
Que bonito que tu és
Vou-te comprar um manjerico
E vou pô-lo a teus pés.


Ó meu rico Santo António
Tu estás muito calado
Quando estás à minha beira
Fico todo envergonhado.


Lisboa meu amor
Lisboa, és meu amor,
Quero contigo dançar
Cantar cheia de fulgor
A tradição popular.


De manjerico na mão
Uma quadra a namorar
E com arquinho e balão
Vamos todos a bailar.


Alegrias como estas
É difícil encontrar
Vestida toda de festas
Lisboa vai a cantar.


Há festa em Portugal
Há festa em Portugal
São os santos populares
Da sardinha ao manjerico
Os cheiros andam pelos ares.


Em Junho todos bailam
Assim é a tradição
As ruas estão enfeitadas
Lá de cima até ao chão."""


def parse_quadras(raw_text: str) -> List[str]:
    return [block.strip() for block in raw_text.strip().split("\n\n") if block.strip()]


def build_quadras() -> List[str]:
    return parse_quadras(QUADRAS_RAW)


def rotate_quadras(quadras: List[str]) -> Tuple[str, int]:
    if not quadras:
        return "", 0
    if "quadra_index" not in st.session_state:
        st.session_state.quadra_index = 0
    current_index = st.session_state.quadra_index % len(quadras)
    current_quadra = quadras[current_index]
    st.session_state.quadra_index = (current_index + 1) % len(quadras)
    return current_quadra, current_index


def render_quadra_html(markdown_text: str) -> str:
    html = markdown_text
    html = re.sub(
        r"\[([^\]]+)\]\((https?://[^\)]+)\)",
        r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>',
        html,
    )
    html = html.replace("\n", "<br>")
    return html


def inject_css():
    st.markdown(
        f"""
        <style>
        :root {{
            --bg: {COLORS['bg']};
            --surface: {COLORS['surface']};
            --surface-alt: {COLORS['surface_alt']};
            --border: {COLORS['border']};
            --border-strong: {COLORS['border_strong']};
            --text: {COLORS['text']};
            --muted: {COLORS['muted']};
            --soft: {COLORS['soft']};
            --accent: {COLORS['accent']};
            --accent-soft: {COLORS['accent_soft']};
            --section-tint: {COLORS['section_tint']};
            --shadow: {COLORS['shadow']};
        }}

        html, body, .stApp {{
            background: var(--bg);
            color: var(--text);
        }}

        .block-container {{
            max-width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }}

        .stMainBlockContainer {{
            padding: 0 !important;
        }}

        section[data-testid="stSidebar"] {{
            background: var(--surface);
            border-right: 1px solid var(--border);
        }}

        .content-shell {{
            width: min(1600px, calc(100vw - 88px));
            margin-left: auto;
            margin-right: auto;
            padding: .6rem 1rem 1.1rem 1rem;
        }}

        .hero,
        .metric-card,
        .card,
        .card-strong,
        .soft-card,
        .table-wrap,
        div[data-testid="stDataFrame"] {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 18px;
            box-shadow: var(--shadow);
            overflow: hidden;
        }}

        div[data-testid="stVerticalBlock"]:has(> .card-strong),
        div[data-testid="stVerticalBlock"]:has(> .card),
        div[data-testid="stVerticalBlock"]:has(> .metric-card),
        div[data-testid="stVerticalBlock"]:has(> .hero),
        div[data-testid="stVerticalBlock"]:has(> .table-wrap) {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }}

        .hero {{
            border-radius: 22px;
            padding: 1.35rem 1.1rem 1.2rem 1.1rem;
            margin-bottom: .85rem;
            text-align: center;
        }}

        .section-band {{
            background: transparent;
            border: none;
            border-radius: 0;
            padding: 0;
            margin-bottom: .85rem;
        }}

        .section-head {{
            margin: 0 0 .75rem 0;
        }}

        .section-grid-4 {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: .75rem;
            align-items: start;
            width: 100%;
        }}

        .section-grid-4 > * {{
            min-width: 0;
        }}

        .span-1 {{ grid-column: span 1; }}
        .span-2 {{ grid-column: span 2; }}
        .span-3 {{ grid-column: span 3; }}
        .span-4 {{ grid-column: span 4; }}

        .eyebrow, .section-label, .card-kicker {{
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: .06em;
            font-weight: 800;
            font-size: .7rem;
            margin-bottom: .28rem;
        }}

        .hero-title {{
            font-size: clamp(2.2rem, 5.6vw, 4.6rem);
            line-height: .95;
            letter-spacing: -.04em;
            font-weight: 900;
            margin: 0 auto .7rem auto;
            max-width: 14ch;
            text-wrap: balance;
        }}

        .hero-copy, .section-copy, .card-copy, .metric-note, .rank-meta {{
            color: var(--muted);
            font-size: .92rem;
            line-height: 1.52;
        }}

        .hero-copy {{
            max-width: 36ch;
            margin: 0 auto;
            text-align: center;
        }}

        .hero-copy a {{
            color: var(--accent);
            text-decoration: none;
            border-bottom: 1px solid rgba(155,54,39,.25);
        }}

        .hero-copy a:hover {{
            border-bottom-color: rgba(155,54,39,.6);
        }}

        .eyebrow {{
            text-align: center;
            margin-bottom: .5rem;
        }}

        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            align-items: stretch;
            gap: .75rem;
            margin-bottom: .85rem;
        }}

        .metric-card,
        .card,
        .card-strong {{
            padding: 1rem;
            height: 100%;
        }}

        .metric-label {{
            color: var(--soft);
            text-transform: uppercase;
            letter-spacing: .07em;
            font-size: .7rem;
            font-weight: 800;
            margin-bottom: .35rem;
        }}

        .metric-value {{
            font-size: clamp(1.35rem, 1.9vw, 1.85rem);
            line-height: 1.02;
            font-weight: 900;
            margin-bottom: .15rem;
        }}

        .card-title {{
            color: var(--text);
            font-size: 1.12rem;
            line-height: 1.16;
            font-weight: 850;
            margin-bottom: .25rem;
        }}

        .pick-card {{
            background: var(--accent_soft);
            border: 1px solid #E3A39A;
            border-radius: 16px;
            padding: .9rem;
        }}

        .soft-card {{
            padding: .8rem;
        }}

        .chip {{
            display: inline-block;
            padding: .32rem .55rem;
            border-radius: 999px;
            font-size: .77rem;
            font-weight: 700;
            margin-right: .32rem;
            margin-bottom: .32rem;
        }}

        .chip-red {{ background: var(--accent-soft); color: var(--accent); border: 1px solid #E3A39A; }}
        .chip-olive {{ background: #E4F3E3; color: #1F6B35; border: 1px solid #97C59A; }}
        .chip-gold {{ background: #FFF3BF; color: #9A6A00; border: 1px solid #E5C94B; }}

        .rank-row {{
            padding: .7rem 0;
            border-bottom: 1px solid var(--border);
        }}

        .rank-row:last-child {{
            border-bottom: none;
            padding-bottom: .25rem;
        }}

        .card-strong {{
            margin-bottom: .9rem;
        }}

        .card-strong + div[data-testid="stPlotlyChart"] {{
            margin-top: .55rem;
            margin-bottom: 1rem;
        }}

        .table-wrap {{
            margin-top: .55rem;
            overflow: hidden;
        }}

        .rank-place {{
            color: var(--text);
            font-size: .96rem;
            font-weight: 800;
            line-height: 1.28;
            margin-bottom: .12rem;
        }}

        .stDownloadButton button {{
            border-radius: 12px !important;
            border: 1px solid var(--border-strong) !important;
            background: var(--surface) !important;
            color: var(--text) !important;
            font-weight: 700 !important;
        }}

        @media (max-width: 1100px) {{
            .content-shell {{ width: calc(100vw - 72px); }}
        }}

        @media (max-width: 980px) {{
            .content-shell {{
                width: 100%;
                max-width: 100%;
                margin: 0;
                padding: .7rem .85rem 1rem .85rem;
            }}

            .metric-grid,
            .section-grid-4 {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}

            .span-1, .span-2, .span-3, .span-4 {{
                grid-column: span 2;
            }}
        }}

        @media (max-width: 768px) {{
            .hero-title {{
                max-width: 14ch;
                font-size: 2.35rem;
                margin-left: auto;
                margin-right: auto;
            }}

            .metric-grid,
            .section-grid-4 {{
                grid-template-columns: 1fr;
                gap: .6rem;
            }}

            .span-1, .span-2, .span-3, .span-4 {{
                grid-column: span 1;
            }}

            .metric-note {{
                display: none;
            }}

            .hero,
            .metric-card,
            .card,
            .card-strong,
            .soft-card,
            .pick-card,
            .table-wrap,
            div[data-testid="stDataFrame"] {{
                border-radius: 16px;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def strip_accents(text: str) -> str:
    replacements = str.maketrans({
        "á": "a", "à": "a", "â": "a", "ã": "a", "ä": "a",
        "é": "e", "è": "e", "ê": "e", "ë": "e",
        "í": "i", "ì": "i", "î": "i", "ï": "i",
        "ó": "o", "ò": "o", "ô": "o", "õ": "o", "ö": "o",
        "ú": "u", "ù": "u", "û": "u", "ü": "u",
        "ç": "c",
        "Á": "A", "À": "A", "Â": "A", "Ã": "A", "Ä": "A",
        "É": "E", "È": "E", "Ê": "E", "Ë": "E",
        "Í": "I", "Ì": "I", "Î": "I", "Ï": "I",
        "Ó": "O", "Ò": "O", "Ô": "O", "Õ": "O", "Ö": "O",
        "Ú": "U", "Ù": "U", "Û": "U", "Ü": "U",
        "Ç": "C",
    })
    return str(text).translate(replacements)


def normalize_text(value) -> str:
    if pd.isna(value):
        return ""
    return re.sub(r"[ \t]+", " ", str(value).replace("\r", "\n")).strip()


def normalize_artist_name(name: str) -> str:
    return strip_accents(normalize_text(name)).lower().strip()


def clean_display_text(value) -> str:
    txt = normalize_text(value).replace("\n", " · ")
    txt = re.sub(r"\s*·\s*·\s*", " · ", txt)
    return re.sub(r"\s{2,}", " ", txt).strip(" ·")


def get_artist_profile(name: str) -> Dict[str, float]:
    n = normalize_artist_name(name)
    for artist, profile in ARTIST_PROFILE_SCORES.items():
        if normalize_artist_name(artist) in n:
            return profile
    return {"legado": 4.0, "mass_market": 4.0, "relevancia_atual": 4.0, "fit_santos": 4.5}


def get_artist_score(name: str) -> float:
    profile = get_artist_profile(name)
    score = (
        profile["legado"] * 0.35
        + profile["mass_market"] * 0.25
        + profile["relevancia_atual"] * 0.20
        + profile["fit_santos"] * 0.20
    )
    return round(min(10.0, max(0.0, score)), 1)


def get_headliner_name(items: List[str]) -> str:
    if not items:
        return "Cartaz variado"
    ranked = sorted(items, key=lambda x: get_artist_score(x), reverse=True)
    return clean_display_text(ranked[0]) if ranked else "Cartaz variado"


def get_headliner_profile(name: str) -> str:
    profile = get_artist_profile(name)
    labels = {
        "legado": "Legado",
        "mass_market": "Popularidade",
        "relevancia_atual": "Atualidade",
        "fit_santos": "Fit Santos",
    }
    top_dim = max(profile, key=profile.get)
    return labels[top_dim]


def parse_date_label(label: str) -> Optional[pd.Timestamp]:
    label = normalize_text(label).replace("(Feriado)", "").replace("Feriado", "").strip()
    match = re.search(r"(\d{1,2})\s+de\s+([\wÀ-ÿçÇãÃõÕáàâéêíóôúü-]+)", label, re.IGNORECASE)
    if not match:
        return None
    day = int(match.group(1))
    month_name = match.group(2).capitalize()
    month = MESES_PT.get(month_name)
    if not month:
        return None
    return pd.Timestamp(year=2026, month=month, day=day)


def classify_event(name: str) -> str:
    n = normalize_text(name).lower()
    if any(x in n for x in ["marcha", "marchas"]):
        return "Marchas"
    if any(x in n for x in ["dj", "set"]):
        return "DJ / Club"
    if "tributo" in n:
        return "Tributo"
    if any(x in n for x in ["pimba", "barreiros", "rossi", "azevedo", "toy", "rosinha"]):
        return "Popular / Pimba"
    if any(x in n for x in ["banda", "show"]):
        return "Concerto"
    if any(x in n for x in ["sagres", "mega santos", "rádio", "radio"]):
        return "Ativação / Marca"
    return "Espetáculo"


def split_multiline_cell(value: str) -> List[str]:
    txt = normalize_text(value)
    if not txt or txt in {".", "-", "—"}:
        return []
    lines = [line.strip() for line in txt.split("\n") if line.strip()]
    if len(lines) > 1:
        out = []
        for line in lines:
            line = re.sub(r"^[\-–—•]+\s*", "", line).strip()
            if line and line not in {".", "-", "—"}:
                out.append(line)
        return out
    single = re.sub(r"^[\-–—•]+\s*", "", txt).strip()
    return [] if not single or single in {".", "-", "—"} else [single]


def coerce_date_range(v, min_date, max_date) -> Tuple:
    if isinstance(v, tuple) and len(v) == 2:
        return v[0], v[1]
    if isinstance(v, tuple) and len(v) == 1:
        return v[0], v[0]
    return min_date, max_date


def format_pt_date(ts: pd.Timestamp) -> str:
    return ts.strftime("%d/%m")


def relative_label(ts: pd.Timestamp, anchor: pd.Timestamp) -> str:
    d = (ts.normalize() - anchor.normalize()).days
    if d == 0:
        return "Hoje"
    if d == 1:
        return "Amanhã"
    return "Depois"


def top_acts_text(items: List[str], limit: int = 3) -> str:
    clean = [clean_display_text(x) for x in items if clean_display_text(x)]
    return ", ".join(clean[:limit]) if clean else "Mais surpresas a caminho"


@st.cache_data(ttl=3600, show_spinner=False)
def load_and_prepare_data(file_bytes: bytes):
    raw = pd.read_excel(BytesIO(file_bytes), header=None, engine="openpyxl")
    header_row = 2
    headers = [normalize_text(x) for x in raw.iloc[header_row].tolist()]
    df = raw.iloc[header_row + 1 :].copy()
    df.columns = headers
    df = df.dropna(how="all").copy()
    df = df.rename(columns={"Dia": "dia", "Dia da Semana": "dia_semana_excel"})
    if "dia" not in df.columns or "dia_semana_excel" not in df.columns:
        raise ValueError("Não foi possível localizar as colunas 'Dia' e 'Dia da Semana'.")

    df = df.dropna(axis=1, how="all").copy()
    event_cols = [c for c in df.columns if c not in ["dia", "dia_semana_excel"]]
    long_df = df.melt(
        id_vars=["dia", "dia_semana_excel"],
        value_vars=event_cols,
        var_name="local",
        value_name="conteudo",
    )
    long_df["conteudo"] = long_df["conteudo"].apply(normalize_text)
    long_df = long_df[(long_df["conteudo"] != "") & (~long_df["conteudo"].isin([".", "-", "—"]))].copy()
    long_df["data"] = long_df["dia"].apply(parse_date_label)
    long_df = long_df.dropna(subset=["data"]).copy()

    records = []
    for _, row in long_df.iterrows():
        for entry in split_multiline_cell(row["conteudo"]):
            records.append(
                {
                    "data": row["data"],
                    "dia_label": normalize_text(row["dia"]),
                    "dia_semana_excel": normalize_text(row["dia_semana_excel"]),
                    "local": clean_display_text(row["local"]),
                    "artista_evento": clean_display_text(entry),
                    "conteudo_original": clean_display_text(row["conteudo"]),
                }
            )

    events = pd.DataFrame(records)
    if events.empty:
        return events

    events["dia_semana"] = events["data"].dt.day_name().map(DIAS_SEMANA_PT).fillna(events["dia_semana_excel"])
    events["fim_de_semana"] = events["data"].dt.dayofweek >= 4
    events["feriado"] = events["dia_label"].str.contains("Feriado", case=False, na=False)
    events["categoria"] = events["artista_evento"].apply(classify_event)
    events["artist_score"] = events["artista_evento"].apply(get_artist_score)
    events["artist_profile_label"] = events["artista_evento"].apply(get_headliner_profile)
    daily_count = events.groupby("data").size().rename("eventos_no_dia")
    events = events.merge(daily_count, on="data", how="left")
    return events.sort_values(["data", "local", "artista_evento"]).reset_index(drop=True)


def get_anchor_date(df_filtered: pd.DataFrame) -> pd.Timestamp:
    today = pd.Timestamp.now().normalize()
    dates = sorted(pd.to_datetime(df_filtered["data"].dropna().unique()))
    if not dates:
        return today
    future = [d for d in dates if d >= today]
    return future[0] if future else dates[-1]


def build_focus(df_filtered: pd.DataFrame, anchor_date: pd.Timestamp, horizon: int = 3) -> pd.DataFrame:
    target_dates = pd.date_range(anchor_date, periods=horizon, freq="D")
    focus = df_filtered[df_filtered["data"].isin(target_dates)].copy()
    if focus.empty:
        fallback_dates = sorted(pd.to_datetime(df_filtered["data"].unique()))[:horizon]
        focus = df_filtered[df_filtered["data"].isin(fallback_dates)].copy()
    return focus


def summarize_options(day_df: pd.DataFrame) -> pd.DataFrame:
    if day_df.empty:
        return pd.DataFrame()

    grouped = (
        day_df.groupby("local")
        .agg(
            eventos=("artista_evento", "count"),
            atos_unicos=("artista_evento", pd.Series.nunique),
            score_notoriedade=("artist_score", "max"),
        )
        .reset_index()
    )

    acts = (
        day_df.groupby("local")["artista_evento"]
        .apply(lambda s: list(dict.fromkeys([clean_display_text(x) for x in s.tolist() if clean_display_text(x)]))[:5])
        .reset_index(name="top_atos")
    )

    grouped = grouped.merge(acts, on="local", how="left")
    grouped["cabeca_cartaz"] = grouped["top_atos"].apply(get_headliner_name)
    grouped["forca_cartaz"] = grouped["cabeca_cartaz"].apply(get_artist_score)
    grouped["perfil_forca"] = grouped["cabeca_cartaz"].apply(get_headliner_profile)
    grouped["score"] = grouped["forca_cartaz"].round(1)
    return grouped.sort_values(["score", "eventos", "atos_unicos"], ascending=[False, False, False])


def day_mood(day_df: pd.DataFrame) -> str:
    if day_df.empty:
        return "Sem festa marcada"
    total = len(day_df)
    locais = day_df["local"].nunique()
    if total >= 12 and locais >= 5:
        return "Grande arraial"
    if total <= 4:
        return "Mais calmo"
    return "Boa onda"


def build_day_summary(day_df: pd.DataFrame) -> dict:
    options = summarize_options(day_df)
    if options.empty:
        return {}

    best = options.iloc[0]
    top_acts = best["top_atos"] if isinstance(best["top_atos"], list) else []
    return {
        "total": len(day_df),
        "arraiais": day_df["local"].nunique(),
        "mood": day_mood(day_df),
        "best_local": best["local"],
        "best_events": int(best["eventos"]),
        "best_unique": int(best["atos_unicos"]),
        "best_headliner": best.get("cabeca_cartaz", "Cartaz variado"),
        "best_score": round(float(best.get("score", 0)), 1),
        "best_profile": best.get("perfil_forca", "Notoriedade"),
        "top_acts": top_acts,
        "options": options,
    }


inject_css()

candidate_paths = [Path("data/santos.xlsx"), Path("santos.xlsx"), Path("./data/santos.xlsx")]
file_bytes = None
for local_path in candidate_paths:
    if local_path.exists():
        file_bytes = local_path.read_bytes()
        break

if file_bytes is None:
    uploaded_file = st.file_uploader("Carregar ficheiro Excel", type=["xlsx"], accept_multiple_files=False)
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()

if file_bytes is None:
    st.info("Carrega o Excel para pôr a festa a mexer.")
    st.stop()

try:
    df = load_and_prepare_data(file_bytes)
except Exception as e:
    st.error("Houve um tropeção a abrir o ficheiro Excel.")
    st.exception(e)
    st.stop()

if df.empty:
    st.error("Não encontrei arraiais válidos neste ficheiro.")
    st.stop()

st.sidebar.header("Filtros")
min_date = df["data"].min().date()
max_date = df["data"].max().date()
anchor_default = get_anchor_date(df)
default_end = min((anchor_default + pd.Timedelta(days=6)).date(), max_date)

date_range = st.sidebar.date_input(
    "Intervalo",
    value=(anchor_default.date(), default_end),
    min_value=min_date,
    max_value=max_date,
)
data_inicio, data_fim = coerce_date_range(date_range, min_date, max_date)

locais = ["Todos"] + sorted(df["local"].dropna().unique().tolist())
categorias = ["Todas"] + sorted(df["categoria"].dropna().unique().tolist())
local_sel = st.sidebar.selectbox("Local", locais)
categoria_sel = st.sidebar.selectbox("Categoria", categorias)
fim_de_semana_only = st.sidebar.checkbox("Só sexta a domingo")

mask = (df["data"] >= pd.Timestamp(data_inicio)) & (df["data"] <= pd.Timestamp(data_fim))
if local_sel != "Todos":
    mask &= df["local"] == local_sel
if categoria_sel != "Todas":
    mask &= df["categoria"] == categoria_sel
if fim_de_semana_only:
    mask &= df["data"].dt.dayofweek >= 4

df_filtered = df.loc[mask].copy()
if df_filtered.empty:
    st.warning("Com estes filtros, a festa ficou vazia.")
    st.stop()

anchor_date = get_anchor_date(df_filtered)
focus_df = build_focus(df_filtered, anchor_date, horizon=3)
focus_dates = sorted(pd.to_datetime(focus_df["data"].unique()))
if not focus_dates:
    st.warning("Não há festa marcada nos próximos dias com estes filtros.")
    st.stop()

first_day = focus_dates[0]
first_df = focus_df[focus_df["data"] == first_day].copy()
first_summary = build_day_summary(first_df)
next_summaries = []
for day in focus_dates[1:3]:
    day_df = focus_df[focus_df["data"] == day].copy()
    next_summaries.append((day, day_df, build_day_summary(day_df)))

window_events = len(focus_df)
window_days = len(focus_dates)
window_locals = focus_df["local"].nunique()
top_local = first_summary["best_local"]
first_day_name = clean_display_text(first_df["dia_semana"].iloc[0]).capitalize()

top_today = first_summary["options"].head(5)
daily = (
    df_filtered.groupby(["data", "local"])
    .size()
    .reset_index(name="eventos")
    .sort_values(["data", "eventos"], ascending=[True, False])
)
daily["data_label"] = pd.to_datetime(daily["data"]).dt.strftime("%d/%m")
date_order = daily[["data", "data_label"]].drop_duplicates().sort_values("data")["data_label"].tolist()

st.markdown('<div class="content-shell">', unsafe_allow_html=True)

quadras = build_quadras()
quadra_atual, _ = rotate_quadras(quadras)
quadra_html = render_quadra_html(quadra_atual)

st.markdown(
    f"""
    <div class="hero">
      <div class="eyebrow">🇵🇹💃🎉 Santos Populares 2026 💃🎉🇵🇹</div>
      <div class="hero-title">Guia Oficial das Festas de Lisboa</div>
      <div class="hero-copy">{quadra_html}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-label">Entrada a matar</div><div class="section-copy">Um olhar rápido para entrares no ritmo da festa sem perder tempo.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='metric-grid'>"
    + "".join(
        [
            f"<div class='metric-card'><div class='metric-label'>Janela ativa</div><div class='metric-value'>{window_days} dias</div><div class='metric-note'>Festa à vista</div></div>",
            f"<div class='metric-card'><div class='metric-label'>Eventos</div><div class='metric-value'>{window_events}</div><div class='metric-note'>Momentos em cartaz</div></div>",
            f"<div class='metric-card'><div class='metric-label'>Arraiais</div><div class='metric-value'>{window_locals}</div><div class='metric-note'>Arraiais a mexer</div></div>",
            f"<div class='metric-card'><div class='metric-label'>Maior cartaz</div><div class='metric-value'>{top_local}</div><div class='metric-note'>{first_summary['best_headliner']} · Nota {first_summary['best_score']}/10</div></div>",
        ]
    )
    + "</div>",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-band">', unsafe_allow_html=True)
st.markdown(
    '<div class="section-head"><div class="section-label">Onde começa a festa</div><div class="section-copy">A força de cada arraial é definida apenas pelo nome mais forte do cartaz em cada dia.</div></div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="section-grid-4">', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="card-strong span-2">
      <div class="card-kicker">Hoje · {first_summary['mood']}</div>
      <div class="card-title">{format_pt_date(first_day)} · {first_day_name}</div>
      <div class="card-copy">{first_summary['total']} entradas distribuídas por {first_summary['arraiais']} arraiais. O destaque é definido pelo artista mais forte do cartaz, sem somar nomes.</div>
      <div style="height:.75rem"></div>
      <div class="pick-card">
        <div class="card-kicker">Arraial em destaque</div>
        <div class="card-title">{first_summary['best_local']}</div>
        <div class="card-copy">Cabeça de cartaz: {first_summary['best_headliner']}</div>
      </div>
      <div style="height:.75rem"></div>
      <span class="chip chip-red">{first_summary['best_events']} eventos</span>
      <span class="chip chip-olive">{first_summary['best_profile']}</span>
      <span class="chip chip-gold">Score {first_summary['best_score']}/10</span>
    </div>
    """,
    unsafe_allow_html=True,
)

for day, day_df, summary in next_summaries:
    if not summary:
        continue
    day_name = clean_display_text(day_df["dia_semana"].iloc[0]).capitalize()
    st.markdown(
        f"""
        <div class="card span-1">
          <div class="card-kicker">{relative_label(day, anchor_date)} · Grande arraial</div>
          <div class="card-title">{format_pt_date(day)} · {day_name}</div>
          <div class="card-copy">{summary['total']} entradas · {summary['arraiais']} arraiais</div>
          <div style="height:.5rem"></div>
          <div class="soft-card">
            <div class="rank-place">{summary['best_local']}</div>
            <div class="rank-meta">Cabeça de cartaz: {summary['best_headliner']} · Score {summary['best_score']}/10</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

fig = px.bar(
    daily,
    x="data_label",
    y="eventos",
    color="local",
    color_discrete_sequence=CHART_COLORS,
    category_orders={"data_label": date_order},
    title="",
)
fig.update_layout(
    paper_bgcolor=COLORS["surface"],
    plot_bgcolor=COLORS["surface"],
    font=dict(color=COLORS["text"], size=12),
    margin=dict(l=18, r=18, t=54, b=12),
    legend_title_text="Local",
    xaxis_title="Data",
    yaxis_title="Eventos",
    barmode="stack",
    bargap=0.32,
    height=360,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        font=dict(size=10),
    ),
)
fig.update_xaxes(showgrid=False, tickangle=0)
fig.update_yaxes(gridcolor="rgba(110,75,42,0.18)", rangemode="tozero")

ranking_html = ['<div class="card-strong">']
ranking_html.append(
    '<div class="card-kicker">Arraiais mais quentes do dia</div><div class="card-copy">A hierarquia é definida pela maior nota individual de notoriedade do dia.</div>'
)
for i, (_, row) in enumerate(top_today.iterrows(), start=1):
    ranking_html.append(
        f"<div class='rank-row'><div class='rank-place'>{i}. {row['local']}</div><div class='rank-meta'>{row.get('cabeca_cartaz', 'Cartaz variado')} · Score {round(float(row.get('score', 0)), 1)}/10 · {row.get('perfil_forca', 'Notoriedade')}</div></div>"
    )
ranking_html.append("</div>")
st.markdown("".join(ranking_html), unsafe_allow_html=True)

st.markdown(
    '<div class="card-strong"><div class="card-kicker">Termómetro da festa</div><div class="card-copy">Um mapa rápido da animação para perceber onde a festa ganha força.</div></div>',
    unsafe_allow_html=True,
)
st.plotly_chart(fig, use_container_width=True, theme=None, config={"displayModeBar": False})

st.markdown(
    "<div class='section-label'>Roteiro completo</div><div class='section-copy'>No fim tens a lista completa para afinar o roteiro ao teu gosto.</div>",
    unsafe_allow_html=True,
)

table_view = focus_df[["data", "dia_semana", "local", "artista_evento", "categoria", "feriado"]].rename(
    columns={
        "data": "Data",
        "dia_semana": "Dia",
        "local": "Local",
        "artista_evento": "Artista / Evento",
        "categoria": "Categoria",
        "feriado": "Feriado",
    }
).copy()
table_view["Data"] = pd.to_datetime(table_view["Data"]).dt.strftime("%d/%m/%Y")
table_view["Score de Notoriedade"] = focus_df["artist_score"].round(1).values
table_view["Perfil"] = focus_df["artist_profile_label"].values

st.markdown('<div class="table-wrap">', unsafe_allow_html=True)
st.dataframe(table_view, use_container_width=True, hide_index=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

csv = table_view.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "⬇️ Exportar roteiro atual (CSV)",
    data=csv,
    file_name="santos_populares_proximos_dias.csv",
    mime="text/csv",
)