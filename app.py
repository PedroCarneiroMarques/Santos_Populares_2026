import re
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Santos Populares 2026 — Lisboa",
    page_icon="🎊",
    layout="wide",
    initial_sidebar_state="expanded",
)

PALETTE = {
    "bg": "#F3EFE7",
    "surface": "#FFFFFF",
    "text": "#111827",
    "muted": "#4B5563",
    "line": "rgba(17,24,39,0.12)",
    "primary": "#0F766E",
    "secondary": "#B45309",
    "accent": "#1D4ED8",
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@600;700&family=Inter:wght@400;500;600;700;800&display=swap');

:root {{
    --bg: {PALETTE['bg']};
    --card: {PALETTE['surface']};
    --ink: {PALETTE['text']};
    --muted: {PALETTE['muted']};
    --line: {PALETTE['line']};
    --primary: {PALETTE['primary']};
    --secondary: {PALETTE['secondary']};
    --accent: {PALETTE['accent']};
    --shadow: 0 10px 28px rgba(17,24,39,0.06);
    --radius-xl: 28px;
    --radius-lg: 22px;
    --radius-md: 18px;
}}

.stApp {{
    background: var(--bg);
    color: var(--ink);
}}

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

h1, h2, h3 {{
    font-family: 'Source Serif 4', serif;
    color: var(--ink);
    letter-spacing: -0.02em;
}}

.block-container {{
    max-width: 1450px;
    padding-top: 1.8rem;
    padding-bottom: 2rem;
}}

[data-testid="stSidebar"] {{
    background: #FFFFFF;
    border-right: 1px solid var(--line);
}}

[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {{
    color: var(--ink);
}}

[data-testid="stSidebar"] [data-baseweb="select"] * {{
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}}

[data-testid="stSidebar"] [data-baseweb="select"] > div {{
    background: #111827 !important;
    border-radius: 20px !important;
    border: none !important;
}}

[data-testid="stSidebar"] input {{
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}}

[data-testid="stSidebar"] [data-baseweb="input"] input {{
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}}

[data-testid="stSidebar"] svg {{
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}}

.hero,
.metric-card,
.info-box,
.chart-shell {{
    background: var(--card);
    border: 1px solid var(--line);
    box-shadow: var(--shadow);
}}

.hero {{
    border-radius: var(--radius-xl);
    padding: 1.4rem;
    margin-bottom: 1rem;
}}

.hero-kicker {{
    display: inline-block;
    margin-bottom: 0.6rem;
    color: var(--primary);
    font-size: 0.8rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}}

.hero-title {{
    margin: 0;
    font-size: clamp(2.1rem, 3vw, 3.8rem);
    line-height: 0.98;
}}

.hero-subtitle {{
    color: var(--muted);
    margin-top: 0.55rem;
    font-size: 1rem;
    max-width: 68ch;
}}

.badges {{
    margin-top: 1rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem;
}}

.badge {{
    background: #FFFFFF;
    border: 1px solid var(--line);
    color: var(--ink);
    border-radius: 999px;
    padding: 0.45rem 0.75rem;
    font-size: 0.88rem;
    font-weight: 600;
}}

.metric-card {{
    border-radius: var(--radius-lg);
    padding: 1rem;
    min-height: 155px;
}}

.metric-label {{
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.78rem;
    font-weight: 800;
}}

.metric-value {{
    color: var(--ink);
    font-weight: 800;
    font-size: clamp(1.9rem, 2.3vw, 3rem);
    line-height: 1.0;
    margin-top: 0.35rem;
}}

.metric-foot {{
    color: var(--muted);
    margin-top: 0.45rem;
    font-size: 0.92rem;
}}

.info-box {{
    border-radius: var(--radius-md);
    padding: 0.95rem 1rem;
    color: var(--ink);
    margin-top: 0.85rem;
}}

.chart-shell {{
    border-radius: var(--radius-lg);
    padding: 0.9rem 0.95rem 0.35rem 0.95rem;
    margin-bottom: 1rem;
}}

.chart-title {{
    color: var(--ink);
    font-size: 1.35rem;
    font-weight: 800;
    line-height: 1.1;
    margin: 0 0 0.4rem 0;
}}

div[data-testid="stDataFrame"] {{
    border: 1px solid var(--line);
    border-radius: 18px;
    overflow: hidden;
    background: white;
}}

.stDownloadButton > button,
.stButton > button {{
    background: var(--ink);
    color: white;
    border: none;
    border-radius: 999px;
    padding: 0.68rem 1rem;
    font-weight: 700;
}}

.stDownloadButton > button:hover,
.stButton > button:hover {{
    background: #000000;
}}

</style>
""", unsafe_allow_html=True)

MONTHS_PT = {
    "janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4,
    "maio": 5, "junho": 6, "julho": 7, "agosto": 8, "setembro": 9,
    "outubro": 10, "novembro": 11, "dezembro": 12,
}
DAY_ORDER = [
    "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
    "sexta-feira", "sábado", "domingo"
]
MONTH_LABELS = {5: "Maio", 6: "Junho"}


def normalize_text(x):
    if pd.isna(x):
        return pd.NA
    s = str(x).replace("\r", "\n").strip()
    s = re.sub(r"[ \t]+", " ", s)
    return s if s else pd.NA


def parse_pt_date(text):
    if pd.isna(text):
        return pd.NaT
    s = str(text).strip().lower()
    s = re.sub(r"\(.*?\)", "", s).strip()
    m = re.search(r"(\d{1,2})\s+de\s+([a-zçãé]+)", s)
    if not m:
        return pd.NaT
    day = int(m.group(1))
    month = MONTHS_PT.get(m.group(2))
    if not month:
        return pd.NaT
    return pd.Timestamp(year=2026, month=month, day=day)


def clean_local_name(s):
    s = str(s).strip().replace("Maritímo", "Marítimo")
    return re.sub(r"\s+", " ", s)


def split_multiline_events(value):
    if pd.isna(value):
        return []
    txt = str(value).replace("\r", "\n")
    parts = []
    for line in txt.split("\n"):
        line = line.strip().strip("-").strip()
        if not line or line in {".", "-"}:
            continue
        parts.append(line)
    return parts


def classify_entry(name):
    txt = str(name).strip().lower()
    keys = [
        "marchas", "tributo", "show", "dj", "set", "grande noite",
        "sagres", "sons ", "rádio", "radio", "revelar", "pimbamix"
    ]
    return "Especial" if any(k in txt for k in keys) else "Concerto"


def intensity_label(events_count):
    if events_count >= 4:
        return "Muito alta"
    if events_count == 3:
        return "Alta"
    if events_count == 2:
        return "Média"
    return "Pontual"


def apply_clean_theme(fig):
    fig.update_layout(
        paper_bgcolor=PALETTE["surface"],
        plot_bgcolor=PALETTE["surface"],
        font=dict(family="Inter, sans-serif", color=PALETTE["text"], size=14),
        margin=dict(l=28, r=28, t=34, b=52),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=13, color=PALETTE["text"]),
            bgcolor="rgba(255,255,255,0.96)",
            bordercolor="rgba(17,24,39,0.10)",
            borderwidth=1,
        ),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor=PALETTE["line"],
        zeroline=False,
        title_font=dict(size=14, color=PALETTE["muted"]),
        tickfont=dict(size=12, color=PALETTE["text"]),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=PALETTE["line"],
        zeroline=False,
        title_font=dict(size=14, color=PALETTE["muted"]),
        tickfont=dict(size=12, color=PALETTE["text"]),
    )
    return fig


def metric_card(label, value, foot):
    st.markdown(
        f"""
        <div class='metric-card'>
            <div class='metric-label'>{label}</div>
            <div class='metric-value'>{value}</div>
            <div class='metric-foot'>{foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_box_open(title):
    st.markdown(f"<div class='chart-shell'><div class='chart-title'>{title}</div>", unsafe_allow_html=True)


def chart_box_close():
    st.markdown("</div>", unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def load_data():
    raw = pd.read_excel("data/santos.xlsx", header=None)
    header_idx = raw.index[raw.iloc[:, 0].astype(str).str.strip().eq("Dia")][0]
    df = raw.iloc[header_idx:].copy()
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)
    df = df.rename(columns={"Dia": "dia_raw", "Dia da Semana": "dia_semana"})
    df = df.dropna(axis=1, how="all")

    for col in df.columns:
        df[col] = df[col].apply(normalize_text)

    df["data"] = df["dia_raw"].apply(parse_pt_date)
    df["mes"] = df["data"].dt.month
    df["dia_mes"] = df["data"].dt.day

    id_cols = ["dia_raw", "dia_semana", "data", "mes", "dia_mes"]
    local_cols = [c for c in df.columns if c not in id_cols]

    long_df = df.melt(id_vars=id_cols, value_vars=local_cols, var_name="local", value_name="evento_raw")
    long_df["local"] = long_df["local"].apply(clean_local_name)
    long_df["evento_raw"] = long_df["evento_raw"].replace(["", ".", "-", "nan", "None"], pd.NA)
    long_df = long_df.dropna(subset=["evento_raw", "data"]).copy()

    long_df["evento_lista"] = long_df["evento_raw"].apply(split_multiline_events)
    long_df = long_df.explode("evento_lista").copy()
    long_df["evento_lista"] = long_df["evento_lista"].apply(normalize_text)
    long_df = long_df.dropna(subset=["evento_lista"])

    long_df["artista"] = long_df["evento_lista"]
    long_df["tipo_evento"] = long_df["artista"].apply(classify_entry)
    long_df["local_curto"] = long_df["local"].str.replace(r"\s*\(.*?\)", "", regex=True)
    long_df["feriado"] = long_df["dia_raw"].astype(str).str.contains("Feriado", case=False, na=False)
    long_df["fim_semana"] = long_df["dia_semana"].isin(["sábado", "domingo"])
    long_df["contexto"] = np.where(long_df["feriado"], "Feriado", np.where(long_df["fim_semana"], "Fim de semana", "Semana"))

    per_day = long_df.groupby("data").size().reset_index(name="n_eventos_dia")
    per_day["intensidade"] = per_day["n_eventos_dia"].apply(intensity_label)
    long_df = long_df.merge(per_day, on="data", how="left")

    return long_df.sort_values(["data", "local", "artista"]).reset_index(drop=True)


df = load_data()
if df.empty:
    st.error("Não foi possível ler eventos do ficheiro santos.xlsx.")
    st.stop()

headliners = ", ".join(df["artista"].value_counts().head(5).index.tolist())
start_date = df["data"].min().strftime("%d/%m")
end_date = df["data"].max().strftime("%d/%m")

st.markdown(
    f"""
    <div class='hero'>
        <div class='hero-kicker'>Santos Populares 2026 · Lisboa e arredores</div>
        <h1 class='hero-title'>Dashboard Santos Populares 2026</h1>
        <div class='hero-subtitle'>Versão simplificada com contraste forte, leitura limpa e uma paleta curta e coerente para filtros, métricas e gráficos.</div>
        <div class='badges'>
            <div class='badge'>{len(df)} eventos modelados</div>
            <div class='badge'>{df['local_curto'].nunique()} locais</div>
            <div class='badge'>Período {start_date}–{end_date}</div>
            <div class='badge'>Destaques: {headliners}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("## Filtros")
st.sidebar.markdown("### Intervalo")

data_inicio = st.sidebar.date_input(
    "Data início",
    value=df["data"].min().date(),
    min_value=df["data"].min().date(),
    max_value=df["data"].max().date(),
    key="data_inicio",
)

data_fim = st.sidebar.date_input(
    "Data fim",
    value=df["data"].max().date(),
    min_value=df["data"].min().date(),
    max_value=df["data"].max().date(),
    key="data_fim",
)

if data_inicio > data_fim:
    st.sidebar.error("A data de início não pode ser posterior à data de fim.")
    st.stop()

selected_local = st.sidebar.selectbox("Local", ["Todos"] + sorted(df["local_curto"].dropna().unique().tolist()))
selected_artist = st.sidebar.selectbox("Artista / momento", ["Todos"] + sorted(df["artista"].dropna().unique().tolist()))
selected_type = st.sidebar.selectbox("Categoria", ["Todos"] + sorted(df["tipo_evento"].dropna().unique().tolist()))
selected_intensity = st.sidebar.selectbox("Intensidade", ["Todas"] + sorted(df["intensidade"].dropna().unique().tolist()))
only_holiday = st.sidebar.checkbox("Só feriados")
only_weekend = st.sidebar.checkbox("Só fins de semana")

mask = (df["data"] >= pd.Timestamp(data_inicio)) & (df["data"] <= pd.Timestamp(data_fim))
if selected_local != "Todos":
    mask &= df["local_curto"] == selected_local
if selected_artist != "Todos":
    mask &= df["artista"] == selected_artist
if selected_type != "Todos":
    mask &= df["tipo_evento"] == selected_type
if selected_intensity != "Todas":
    mask &= df["intensidade"] == selected_intensity
if only_holiday:
    mask &= df["feriado"]
if only_weekend:
    mask &= df["fim_semana"]

fdf = df[mask].copy()
if fdf.empty:
    st.warning("Sem resultados para os filtros escolhidos.")
    st.stop()

peak_day = fdf.groupby("data").size().sort_values(ascending=False).head(1)
peak_local = fdf["local_curto"].value_counts().head(1)

st.sidebar.markdown("---")
st.sidebar.markdown("### Resumo")
st.sidebar.markdown(f"- Dia mais forte: **{peak_day.index[0].strftime('%d/%m')}** ({int(peak_day.iloc[0])} eventos)")
st.sidebar.markdown(f"- Local dominante: **{peak_local.index[0]}** ({int(peak_local.iloc[0])} eventos)")
st.sidebar.markdown(f"- Artistas/eventos distintos: **{fdf['artista'].nunique()}**")

m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card("Eventos", f"{len(fdf):,}".replace(",", "."), "Linhas visíveis no recorte atual")
with m2:
    metric_card("Locais", fdf["local_curto"].nunique(), "Arraiais com atividade")
with m3:
    metric_card("Artistas", fdf["artista"].nunique(), "Nomes ou momentos únicos")
with m4:
    metric_card("Pico diário", int(fdf.groupby("data").size().max()), "Máximo de eventos num único dia")

b1, b2 = st.columns(2)
with b1:
    top3 = fdf.groupby("data").size().sort_values(ascending=False).head(3)
    txt = " · ".join([f"{idx.strftime('%d/%m')} ({int(val)})" for idx, val in top3.items()])
    st.markdown(f"<div class='info-box'><strong>Noites mais fortes:</strong> {txt}</div>", unsafe_allow_html=True)
with b2:
    share = fdf["tipo_evento"].value_counts(normalize=True).mul(100).round(1)
    txt = " · ".join([f"{k}: {v}%" for k, v in share.items()])
    st.markdown(f"<div class='info-box'><strong>Mix da programação:</strong> {txt}</div>", unsafe_allow_html=True)

st.markdown("## Calendário e pulso diário")
c1, c2 = st.columns(2)

with c1:
    chart_box_open("Mapa de calor por dia")
    base_days = pd.DataFrame({"data": pd.date_range(fdf["data"].min(), fdf["data"].max(), freq="D")})
    base_days["mes"] = base_days["data"].dt.month
    base_days["dia_mes"] = base_days["data"].dt.day
    per_day = fdf.groupby(["mes", "dia_mes"]).size().reset_index(name="eventos")
    cal = base_days.merge(per_day, on=["mes", "dia_mes"], how="left").fillna({"eventos": 0})
    heat = cal.pivot(index="dia_mes", columns="mes", values="eventos").fillna(0)

    fig_heat = go.Figure(go.Heatmap(
        z=heat.values,
        x=[MONTH_LABELS.get(c, str(c)) for c in heat.columns],
        y=heat.index,
        colorscale=[[0.0, "#F8FAFC"], [0.35, "#93C5FD"], [0.65, PALETTE["accent"]], [1.0, PALETTE["text"]]],
        colorbar=dict(
            title="Eventos",
            tickfont=dict(color=PALETTE["text"], size=12),
            titlefont=dict(color=PALETTE["text"], size=13)
        ),
        hovertemplate="Dia %{y}<br>Mês %{x}<br>%{z} eventos<extra></extra>",
    ))
    fig_heat.update_layout(xaxis_title="Mês", yaxis_title="Dia do mês", height=390)
    fig_heat = apply_clean_theme(fig_heat)
    st.plotly_chart(fig_heat, use_container_width=True)
    chart_box_close()

with c2:
    chart_box_open("Pulso diário da agenda")
    curve = fdf.groupby("data").size().reset_index(name="eventos")
    fig_curve = px.line(curve, x="data", y="eventos", markers=True, color_discrete_sequence=[PALETTE["primary"]])
    fig_curve.update_traces(
        line=dict(width=3),
        marker=dict(size=8, color=PALETTE["primary"], line=dict(width=2, color="#FFFFFF"))
    )
    fig_curve.update_layout(xaxis_title="Data", yaxis_title="Eventos", height=390, showlegend=False)
    fig_curve = apply_clean_theme(fig_curve)
    st.plotly_chart(fig_curve, use_container_width=True)
    chart_box_close()

st.markdown("## Locais e protagonistas")
c3, c4 = st.columns(2)

with c3:
    chart_box_open("Top locais por volume de eventos")
    local_rank = (
        fdf.groupby("local_curto", as_index=False)
        .size()
        .rename(columns={"size": "eventos"})
        .sort_values("eventos", ascending=True)
        .tail(12)
    )
    fig_loc = px.bar(
        local_rank,
        x="eventos",
        y="local_curto",
        orientation="h",
        text="eventos",
        color_discrete_sequence=[PALETTE["secondary"]],
    )
    fig_loc.update_traces(textposition="outside", cliponaxis=False, textfont=dict(color=PALETTE['text'], size=13), hovertemplate="%{y}<br>%{x} eventos<extra></extra>")
    fig_loc.update_layout(xaxis_title="Eventos", yaxis_title="", height=470, showlegend=False, uniformtext_minsize=12, uniformtext_mode='hide')
    fig_loc = apply_clean_theme(fig_loc)
    st.plotly_chart(fig_loc, use_container_width=True)
    chart_box_close()

with c4:
    chart_box_open("Artistas / momentos mais frequentes")
    artist_rank = (
        fdf.groupby("artista", as_index=False)
        .size()
        .rename(columns={"size": "eventos"})
        .sort_values("eventos", ascending=False)
        .head(12)
    )
    fig_art = px.bar(
        artist_rank,
        x="artista",
        y="eventos",
        text="eventos",
        color_discrete_sequence=[PALETTE["accent"]],
    )
    fig_art.update_traces(textposition="outside", cliponaxis=False, textfont=dict(color=PALETTE['text'], size=13), hovertemplate="%{x}<br>%{y} eventos<extra></extra>")
    fig_art.update_layout(xaxis_title="", yaxis_title="Eventos", height=470, showlegend=False, uniformtext_minsize=12, uniformtext_mode='hide')
    fig_art.update_xaxes(tickangle=-32)
    fig_art = apply_clean_theme(fig_art)
    st.plotly_chart(fig_art, use_container_width=True)
    chart_box_close()

st.markdown("## Agenda interativa")
c5, c6 = st.columns([1, 1])

with c5:
    chart_box_open("Eventos ao longo do tempo")
    fig_timeline = px.scatter(
        fdf,
        x="data",
        y="local_curto",
        color="tipo_evento",
        hover_name="artista",
        hover_data={
            "data": "|%d/%m/%Y",
            "dia_semana": True,
            "tipo_evento": True,
            "local_curto": False,
        },
        color_discrete_map={
            "Concerto": PALETTE["primary"],
            "Especial": PALETTE["secondary"],
        },
    )
    fig_timeline.update_traces(marker=dict(size=11, opacity=0.92, line=dict(width=1.2, color="#FFFFFF")))
    fig_timeline.update_layout(xaxis_title="Data", yaxis_title="Local", height=520, legend_title_text='tipo_evento')
    fig_timeline = apply_clean_theme(fig_timeline)
    fig_timeline.update_layout(legend_title_font=dict(color=PALETTE['text'], size=13), legend_font=dict(color=PALETTE['text'], size=13))
    fig_timeline.update_layout(legend_title_font=dict(color=PALETTE['text'], size=13), legend_font=dict(color=PALETTE['text'], size=13))
    st.plotly_chart(fig_timeline, use_container_width=True)
    chart_box_close()

with c6:
    chart_box_open("Composição da agenda")
    mix = fdf["tipo_evento"].value_counts().reset_index()
    mix.columns = ["tipo", "n"]
    fig_mix = px.pie(
        mix,
        names="tipo",
        values="n",
        hole=0.56,
        color="tipo",
        color_discrete_map={
            "Concerto": PALETTE["primary"],
            "Especial": PALETTE["secondary"],
        },
    )
    fig_mix.update_traces(
        textposition="inside",
        textinfo="percent+label",
        textfont=dict(color="#FFFFFF", size=13),
        marker=dict(line=dict(color="#FFFFFF", width=2)),
        hovertemplate="%{label}: %{value} eventos (%{percent})<extra></extra>",
    )
    fig_mix.update_layout(
        height=260,
        margin=dict(l=12, r=12, t=18, b=8),
        paper_bgcolor=PALETTE["surface"],
        plot_bgcolor=PALETTE["surface"],
        font=dict(color=PALETTE["text"]),
        legend=dict(font=dict(color=PALETTE["text"], size=13)),
    )
    st.plotly_chart(fig_mix, use_container_width=True)
    chart_box_close()

    chart_box_open("Distribuição por dia da semana")
    weekday = fdf.groupby("dia_semana", as_index=False).size().rename(columns={"size": "eventos"})
    weekday["dia_semana"] = pd.Categorical(weekday["dia_semana"], categories=DAY_ORDER, ordered=True)
    weekday = weekday.sort_values("dia_semana")
    fig_week = px.bar(
        weekday,
        x="dia_semana",
        y="eventos",
        text="eventos",
        color_discrete_sequence=[PALETTE["accent"]],
    )
    fig_week.update_traces(textposition="outside", cliponaxis=False, textfont=dict(color=PALETTE['text'], size=13))
    fig_week.update_layout(xaxis_title="", yaxis_title="Eventos", height=260, showlegend=False, uniformtext_minsize=12, uniformtext_mode='hide')
    fig_week.update_xaxes(tickangle=-24)
    fig_week = apply_clean_theme(fig_week)
    st.plotly_chart(fig_week, use_container_width=True)
    chart_box_close()

st.markdown("## Planeamento rápido")
c7, c8 = st.columns(2)

with c7:
    route = (
        fdf.groupby(["data", "local_curto"], as_index=False)
        .size()
        .rename(columns={"size": "eventos"})
        .sort_values(["data", "eventos"], ascending=[True, False])
        .groupby("data")
        .head(1)
        .copy()
    )
    route["Data"] = route["data"].dt.strftime("%d/%m/%Y")
    route = route[["Data", "local_curto", "eventos"]].rename(columns={"local_curto": "Local recomendado", "eventos": "Nº eventos"})
    st.dataframe(route, use_container_width=True, hide_index=True)

with c8:
    recurring = (
        fdf.groupby("artista", as_index=False)
        .agg(eventos=("artista", "size"), locais=("local_curto", "nunique"), dias=("data", "nunique"))
        .sort_values(["eventos", "locais", "dias"], ascending=False)
        .head(10)
    )
    recurring["Presença"] = recurring.apply(
        lambda r: f"{int(r['eventos'])} eventos · {int(r['locais'])} locais · {int(r['dias'])} dias",
        axis=1,
    )
    recurring = recurring[["artista", "Presença"]].rename(columns={"artista": "Nome"})
    st.dataframe(recurring, use_container_width=True, hide_index=True)

st.markdown("## Tabela detalhada")
show_df = fdf[["data", "dia_semana", "local_curto", "artista", "tipo_evento", "contexto", "intensidade"]].copy()
show_df["data"] = show_df["data"].dt.strftime("%Y-%m-%d")
show_df = show_df.rename(columns={
    "data": "Data",
    "dia_semana": "Dia da semana",
    "local_curto": "Local",
    "artista": "Artista / momento",
    "tipo_evento": "Categoria",
    "contexto": "Contexto",
    "intensidade": "Intensidade do dia",
})
st.dataframe(show_df, use_container_width=True, hide_index=True, height=460)

csv = show_df.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "Exportar tabela filtrada (CSV)",
    data=csv,
    file_name="santos_populares_2026_filtrado.csv",
    mime="text/csv",
)