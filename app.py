import re
from io import BytesIO
from pathlib import Path
from typing import List, Optional, Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st


# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Santos Populares 2026",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded",
)

pio.templates.default = "plotly"


# =========================================================
# THEME
# =========================================================
CHART_SEQ = [
    "#8F2D14",
    "#B45A1B",
    "#C88A3D",
    "#6E7F3B",
    "#2F6F73",
    "#5B4A3F",
]

CHART_SCALE = ["#F3E4D1", "#D7A45B", "#B45A1B", "#8F2D14"]


def inject_css():
    st.markdown(
        """
        <style>
        :root {
            --bg: #f2eee6;
            --card: #ffffff;
            --card-2: #fffaf3;
            --ink: #111111;
            --muted: #3f3f46;
            --soft: #5f5f67;
            --line: #cfc5b6;
            --accent: #8f2d14;
            --accent-2: #b86a1f;
            --shadow: 0 10px 30px rgba(17, 17, 17, 0.08);
            --radius: 18px;
        }

        .stApp {
            background: var(--bg);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }

        .hero-wrap {
            background: #fffaf4;
            border: 1px solid var(--line);
            border-radius: 28px;
            padding: 1.6rem 1.6rem 1.2rem 1.6rem;
            box-shadow: var(--shadow);
            margin-bottom: 1.25rem;
        }

        .eyebrow {
            display: inline-block;
            font-size: 0.82rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--accent);
            font-weight: 800;
            margin-bottom: 0.6rem;
        }

        .hero-title {
            font-size: clamp(1.8rem, 3vw, 3.4rem);
            line-height: 1.05;
            font-weight: 900;
            color: var(--ink);
            margin: 0 0 0.55rem 0;
        }

        .hero-subtitle {
            color: var(--muted);
            font-size: 1.02rem;
            max-width: 78ch;
            margin-bottom: 0.4rem;
            font-weight: 500;
        }

        .section-label {
            font-size: 0.94rem;
            font-weight: 900;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: var(--accent);
            margin: 1rem 0 0.8rem;
        }

        .metric-card {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: 1rem 1rem 0.9rem 1rem;
            min-height: 132px;
        }

        .metric-label {
            color: var(--soft);
            font-size: 0.84rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 800;
            margin-bottom: 0.45rem;
        }

        .metric-value {
            font-size: clamp(1.5rem, 2.3vw, 2.4rem);
            line-height: 1;
            font-weight: 900;
            color: var(--ink);
            margin-bottom: 0.35rem;
        }

        .metric-note {
            color: var(--muted);
            font-size: 0.94rem;
            font-weight: 500;
        }

        .insight-card {
            background: var(--card-2);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 1rem 1rem 0.9rem 1rem;
            height: 100%;
        }

        .insight-title {
            font-size: 0.9rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: var(--accent);
            margin-bottom: 0.35rem;
        }

        .insight-body {
            color: var(--ink);
            font-size: 0.98rem;
            line-height: 1.45;
            font-weight: 500;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 16px;
            overflow: hidden;
            background: #ffffff;
        }

        [data-testid="stDataFrame"] div {
            font-size: 14px !important;
        }

        label, .stSelectbox label, .stDateInput label, .stMultiSelect label {
            color: var(--ink) !important;
            font-weight: 700 !important;
        }

        .stCaption, [data-testid="stCaptionContainer"] {
            color: var(--muted) !important;
        }

        .stAlert {
            color: #111 !important;
        }

        h1, h2, h3, h4, h5, h6, p, li, span, div {
            color: inherit;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_readable_chart_style(fig):
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(color="#111111", size=13),
        title=dict(font=dict(size=20, color="#111111")),
        legend=dict(
            title=dict(font=dict(color="#111111")),
            font=dict(color="#111111"),
            bgcolor="rgba(255,255,255,0.92)"
        ),
        margin=dict(l=20, r=20, t=70, b=20),
    )

    fig.update_xaxes(
        title_font=dict(color="#111111", size=14),
        tickfont=dict(color="#111111", size=12),
        showgrid=True,
        gridcolor="rgba(17,17,17,0.10)",
        zeroline=False,
        linecolor="rgba(17,17,17,0.35)"
    )

    fig.update_yaxes(
        title_font=dict(color="#111111", size=14),
        tickfont=dict(color="#111111", size=12),
        showgrid=True,
        gridcolor="rgba(17,17,17,0.10)",
        zeroline=False,
        linecolor="rgba(17,17,17,0.35)"
    )
    return fig


inject_css()


# =========================================================
# CONSTANTS
# =========================================================
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


# =========================================================
# HELPERS
# =========================================================
def normalize_text(value) -> str:
    if pd.isna(value):
        return ""
    txt = str(value)
    txt = txt.replace("\r", "\n")
    txt = re.sub(r"[ \t]+", " ", txt)
    return txt.strip()


def parse_date_label(label: str) -> Optional[pd.Timestamp]:
    label = normalize_text(label)
    label = label.replace("(Feriado)", "").replace("Feriado", "").strip()

    match = re.search(r"(\d{1,2})\s+de\s+([A-Za-zÀ-ÿ]+)", label, re.IGNORECASE)
    if not match:
        return None

    dia = int(match.group(1))
    mes_nome = match.group(2).capitalize()
    mes = MESES_PT.get(mes_nome)
    if not mes:
        return None

    return pd.Timestamp(year=2026, month=mes, day=dia)


def classify_event(name: str) -> str:
    n = normalize_text(name).lower()

    if any(x in n for x in ["marcha", "marchas"]):
        return "Marchas"
    if any(x in n for x in ["dj", "set", "over the rule", "is hot"]):
        return "DJ / Club"
    if "tributo" in n:
        return "Tributo"
    if any(x in n for x in ["pimba", "barreiros", "rossi", "azevedo", "ruth marlene", "toy", "rosinha"]):
        return "Popular / Pimba"
    if any(x in n for x in ["banda", "show"]):
        return "Concerto"
    if any(x in n for x in ["sagres", "mega santos", "revelar", "rádio 105.4"]):
        return "Ativação / Marca"
    return "Espetáculo"


def split_multiline_cell(value: str) -> List[str]:
    txt = normalize_text(value)
    if not txt or txt in {".", "-", "—"}:
        return []

    lines = [line.strip() for line in txt.split("\n") if line.strip()]
    cleaned = []

    if len(lines) > 1:
        for line in lines:
            line = re.sub(r"^[\-\–\—•]+\s*", "", line).strip()
            if line and line not in {".", "-", "—"}:
                cleaned.append(line)
        return cleaned

    single = re.sub(r"^[\-\–\—•]+\s*", "", txt).strip()
    if not single or single in {".", "-", "—"}:
        return []

    return [single]


def coerce_date_range(date_input_value, min_date, max_date) -> Tuple:
    if isinstance(date_input_value, tuple):
        if len(date_input_value) == 2:
            return date_input_value[0], date_input_value[1]
        if len(date_input_value) == 1:
            return date_input_value[0], date_input_value[0]
        return min_date, max_date
    return date_input_value, date_input_value


# =========================================================
# DATA LOADING
# =========================================================
@st.cache_data(ttl=3600, show_spinner=False)
def load_and_prepare_data(file_bytes: bytes):
    raw = pd.read_excel(BytesIO(file_bytes), header=None, engine="openpyxl")

    header_row = 2
    headers = [normalize_text(x) for x in raw.iloc[header_row].tolist()]
    df = raw.iloc[header_row + 1:].copy()
    df.columns = headers
    df = df.dropna(how="all").copy()

    df = df.rename(columns={
        "Dia": "dia",
        "Dia da Semana": "dia_semana_excel"
    })

    if "dia" not in df.columns or "dia_semana_excel" not in df.columns:
        raise ValueError("Não foi possível localizar as colunas 'Dia' e 'Dia da Semana'.")

    df = df.dropna(axis=1, how="all").copy()
    event_cols = [c for c in df.columns if c not in ["dia", "dia_semana_excel"]]

    long_df = df.melt(
        id_vars=["dia", "dia_semana_excel"],
        value_vars=event_cols,
        var_name="local",
        value_name="conteudo"
    )

    long_df["conteudo"] = long_df["conteudo"].apply(normalize_text)
    long_df = long_df[long_df["conteudo"] != ""].copy()
    long_df = long_df[~long_df["conteudo"].isin([".", "-", "—"])].copy()

    long_df["data"] = long_df["dia"].apply(parse_date_label)
    long_df = long_df.dropna(subset=["data"]).copy()

    records = []
    for _, row in long_df.iterrows():
        entries = split_multiline_cell(row["conteudo"])
        for entry in entries:
            records.append(
                {
                    "data": row["data"],
                    "dia_label": normalize_text(row["dia"]),
                    "dia_semana_excel": normalize_text(row["dia_semana_excel"]),
                    "local": normalize_text(row["local"]),
                    "artista_evento": entry,
                    "conteudo_original": normalize_text(row["conteudo"]),
                }
            )

    events = pd.DataFrame(records)

    if events.empty:
        return events

    events["mes"] = events["data"].dt.month
    events["mes_nome"] = events["data"].dt.strftime("%b")
    events["dia_mes"] = events["data"].dt.day
    events["dia_semana"] = (
        events["data"].dt.day_name().map(DIAS_SEMANA_PT).fillna(events["dia_semana_excel"])
    )
    events["fim_de_semana"] = events["data"].dt.dayofweek >= 4
    events["feriado"] = events["dia_label"].str.contains("Feriado", case=False, na=False)
    events["categoria"] = events["artista_evento"].apply(classify_event)

    counts_by_day = events.groupby("data").size().rename("eventos_no_dia")
    events = events.merge(counts_by_day, on="data", how="left")

    max_events = int(events["eventos_no_dia"].max()) if not events.empty else 0
    if max_events <= 2:
        events["intensidade_dia"] = "Baixa"
    else:
        events["intensidade_dia"] = pd.cut(
            events["eventos_no_dia"],
            bins=[-1, 2, 5, 999],
            labels=["Baixa", "Média", "Alta"]
        ).astype(str)

    return events.sort_values(["data", "local", "artista_evento"]).reset_index(drop=True)


# =========================================================
# HEADER
# =========================================================
st.markdown(
    """
    <div class="hero-wrap">
        <div class="eyebrow">Lisboa + Arredores • Agenda Analítica</div>
        <div class="hero-title">Santos Populares 2026</div>
        <div class="hero-subtitle">
            Criado, com amor, para a malta linda do BBC <3
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# INPUT FILE STRATEGY
# =========================================================
candidate_paths = [
    Path("data/santos.xlsx"),
    Path("santos.xlsx"),
    Path("./data/santos.xlsx"),
]

uploaded_file = None
file_bytes = None

for local_path in candidate_paths:
    if local_path.exists():
        file_bytes = local_path.read_bytes()
        break

if file_bytes is None:
    uploaded_file = st.file_uploader(
        "Carregar ficheiro Excel",
        type=["xlsx"],
        accept_multiple_files=False,
        help="Usa o ficheiro `santos.xlsx` para alimentar o dashboard."
    )
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()

if file_bytes is None:
    st.info("Carrega o ficheiro Excel para visualizar o dashboard.")
    st.stop()


# =========================================================
# PROCESS FILE
# =========================================================
try:
    df = load_and_prepare_data(file_bytes)
except Exception as e:
    st.error("Erro ao ler ou transformar o ficheiro Excel.")
    st.exception(e)
    st.stop()

if df.empty:
    st.error("A extração terminou sem eventos válidos.")
    st.stop()


# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.header("🔎 Filtros")

min_date = df["data"].min().date()
max_date = df["data"].max().date()

date_range = st.sidebar.date_input(
    "Intervalo de datas",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

data_inicio, data_fim = coerce_date_range(date_range, min_date, max_date)

locais = ["Todos"] + sorted(df["local"].dropna().unique().tolist())
categorias = ["Todas"] + sorted(df["categoria"].dropna().unique().tolist())
intensidades = ["Todas"] + sorted(df["intensidade_dia"].dropna().unique().tolist())
artistas = ["Todos"] + sorted(df["artista_evento"].dropna().unique().tolist())

local_sel = st.sidebar.selectbox("Local / Arraial", locais)
categoria_sel = st.sidebar.selectbox("Categoria", categorias)
intensidade_sel = st.sidebar.selectbox("Intensidade do dia", intensidades)
artista_sel = st.sidebar.selectbox("Artista / Evento", artistas)

apenas_feriados = st.sidebar.checkbox("Só feriados")
apenas_fim_de_semana = st.sidebar.checkbox("Só sexta a domingo")

mask = (
    (df["data"] >= pd.Timestamp(data_inicio)) &
    (df["data"] <= pd.Timestamp(data_fim))
)

if local_sel != "Todos":
    mask &= df["local"] == local_sel

if categoria_sel != "Todas":
    mask &= df["categoria"] == categoria_sel

if intensidade_sel != "Todas":
    mask &= df["intensidade_dia"] == intensidade_sel

if artista_sel != "Todos":
    mask &= df["artista_evento"] == artista_sel

if apenas_feriados:
    mask &= df["feriado"]

if apenas_fim_de_semana:
    mask &= df["data"].dt.dayofweek >= 4

df_filtered = df.loc[mask].copy()

if df_filtered.empty:
    st.warning("Os filtros atuais não devolvem resultados.")
    st.stop()


# =========================================================
# KPIS
# =========================================================
total_eventos = len(df_filtered)
locais_ativos = df_filtered["local"].nunique()
artistas_unicos = df_filtered["artista_evento"].nunique()

dia_top_counts = df_filtered.groupby("data").size().sort_values(ascending=False)
dia_top = dia_top_counts.index[0] if not dia_top_counts.empty else None
dia_top_qtd = int(dia_top_counts.iloc[0]) if not dia_top_counts.empty else 0

local_top_counts = df_filtered.groupby("local").size().sort_values(ascending=False)
local_top = local_top_counts.index[0] if not local_top_counts.empty else "—"
local_top_qtd = int(local_top_counts.iloc[0]) if not local_top_counts.empty else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Eventos visíveis</div>
        <div class="metric-value">{total_eventos}</div>
        <div class="metric-note">Linhas após limpeza e filtros.</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Locais ativos</div>
        <div class="metric-value">{locais_ativos}</div>
        <div class="metric-note">Arraiais com programação no recorte atual.</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Artistas / atos</div>
        <div class="metric-value">{artistas_unicos}</div>
        <div class="metric-note">Entradas únicas identificadas.</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    dia_top_txt = dia_top.strftime("%d %b") if dia_top is not None else "—"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Pico diário</div>
        <div class="metric-value">{dia_top_qtd}</div>
        <div class="metric-note">{dia_top_txt} • dia com maior densidade.</div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# INSIGHTS
# =========================================================
i1, i2, i3 = st.columns(3)

with i1:
    texto = (
        f"O dia mais carregado no recorte atual é <b>{dia_top.strftime('%d/%m/%Y')}</b> com <b>{dia_top_qtd}</b> eventos."
        if dia_top is not None else "Sem dia dominante no recorte atual."
    )
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Pressão do calendário</div>
        <div class="insight-body">{texto}</div>
    </div>
    """, unsafe_allow_html=True)

with i2:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Local dominante</div>
        <div class="insight-body"><b>{local_top}</b> concentra <b>{local_top_qtd}</b> entradas no recorte atual.</div>
    </div>
    """, unsafe_allow_html=True)

with i3:
    feriados = int(df_filtered["feriado"].sum())
    fins = int(df_filtered["fim_de_semana"].sum())
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Ritmo festivo</div>
        <div class="insight-body">Há <b>{feriados}</b> eventos em dias marcados como feriado e <b>{fins}</b> entradas entre sexta e domingo.</div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# SECTION 1
# =========================================================
st.markdown('<div class="section-label">Distribuição temporal</div>', unsafe_allow_html=True)

col_a, col_b = st.columns([1.1, 1])

with col_a:
    heat = (
        df_filtered
        .assign(mes_nome=df_filtered["data"].dt.strftime("%b"))
        .pivot_table(index="dia_mes", columns="mes_nome", values="local", aggfunc="count", fill_value=0)
    )

    ordem_meses = ["May", "Jun"]
    heat = heat.reindex(columns=[m for m in ordem_meses if m in heat.columns], fill_value=0)

    if heat.empty:
        st.info("Sem dados suficientes para desenhar o mapa de calor.")
    else:
        fig_heat = go.Figure(
            data=go.Heatmap(
                z=heat.values,
                x=heat.columns.tolist(),
                y=heat.index.tolist(),
                colorscale=[
                    [0.0, "#F7EFE2"],
                    [0.25, "#E6C48D"],
                    [0.5, "#D7A45B"],
                    [0.75, "#B45A1B"],
                    [1.0, "#8F2D14"],
                ],
                zmin=0,
                zmax=max(1, int(heat.values.max())),
                hovertemplate="Dia %{y}<br>Mês %{x}<br>%{z} eventos<extra></extra>",
                colorbar=dict(title="Eventos"),
            )
        )
        fig_heat.update_layout(
            title="Mapa de calor diário",
            xaxis_title="Mês",
            yaxis_title="Dia do mês",
            yaxis=dict(autorange="reversed"),
        )
        fig_heat = apply_readable_chart_style(fig_heat)
        st.plotly_chart(fig_heat, use_container_width=True, theme=None)

with col_b:
    daily_series = (
        df_filtered.groupby("data")
        .size()
        .reset_index(name="eventos")
        .sort_values("data")
    )

    fig_daily = px.area(
        daily_series,
        x="data",
        y="eventos",
        markers=True,
        title="Cadência de eventos por dia",
    )
    fig_daily.update_traces(
        line=dict(color="#8F2D14", width=3),
        marker=dict(color="#B45A1B", size=7),
        fillcolor="rgba(180,90,27,0.28)",
    )
    fig_daily.update_layout(
        xaxis_title="Data",
        yaxis_title="Eventos",
    )
    fig_daily = apply_readable_chart_style(fig_daily)
    st.plotly_chart(fig_daily, use_container_width=True, theme=None)


# =========================================================
# SECTION 2
# =========================================================
st.markdown('<div class="section-label">Locais e perfis de programação</div>', unsafe_allow_html=True)

col_c, col_d = st.columns(2)

with col_c:
    by_local = (
        df_filtered.groupby("local")
        .size()
        .reset_index(name="eventos")
        .sort_values("eventos", ascending=True)
    )

    fig_local = px.bar(
        by_local,
        x="eventos",
        y="local",
        orientation="h",
        title="Ranking de arraiais",
        color="eventos",
        color_continuous_scale=CHART_SCALE,
    )
    fig_local.update_layout(
        xaxis_title="Nº de eventos",
        yaxis_title="Local",
        coloraxis_showscale=False,
    )
    fig_local = apply_readable_chart_style(fig_local)
    st.plotly_chart(fig_local, use_container_width=True, theme=None)

with col_d:
    by_cat = (
        df_filtered.groupby("categoria")
        .size()
        .reset_index(name="eventos")
        .sort_values("eventos", ascending=False)
    )

    fig_cat = px.pie(
        by_cat,
        values="eventos",
        names="categoria",
        hole=0.55,
        title="Composição por categoria",
        color_discrete_sequence=CHART_SEQ,
    )
    fig_cat.update_traces(
        textposition="inside",
        textinfo="percent+label",
        textfont=dict(color="#111111", size=12),
        marker=dict(line=dict(color="#ffffff", width=1.5))
    )
    fig_cat = apply_readable_chart_style(fig_cat)
    st.plotly_chart(fig_cat, use_container_width=True, theme=None)


# =========================================================
# SECTION 3
# =========================================================
st.markdown('<div class="section-label">Movimento ao longo do calendário</div>', unsafe_allow_html=True)

col_e, col_f = st.columns([1.2, 0.8])

with col_e:
    timeline = df_filtered.copy()

    fig_timeline = px.scatter(
        timeline,
        x="data",
        y="local",
        color="categoria",
        hover_data=["artista_evento", "dia_semana"],
        title="Timeline de programação",
        color_discrete_sequence=CHART_SEQ,
    )
    fig_timeline.update_traces(
        marker=dict(
            size=14,
            opacity=0.82,
            line=dict(width=1, color="rgba(17,17,17,0.35)")
        )
    )
    fig_timeline.update_layout(
        xaxis_title="Data",
        yaxis_title="Local",
        legend_title="Categoria",
    )
    fig_timeline = apply_readable_chart_style(fig_timeline)
    st.plotly_chart(fig_timeline, use_container_width=True, theme=None)

with col_f:
    ordem_dias = [
        "segunda-feira", "terça-feira", "quarta-feira",
        "quinta-feira", "sexta-feira", "sábado", "domingo"
    ]

    dow = (
        df_filtered.groupby("dia_semana")
        .size()
        .reindex(ordem_dias, fill_value=0)
        .reset_index(name="eventos")
        .rename(columns={"dia_semana": "dia"})
    )

    fig_dow = px.bar(
        dow,
        x="dia",
        y="eventos",
        title="Eventos por dia da semana",
        color="eventos",
        color_continuous_scale=CHART_SCALE,
    )
    fig_dow.update_layout(
        xaxis_title="Dia da semana",
        yaxis_title="Eventos",
        coloraxis_showscale=False,
    )
    fig_dow = apply_readable_chart_style(fig_dow)
    st.plotly_chart(fig_dow, use_container_width=True, theme=None)


# =========================================================
# SECTION 4
# =========================================================
st.markdown('<div class="section-label">Nomes mais recorrentes</div>', unsafe_allow_html=True)

top_artists = (
    df_filtered.groupby("artista_evento")
    .size()
    .reset_index(name="ocorrencias")
    .sort_values("ocorrencias", ascending=False)
    .head(15)
)

fig_artists = px.bar(
    top_artists,
    x="ocorrencias",
    y="artista_evento",
    orientation="h",
    title="Top 15 artistas / entradas",
    color="ocorrencias",
    color_continuous_scale=CHART_SCALE,
)
fig_artists.update_layout(
    yaxis=dict(categoryorder="total ascending"),
    xaxis_title="Ocorrências",
    yaxis_title="Artista / evento",
    coloraxis_showscale=False,
)
fig_artists = apply_readable_chart_style(fig_artists)
st.plotly_chart(fig_artists, use_container_width=True, theme=None)


# =========================================================
# ROUTE
# =========================================================
st.markdown('<div class="section-label">Sugestões de rota</div>', unsafe_allow_html=True)

rota = (
    df_filtered.groupby(["data", "local"])
    .size()
    .reset_index(name="eventos")
    .sort_values(["data", "eventos"], ascending=[True, False])
    .groupby("data")
    .head(1)
    .sort_values("data")
)

if not rota.empty:
    rota_view = rota.copy()
    rota_view["data"] = rota_view["data"].dt.strftime("%d/%m/%Y")
    rota_view = rota_view.rename(columns={
        "data": "Data",
        "local": "Local sugerido",
        "eventos": "Volume"
    })
    st.dataframe(rota_view, use_container_width=True, hide_index=True)
else:
    st.info("Sem dados suficientes para gerar uma rota sugerida.")


# =========================================================
# TABLE
# =========================================================
st.markdown('<div class="section-label">Detalhe dos eventos</div>', unsafe_allow_html=True)

table_view = (
    df_filtered[
        ["data", "dia_semana", "local", "artista_evento", "categoria", "feriado", "fim_de_semana", "eventos_no_dia"]
    ]
    .rename(columns={
        "data": "Data",
        "dia_semana": "Dia da semana",
        "local": "Local",
        "artista_evento": "Artista / Evento",
        "categoria": "Categoria",
        "feriado": "Feriado",
        "fim_de_semana": "Fim de semana",
        "eventos_no_dia": "Eventos no dia",
    })
    .copy()
)

table_view["Data"] = pd.to_datetime(table_view["Data"]).dt.strftime("%d/%m/%Y")

st.dataframe(table_view, use_container_width=True, hide_index=True)

csv = table_view.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "⬇️ Exportar tabela filtrada (CSV)",
    data=csv,
    file_name="santos_populares_2026_filtrado.csv",
    mime="text/csv",
)