

import pandas as pd
import plotly.io as pio
import streamlit as st



from charts import build_festival_chart
from components import (
    MANJERICO_HTML,
    day_card,
    hero,
    manjerico_dialog_html,
    metric_grid,
    ranking,
    section,
    vote_leaderboard_html,
)
from config import PAGE_TITLE
from data import (
    build_daily_chart_summary,
    build_heat_order_summaries,
    get_anchor_date,
    load_and_prepare_data,
    read_local_xlsx,
    slice_date_window,
)
from quadras import get_hero_quadra, init_manjerico_quadra, next_manjerico_quadra, render_quadra_html
from styles import inject_css
from text_utils import coerce_date_range
from votes import cast_vote, clear_vote, get_user_vote, get_vote_counts, get_vote_leaderboard, total_votes

st.set_page_config(page_title=PAGE_TITLE, page_icon="🎈", layout="wide", initial_sidebar_state="expanded")
pio.templates.default = "plotly_white"
inject_css()

if st.query_params.get("manjerico") == "open":
    st.session_state.show_quadra_dialog = True
    st.query_params.clear()

if "show_quadra_dialog" not in st.session_state:
    st.session_state.show_quadra_dialog = False

file_bytes = read_local_xlsx()
if file_bytes is None:
    uploaded = st.file_uploader("Carregar ficheiro Excel", type=["xlsx"])
    file_bytes = uploaded.getvalue() if uploaded else None

if file_bytes is None:
    st.info("Carrega o Excel para pôr a festa a mexer.")
    st.stop()

try:
    df = load_and_prepare_data(file_bytes)
except Exception as exc:
    st.error("Houve um tropeção a abrir o ficheiro Excel.")
    st.exception(exc)
    st.stop()

if df.empty:
    st.error("Não encontrei arraiais válidos neste ficheiro.")
    st.stop()

st.sidebar.header("Filtros")
min_date, max_date = df["data"].min().date(), df["data"].max().date()
anchor_default = get_anchor_date(df)
default_end = min((anchor_default + pd.Timedelta(days=6)).date(), max_date)

date_range = st.sidebar.date_input(
    "Intervalo", value=(anchor_default.date(), default_end), min_value=min_date, max_value=max_date
)
data_inicio, data_fim = coerce_date_range(date_range, min_date, max_date)

local_sel = st.sidebar.selectbox("Local", ["Todos"] + sorted(df["local"].dropna().unique()))
categoria_sel = st.sidebar.selectbox("Categoria", ["Todas"] + sorted(df["categoria"].dropna().unique()))
weekend_only = st.sidebar.checkbox("Só sexta a domingo")

mask = (df["data"] >= pd.Timestamp(data_inicio)) & (df["data"] <= pd.Timestamp(data_fim))
if local_sel != "Todos":
    mask &= df["local"] == local_sel
if categoria_sel != "Todas":
    mask &= df["categoria"] == categoria_sel
if weekend_only:
    mask &= df["data"].dt.dayofweek >= 4

df_filtered = df.loc[mask]
if df_filtered.empty:
    st.warning("Com estes filtros, a festa ficou vazia.")
    st.stop()

anchor_date = get_anchor_date(df_filtered)
focus_df = slice_date_window(df_filtered, anchor_date, 3)
chart_df = slice_date_window(df_filtered, anchor_date, 7)
focus_dates = sorted(pd.to_datetime(focus_df["data"].unique()))

if not focus_dates:
    st.warning("Não há festa marcada nos próximos dias com estes filtros.")
    st.stop()

day_summaries = build_heat_order_summaries(focus_df, anchor_date)
if not day_summaries:
    st.warning("Não foi possível resumir os dias em destaque.")
    st.stop()

init_manjerico_quadra()
hero_html = render_quadra_html(get_hero_quadra())
fig = build_festival_chart(build_daily_chart_summary(chart_df))
hot_day = day_summaries[0]
vote_counts = get_vote_counts()
user_vote = get_user_vote()
arraiais_opcoes = sorted(df_filtered["local"].dropna().unique())


@st.dialog("🌿 Quadra do manjerico", width="small")
def manjerico_dialog() -> None:
    st.markdown(manjerico_dialog_html(render_quadra_html(st.session_state.get("manjerico_quadra", ""))), unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    if col_a.button("Outra quadra", key="next_quadra_dialog"):
        next_manjerico_quadra()
        st.session_state.show_quadra_dialog = True
        st.rerun()
    if col_b.button("Fechar", key="close_quadra_dialog"):
        st.session_state.show_quadra_dialog = False
        st.rerun()


if st.session_state.show_quadra_dialog:
    st.session_state.show_quadra_dialog = False
    manjerico_dialog()

day_cards_html = "".join(
    day_card(summary, featured=idx == 0, vote_counts=vote_counts)
    for idx, summary in enumerate(day_summaries)
)

st.markdown(
    '<div class="content-shell">'
    + hero(hero_html)
    + section("O melhor fica para o fim", "Antes de fechares o roteiro, passa pelo manjerico e abre a tua quadra do dia."),
    unsafe_allow_html=True,
)

_, manj_col, _ = st.columns([1.2, 1, 1.2])
manj_col.markdown(MANJERICO_HTML, unsafe_allow_html=True)

st.markdown(
    section("Entrada a matar", "Um olhar rápido para entrares no ritmo da festa sem perder tempo.")
    + metric_grid(len(focus_dates), len(focus_df), focus_df["local"].nunique(), hot_day)
    + ranking(hot_day["options"].head(5), vote_counts),
    unsafe_allow_html=True,
)

st.markdown(section("Vota no teu arraial", "Escolhe o arraial onde preferes ir. Cada pessoa tem um voto — podes mudar quando quiseres."), unsafe_allow_html=True)

with st.container(border=True):
    vote_index = arraiais_opcoes.index(user_vote) if user_vote in arraiais_opcoes else 0
    escolha = st.selectbox("Arraial preferido", arraiais_opcoes, index=vote_index)
    btn_a, btn_b = st.columns(2)
    if btn_a.button("Confirmar voto", type="primary", use_container_width=True):
        cast_vote(escolha)
        st.toast(f"Voto registado em {escolha}!")
        st.rerun()
    if btn_b.button("Retirar voto", use_container_width=True, disabled=user_vote is None):
        clear_vote()
        st.toast("Voto retirado.")
        st.rerun()
    if user_vote:
        st.markdown(f"<span class='vote-user-pill'>O teu voto: {user_vote}</span>", unsafe_allow_html=True)

    st.markdown("<div class='vote-section-divider'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='card-kicker'>Ranking da comunidade</div>"
        f"<div class='card-copy'>{total_votes()} voto{'s' if total_votes() != 1 else ''} no total.</div>"
        + vote_leaderboard_html(get_vote_leaderboard(8)),
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="section-band"><div class="section-head">'
    + section("Onde começa a festa", "Os dias abaixo já estão ordenados pelo calor do cartaz, não pela ordem cronológica.")
    + f'<div class="section-grid-4">{day_cards_html}</div></div>'
    + '<div class="card-strong"><div class="card-kicker">Termómetro da festa</div>'
    '<div class="card-copy">No máximo aparecem 7 dias, com o cabeça de cartaz de cada dia destacado diretamente no ponto.</div></div>'
    "</div>",
    unsafe_allow_html=True,
)
st.plotly_chart(fig, use_container_width=True, theme=None, config={"displayModeBar": False})
