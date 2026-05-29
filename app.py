import hashlib
import random
import re
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

random.seed()

st.set_page_config(
    page_title="Guia Oficial das Festas de Lisboa para o (B)enfica(B)eer(C)lub",
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
    "green_zone": "#4CAF50",
    "green_zone_dark": "#2E7D32",
    "green_zone_light": "#7BC96F",
    "green_zone_text": "#F7FFE9",
}

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

QUADRAS_HERO_RAW = r"""Lisboa meu amor
Lisboa, és meu amor,
Quero contigo dançar
Cantar cheia de fulgor
A tradição popular.

Alegrias como estas
É difícil encontrar
Vestida toda de festas
Lisboa vai a cantar.

Há festa em Portugal
São os santos populares
Da sardinha ao manjerico
Os cheiros andam pelos ares

Santo António, Santo António
Que bonito que tu és
Vou-te comprar um manjerico
E vou pô-lo a teus pés.

Ó meu rico Santo António
És um santo popular
Na tua festa não falta
Sardinha para assar.

De manjerico na mão
Uma quadra a namorar
E com arquinho e balão
Vamos todos a bailar.

No mês dos santos populares
Vou p'rá rua, vou cantar
Não quero estar em casa
Quero é ir pular.

Santo António, Santo António
Que tens tu de especial?
Só sei que na tua festa
Há alegria no arraial."""

QUADRAS_MANJERICO_RAW = r"""Uma cerveja atrás da outra
E caracóis para o bandulho
Coitado do amigo Serra
Só vê a Rita em Julho

Noites tardias e confusão
Deixa o Tony bem mal disposto
Agora se estiver bem frequentado
Em vez de Junho entra Agosto

Sem colete de forcado
O Cajó toureia em Julho
Quando está todo embebedado
Façam BARUUUUULHOOOO!

Cerveja todos os dias
Mas à segunda é que é vida
Todos sabemos que a Carol
É a irmã preferida

Diz que bebe à animal
Diz que é a melhor brasa
O Gonçalo tem de abalar
Perdeu a ganza, vai a casa

Quando falamos em modelo
Não é do supermercado
A Mariana de Civil
Não pega nenhum coitado

Em nenhum bailarico
Ela vai ver um Trincão
Mariana de Ourém
Com sorte tens um lampião

Quer sempre ir pra casa
Mas tem tantos jantares, é uma sorte
Porque a Patrícia Ribeiro
Vê que há neve em Nova York

Vai buscar jola ao balcão
Com a ajuda de um escada
Ai a Ana, a miminho
Fica até de madrugada

Cheira a lenha em todo o lado
Pergunta sempre: Queres fumar?
A do Carvolhoto é purex
Amigo, quero-me é embebedar

Não tenhas nenhum acidente
Rezamos pelo teu bem estar
Pois menina Inês Rosa
Já não há airbag para salvar

A calvice ja não afeta
Já não tem dor de cotovelo
Lopes é feio teres pago
Para teres um tufo de cabelo

Com entradas a Vegeta
Até tem um super poder
O grande amigo Marques
Ele não pára de beber

20 dias sem dormir
Foi a lenda que eu ouvi
Ó meste Pedro Ribeiro
Queríamos ser iguais a ti

Copo cheio a toda a hora
Amêndoa amarga ou Gin
Até ganhas bem Maria
Paga um copo a mim

Come banana e puxa carroça
E tem ressaca de 3 dias
Alberto Cachindele
Não aguentavas, não bebias

O puto que sabe mais que outros
Tem aço, fúria e tem vontade
Bora lá Tomás Évora
És filho da liberdade

Para que bar irá agora
Zezão está sempre apromado
Sempre pronto para o bailarico
Bora lá meu Rei do Gado

Com proeza a declamar
Vem o nosso Gama de aparelho
Não queria dizer na rima
Já lá vi preso um pentelho

Quando a Taylor cá vem
Na fila espera até mais não
Ó Patricia Swifty
Quem pagou foi o patrão

Para o Iria onde há alcool
Para beber é onde for
É até de madrugada
Então bota calor

Foi para a aldeia porque é trolha
Com o Benfica muito gritas
Bora lá Carlos Serra
O grande seca-"Pipas"

Parece o outro com entradas
Talvez fique até de manhã
É um enigma do Benny
Na na na na na na na

Um dos carecas do grupo
Que é velho isso sei eu
Isac, o rei das motas
Usa boina e nao chapéu

Antigamente um bom vivã
Agora dorme na parada
Meu belo Afonso Costa
Vais ser pai não tarda nada

A Patrícia é bem magrinha
Mas alegra o arraial
Tem um sorriso tão grande
Que não há outra igual

Nestes Santos de Lisboa
Com certeza vê o Toy
Mas o que bate ao Carvalhoto
É a saudade do lady boy

Vamos todos por ela
Não chega a ver ninguém cantar
Pobre da Inês Rosa
Teve de ir a casa jantar

Caseiro como ele não há
Fica agarrado às cadelas
O meu Lopes assanhado
O meu grande monta-nelas

O Gama vai aos Santos
É o maior do arraial
Vira bicas de cerveja
Até fica a ver mal

Antigo rei das tainadas
Sempre de copo na mão
Para o mês que vem o puto Afonso
Só agarra num biberão

Tanta dica, tanta festa
Ela até "fazia"
Depois vais-se a ver
A Inês nao aparecia"""


def parse_quadras(raw_text: str) -> List[str]:
    return [block.strip() for block in re.split(r"\n\s*\n", raw_text.strip()) if block.strip()]


def build_quadras(raw_text: str) -> List[str]:
    return parse_quadras(raw_text)


def content_signature(raw_text: str) -> str:
    return hashlib.md5(raw_text.strip().encode("utf-8")).hexdigest()


def random_quadra(quadras: List[str], exclude: Optional[str] = None) -> str:
    if not quadras:
        return ""
    pool = [q for q in quadras if q != exclude] if exclude and len(quadras) > 1 else quadras
    return random.choice(pool)


def get_randomized_hero_quadra(raw_text: str) -> str:
    quadras = build_quadras(raw_text)
    if not quadras:
        return ""

    sig = content_signature(raw_text)
    prev_sig = st.session_state.get("hero_quadras_sig")

    if prev_sig != sig or "hero_quadra_text" not in st.session_state:
        prev_quadra = st.session_state.get("hero_quadra_text")
        chosen = random_quadra(quadras, exclude=prev_quadra)
        st.session_state["hero_quadras_sig"] = sig
        st.session_state["hero_quadra_text"] = chosen

    return st.session_state["hero_quadra_text"]


def init_manjerico_quadra(raw_text: str) -> None:
    quadras = build_quadras(raw_text)
    sig = content_signature(raw_text)
    prev_sig = st.session_state.get("manjerico_quadras_sig")

    if prev_sig != sig:
        st.session_state["manjerico_quadras_sig"] = sig
        st.session_state["manjerico_quadra_text"] = random_quadra(quadras)
    elif "manjerico_quadra_text" not in st.session_state:
        st.session_state["manjerico_quadra_text"] = random_quadra(quadras)


def next_manjerico_quadra(raw_text: str) -> str:
    quadras = build_quadras(raw_text)
    current = st.session_state.get("manjerico_quadra_text")
    chosen = random_quadra(quadras, exclude=current)
    st.session_state["manjerico_quadra_text"] = chosen
    return chosen


def render_quadra_html(markdown_text: str) -> str:
    html = markdown_text
    html = re.sub(
        r"\[([^\]]+)\((https?://[^\)]+)\)",
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
            --green-zone: {COLORS['green_zone']};
            --green-zone-dark: {COLORS['green_zone_dark']};
            --green-zone-light: {COLORS['green_zone_light']};
            --green-zone-text: {COLORS['green_zone_text']};
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

        section[data-testid="stSidebar"] * {{
            color: var(--text) !important;
            opacity: 1 !important;
        }}

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] label {{
            color: var(--text) !important;
            opacity: 1 !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {{
            color: var(--text) !important;
            font-weight: 800 !important;
            opacity: 1 !important;
        }}

        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stMarkdown p,
        section[data-testid="stSidebar"] .stCaption,
        section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
            color: var(--muted) !important;
            opacity: 1 !important;
        }}

        section[data-testid="stSidebar"] .stCheckbox label,
        section[data-testid="stSidebar"] .stCheckbox label p,
        section[data-testid="stSidebar"] [data-baseweb="checkbox"] label,
        section[data-testid="stSidebar"] [data-baseweb="checkbox"] span {{
            color: var(--text) !important;
            font-weight: 700 !important;
            opacity: 1 !important;
        }}

        section[data-testid="stSidebar"] [data-baseweb="select"] *,
        section[data-testid="stSidebar"] [data-baseweb="input"] *,
        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] textarea {{
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }}

        section[data-testid="stSidebar"] [data-baseweb="select"] svg {{
            fill: #FFFFFF !important;
            color: #FFFFFF !important;
            stroke: #FFFFFF !important;
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
        .soft-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 18px;
            box-shadow: var(--shadow);
            overflow: hidden;
        }}

        div[data-testid="stVerticalBlock"]:has(> .card-strong),
        div[data-testid="stVerticalBlock"]:has(> .card),
        div[data-testid="stVerticalBlock"]:has(> .metric-card),
        div[data-testid="stVerticalBlock"]:has(> .hero) {{
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
            font-size: clamp(1.9rem, 4.6vw, 3.8rem);
            line-height: 1.02;
            letter-spacing: -.035em;
            font-weight: 900;
            margin: 0 auto .7rem auto;
            max-width: 20ch;
            text-wrap: balance;
        }}

        .hero-copy, .section-copy, .card-copy, .metric-note, .rank-meta {{
            color: var(--muted);
            font-size: .92rem;
            line-height: 1.52;
        }}

        .hero-copy {{
            max-width: 36ch;
            margin: 0 auto .9rem auto;
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

        .hero-manjerico-wrap {{
            display: flex;
            justify-content: center;
            margin-top: .15rem;
            margin-bottom: .35rem;
        }}

        .manjerico-shell {{
            width: 260px;
            margin: 0 auto;
            text-align: center;
        }}

        .manjerico-link-reset {{
            text-decoration: none !important;
            color: inherit !important;
            display: inline-block;
        }}

        .manjerico-plant-zone {{
            width: 178px;
            height: 178px;
            margin: 0 auto -8px auto;
            border-radius: 999px;
            background:
                radial-gradient(circle at 30% 30%, #74C365 0 14%, transparent 15%),
                radial-gradient(circle at 68% 28%, #61BC5A 0 13%, transparent 14%),
                radial-gradient(circle at 39% 68%, #2F8737 0 13%, transparent 14%),
                radial-gradient(circle at 70% 69%, #4AAE49 0 13%, transparent 14%),
                radial-gradient(circle at 50% 50%, #4FAF50 0 52%, #2E7D32 100%);
            box-shadow:
                inset 0 10px 18px rgba(255,255,255,.16),
                inset 0 -14px 20px rgba(18,68,22,.18),
                0 18px 30px rgba(92,54,18,.12);
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .manjerico-plant-zone::after {{
            content: "";
            position: absolute;
            inset: 0;
            border-radius: 999px;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,.06);
            pointer-events: none;
        }}

        .manjerico-green-button {{
            position: relative;
            z-index: 3;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 112px;
            padding: .58rem .95rem;
            border-radius: 999px;
            background: linear-gradient(180deg, rgba(123,201,111,.98) 0%, rgba(76,175,80,.98) 45%, rgba(46,125,50,.98) 100%);
            color: var(--green-zone-text);
            border: 1px solid rgba(255,255,255,.22);
            box-shadow:
                0 10px 24px rgba(20,70,24,.24),
                inset 0 1px 0 rgba(255,255,255,.18);
            font-weight: 900;
            letter-spacing: .02em;
            font-size: .88rem;
            line-height: 1;
            cursor: pointer;
            transition: transform .16s ease, filter .16s ease, box-shadow .16s ease;
            user-select: none;
            backdrop-filter: blur(1px);
        }}

        .manjerico-green-button:hover {{
            transform: translateY(-1px) scale(1.02);
            filter: brightness(1.03);
            box-shadow:
                0 14px 28px rgba(20,70,24,.28),
                inset 0 1px 0 rgba(255,255,255,.2);
        }}

        .manjerico-green-button:active {{
            transform: translateY(0) scale(.99);
        }}

        .manjerico-pot {{
            width: 150px;
            height: 92px;
            margin: 0 auto;
            background: linear-gradient(180deg, #DB9462 0%, #C87A48 55%, #A55E34 100%);
            border-radius: 0 0 70px 70px / 0 0 52px 52px;
            border: 1px solid rgba(124,76,39,.35);
            position: relative;
            box-shadow: 0 18px 28px rgba(92,54,18,.12);
        }}

        .manjerico-pot::before {{
            content: "";
            position: absolute;
            left: 50%;
            top: -14px;
            transform: translateX(-50%);
            width: 166px;
            height: 24px;
            background: linear-gradient(180deg, #E3A06E 0%, #C87847 100%);
            border-radius: 999px;
            border: 1px solid rgba(124,76,39,.35);
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

        .rank-place {{
            color: var(--text);
            font-size: .96rem;
            font-weight: 800;
            line-height: 1.28;
            margin-bottom: .12rem;
        }}

        .top-rank-hero {{
            background: linear-gradient(180deg, #FFF4DB 0%, #FFF0D1 100%);
            border: 1px solid #E3B46C;
            border-radius: 18px;
            padding: 1rem;
            margin-top: .75rem;
            margin-bottom: .8rem;
            box-shadow: 0 10px 22px rgba(184, 135, 70, .14);
        }}

        .top-rank-grid {{
            display: grid;
            grid-template-columns: 84px 1fr;
            gap: .85rem;
            align-items: center;
        }}

        .top-rank-badge {{
            width: 84px;
            height: 84px;
            border-radius: 22px;
            background: #C62828;
            color: #FFF7E8;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            box-shadow: 0 10px 24px rgba(198, 40, 40, .22);
        }}

        .top-rank-badge small {{
            font-size: .68rem;
            letter-spacing: .08em;
            text-transform: uppercase;
            font-weight: 800;
            opacity: .9;
        }}

        .top-rank-badge strong {{
            font-size: 2rem;
            line-height: 1;
            font-weight: 900;
        }}

        .top-rank-title {{
            font-size: 1.2rem;
            line-height: 1.12;
            font-weight: 900;
            color: var(--text);
            margin-bottom: .22rem;
        }}

        .day-heat-hero {{
            background: linear-gradient(180deg, #FFF3DE 0%, #FFF7E8 100%);
            border: 1px solid #E8C58A;
        }}

        .day-order-note {{
            color: var(--soft);
            font-size: .78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: .06em;
            margin-bottom: .35rem;
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
                max-width: 18ch;
                font-size: 1.95rem;
                line-height: 1.04;
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

            .manjerico-shell {{
                width: 220px;
            }}

            .manjerico-plant-zone {{
                width: 156px;
                height: 156px;
            }}

            .manjerico-green-button {{
                min-width: 100px;
                font-size: .82rem;
                padding: .52rem .85rem;
            }}

            .manjerico-pot {{
                width: 132px;
                height: 82px;
            }}

            .manjerico-pot::before {{
                width: 148px;
                height: 22px;
            }}

            .top-rank-grid {{
                grid-template-columns: 1fr;
            }}

            .top-rank-badge {{
                width: 72px;
                height: 72px;
            }}

            .hero,
            .metric-card,
            .card,
            .card-strong,
            .soft-card,
            .pick-card {{
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


def abbreviate_label(text: str, max_len: int = 14) -> str:
    text = clean_display_text(text)
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


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


def short_weekday_pt(value: str) -> str:
    v = normalize_artist_name(value)
    mapping = {
        "segunda-feira": "Seg",
        "terca-feira": "Ter",
        "terça-feira": "Ter",
        "quarta-feira": "Qua",
        "quinta-feira": "Qui",
        "sexta-feira": "Sex",
        "sabado": "Sáb",
        "sábado": "Sáb",
        "domingo": "Dom",
    }
    return mapping.get(v, clean_display_text(value)[:3].title())


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


def build_chart_window(df_filtered: pd.DataFrame, anchor_date: pd.Timestamp, max_days: int = 7) -> pd.DataFrame:
    target_dates = pd.date_range(anchor_date, periods=max_days, freq="D")
    chart_df = df_filtered[df_filtered["data"].isin(target_dates)].copy()
    if chart_df.empty:
        fallback_dates = sorted(pd.to_datetime(df_filtered["data"].unique()))[:max_days]
        chart_df = df_filtered[df_filtered["data"].isin(fallback_dates)].copy()
    return chart_df


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
    return grouped.sort_values(["score", "eventos", "atos_unicos"], ascending=[False, False, False]).reset_index(drop=True)


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
        "date": pd.to_datetime(day_df["data"].iloc[0]),
        "day_name": clean_display_text(day_df["dia_semana"].iloc[0]).capitalize(),
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


def build_heat_order_summaries(focus_df: pd.DataFrame, anchor_date: pd.Timestamp) -> List[dict]:
    summaries = []
    for day in sorted(pd.to_datetime(focus_df["data"].unique())):
        day_df = focus_df[focus_df["data"] == day].copy()
        summary = build_day_summary(day_df)
        if summary:
            summary["relative_label"] = relative_label(day, anchor_date)
            summaries.append(summary)

    summaries = sorted(
        summaries,
        key=lambda x: (x["best_score"], x["total"], x["arraiais"]),
        reverse=True,
    )
    return summaries


def build_daily_chart_summary(chart_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for data, g in chart_df.groupby("data"):
        options = summarize_options(g)
        if options.empty:
            continue
        best = options.iloc[0]
        rows.append(
            {
                "data": pd.Timestamp(data),
                "dia_semana": g["dia_semana"].iloc[0],
                "local": best["local"],
                "cabeca_cartaz": best["cabeca_cartaz"],
                "perfil_forca": best["perfil_forca"],
                "score": float(best["score"]),
            }
        )
    return pd.DataFrame(rows).sort_values("data").reset_index(drop=True)


inject_css()

if "show_quadra_dialog" not in st.session_state:
    st.session_state.show_quadra_dialog = False

params = st.query_params
manjerico_action = params.get("manjerico")
if manjerico_action == "open":
    st.session_state.show_quadra_dialog = True
    st.query_params.clear()

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
chart_df = build_chart_window(df_filtered, anchor_date, max_days=7)

focus_dates = sorted(pd.to_datetime(focus_df["data"].unique()))
if not focus_dates:
    st.warning("Não há festa marcada nos próximos dias com estes filtros.")
    st.stop()

day_summaries = build_heat_order_summaries(focus_df, anchor_date)
if not day_summaries:
    st.warning("Não foi possível resumir os dias em destaque.")
    st.stop()

first_summary = day_summaries[0]
top_today = first_summary["options"].head(5).copy()

init_manjerico_quadra(QUADRAS_MANJERICO_RAW)
hero_quadra_atual = get_randomized_hero_quadra(QUADRAS_HERO_RAW)
hero_quadra_html = render_quadra_html(hero_quadra_atual)


@st.dialog("🌿 Quadra do manjerico", width="small")
def open_manjerico_quadra():
    quadra_dialogo = st.session_state.get("manjerico_quadra_text", "")
    quadra_dialogo_html = render_quadra_html(quadra_dialogo)

    st.markdown(
        f"""
        <div style="padding:.25rem .15rem .25rem .15rem;">
            <div style="font-size:.78rem; color:#C62828; font-weight:900; text-transform:uppercase; letter-spacing:.06em; margin-bottom:.6rem;">Bilhete do manjerico</div>
            <div style="background:#F4E24F; border:1px solid #CBB53A; border-radius:16px; padding:1rem .95rem; box-shadow:0 8px 20px rgba(92,54,18,.10);">
                <div style="font-size:.94rem; line-height:1.6; color:#3E2615; font-weight:700;">{quadra_dialogo_html}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Outra quadra", key="next_quadra_dialog"):
            next_manjerico_quadra(QUADRAS_MANJERICO_RAW)
            st.session_state.show_quadra_dialog = True
            st.rerun()

    with col_b:
        if st.button("Fechar", key="close_quadra_dialog"):
            st.session_state.show_quadra_dialog = False
            st.rerun()


if st.session_state.show_quadra_dialog:
    st.session_state.show_quadra_dialog = False
    open_manjerico_quadra()

chart_base = build_daily_chart_summary(chart_df)
chart_base["dia_curto"] = chart_base["dia_semana"].apply(short_weekday_pt)
chart_base["data_curta"] = pd.to_datetime(chart_base["data"]).dt.strftime("%d/%m")
chart_base["artist_label"] = chart_base["cabeca_cartaz"].apply(lambda x: abbreviate_label(x, max_len=14))
chart_base["x_label"] = chart_base["dia_curto"] + " " + chart_base["data_curta"]

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=chart_base["x_label"],
        y=chart_base["score"],
        mode="lines+markers+text",
        text=chart_base["artist_label"],
        textposition="top center",
        textfont=dict(size=11, color=COLORS["text"]),
        line=dict(color=COLORS["accent"], width=3.5, shape="spline", smoothing=0.45),
        marker=dict(
            size=11,
            color=COLORS["accent"],
            line=dict(color=COLORS["surface"], width=2),
        ),
        customdata=chart_base[["local", "cabeca_cartaz", "perfil_forca", "data_curta"]],
        hovertemplate=(
            "<b>%{customdata[3]}</b><br>"
            "Arraial em destaque: %{customdata[0]}<br>"
            "Cabeça de cartaz: %{customdata[1]}<br>"
            "Perfil dominante: %{customdata[2]}<br>"
            "Score: %{y:.1f}/10<br>"
            "<extra></extra>"
        ),
        cliponaxis=False,
    )
)

fig.update_layout(
    paper_bgcolor=COLORS["surface"],
    plot_bgcolor=COLORS["surface"],
    font=dict(color=COLORS["text"], size=12),
    margin=dict(l=18, r=18, t=70, b=18),
    xaxis_title="Dia",
    yaxis_title="Score",
    height=430,
)

fig.update_xaxes(showgrid=False, tickangle=0)
fig.update_yaxes(
    range=[0, 10],
    tickmode="array",
    tickvals=list(range(0, 11, 2)),
    gridcolor="rgba(110,75,42,0.18)",
    zeroline=False,
)

st.markdown('<div class="content-shell">', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="hero">
      <div class="eyebrow">🇵🇹💃🎉 Santos Populares 2026 💃🎉🇵🇹</div>
      <div class="hero-title">Guia Oficial das Festas de Lisboa para o (B)enfica(B)eer(C)lub</div>
      <div class="hero-copy">{hero_quadra_html}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='section-label'>Pensamento do dia</div>"
    "<div class='section-copy'>Clica no manjerico!.</div>",
    unsafe_allow_html=True,
)

manj_left, manj_mid, manj_right = st.columns([1.2, 1, 1.2])
with manj_mid:
    st.markdown(
        """
        <div class="hero-manjerico-wrap">
          <div class="manjerico-shell">
            <a class="manjerico-link-reset" href="?manjerico=open" target="_self">
              <div class="manjerico-plant-zone" role="button" aria-label="Ver quadra do manjerico">
                <span class="manjerico-green-button">Ver quadra</span>
              </div>
            </a>
            <div class="manjerico-pot"></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="section-label">Aquecimento com minis</div><div class="section-copy">Um olhar rápido para entrares no ritmo da festa antes da conversa começar a sair torta.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='metric-grid'>"
    + "".join(
        [
            f"<div class='metric-card'><div class='metric-label'>Janela ativa</div><div class='metric-value'>{len(focus_dates)} dias</div><div class='metric-note'>Festa à vista</div></div>",
            f"<div class='metric-card'><div class='metric-label'>Eventos</div><div class='metric-value'>{len(focus_df)}</div><div class='metric-note'>Momentos em cartaz</div></div>",
            f"<div class='metric-card'><div class='metric-label'>Arraiais</div><div class='metric-value'>{focus_df['local'].nunique()}</div><div class='metric-note'>Arraiais a mexer</div></div>",
            f"<div class='metric-card'><div class='metric-label'>Dia mais quente</div><div class='metric-value'>{format_pt_date(first_summary['date'])}</div><div class='metric-note'>{first_summary['best_local']} · Nota {first_summary['best_score']}/10</div></div>",
        ]
    )
    + "</div>",
    unsafe_allow_html=True,
)

ranking_html = ['<div class="card-strong">']
ranking_html.append(
    '<div class="card-kicker">Pódio da coparia</div><div class="card-copy">A hierarquia é definida pela maior nota individual de notoriedade do dia.</div>'
)

if not top_today.empty:
    top_row = top_today.iloc[0]
    ranking_html.append(
        f"""
        <div class="top-rank-hero">
          <div class="top-rank-grid">
            <div class="top-rank-badge">
              <small>Top</small>
              <strong>1</strong>
            </div>
            <div>
              <div class="top-rank-title">{top_row['local']}</div>
              <div class="card-copy">Cabeça de cartaz: {top_row.get('cabeca_cartaz', 'Cartaz variado')}</div>
              <div style="height:.55rem"></div>
              <span class="chip chip-red">{int(top_row.get('eventos', 0))} eventos</span>
              <span class="chip chip-olive">{top_row.get('perfil_forca', 'Notoriedade')}</span>
              <span class="chip chip-gold">Score {round(float(top_row.get('score', 0)), 1)}/10</span>
            </div>
          </div>
        </div>
        """
    )

    for i, (_, row) in enumerate(top_today.iloc[1:].iterrows(), start=2):
        ranking_html.append(
            f"<div class='rank-row'><div class='rank-place'>{i}. {row['local']}</div><div class='rank-meta'>{row.get('cabeca_cartaz', 'Cartaz variado')} · Score {round(float(row.get('score', 0)), 1)}/10 · {row.get('perfil_forca', 'Notoriedade')}</div></div>"
        )

ranking_html.append("</div>")
st.markdown("".join(ranking_html), unsafe_allow_html=True)

st.markdown('<div class="section-band">', unsafe_allow_html=True)
st.markdown(
    '<div class="section-head"><div class="section-label">Por onde se entorna a noite</div><div class="section-copy">Os dias abaixo já estão ordenados pelo calor do cartaz, não pela ordem cronológica.</div></div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="section-grid-4">', unsafe_allow_html=True)

for idx, summary in enumerate(day_summaries):
    is_top_day = idx == 0
    span = "span-2" if is_top_day else "span-1"
    card_class = "card-strong day-heat-hero" if is_top_day else "card"

    extra_note = "Dia mais forte da janela ativa" if is_top_day else f"{summary['relative_label']} · {summary['mood']}"
    title = f"{format_pt_date(summary['date'])} · {summary['day_name']}"
    copy = f"{summary['total']} entradas distribuídas por {summary['arraiais']} arraiais."

    if is_top_day:
        st.markdown(
            f"""
            <div class="{card_class} {span}">
              <div class="day-order-note">{extra_note}</div>
              <div class="card-kicker">{summary['relative_label']} · {summary['mood']}</div>
              <div class="card-title">{title}</div>
              <div class="card-copy">{copy} O destaque é definido pelo artista mais forte do cartaz, sem somar nomes.</div>
              <div style="height:.75rem"></div>
              <div class="pick-card">
                <div class="card-kicker">Poiso oficial da molha</div>
                <div class="card-title">{summary['best_local']}</div>
                <div class="card-copy">Cabeça de cartaz: {summary['best_headliner']}</div>
              </div>
              <div style="height:.75rem"></div>
              <span class="chip chip-red">{summary['best_events']} eventos</span>
              <span class="chip chip-olive">{summary['best_profile']}</span>
              <span class="chip chip-gold">Score {summary['best_score']}/10</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="{card_class} {span}">
              <div class="card-kicker">{extra_note}</div>
              <div class="card-title">{title}</div>
              <div class="card-copy">{copy}</div>
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

st.markdown(
    '<div class="card-strong"><div class="card-kicker">Nível de bezana</div><div class="card-copy">No máximo aparecem 7 dias, com o cabeça de cartaz de cada dia destacado diretamente no ponto.</div></div>',
    unsafe_allow_html=True,
)
st.plotly_chart(fig, use_container_width=True, theme=None, config={"displayModeBar": False})

st.markdown("</div>", unsafe_allow_html=True)