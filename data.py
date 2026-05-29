from io import BytesIO
from typing import List, Optional

import pandas as pd
import streamlit as st

from artists import classify_event, get_artist_score, get_headliner_name, get_headliner_profile
from config import DATA_PATHS, DIAS_SEMANA_PT
from text_utils import (
    clean_display_text,
    format_pt_date,
    normalize_text,
    parse_date_label,
    relative_label,
    split_multiline_cell,
    EMPTY_CELL_VALUES,
)


@st.cache_data(ttl=3600, show_spinner=False)
def load_and_prepare_data(file_bytes: bytes) -> pd.DataFrame:
    raw = pd.read_excel(BytesIO(file_bytes), header=None, engine="openpyxl")
    headers = [normalize_text(x) for x in raw.iloc[2].tolist()]
    df = raw.iloc[3:].copy()
    df.columns = headers
    df = df.dropna(how="all").rename(columns={"Dia": "dia", "Dia da Semana": "dia_semana_excel"})
    if "dia" not in df.columns or "dia_semana_excel" not in df.columns:
        raise ValueError("Não foi possível localizar as colunas 'Dia' e 'Dia da Semana'.")

    event_cols = [c for c in df.dropna(axis=1, how="all").columns if c not in ("dia", "dia_semana_excel")]
    long_df = df.melt(["dia", "dia_semana_excel"], event_cols, var_name="local", value_name="conteudo")
    long_df["conteudo"] = long_df["conteudo"].map(normalize_text)
    long_df = long_df[(long_df["conteudo"] != "") & (~long_df["conteudo"].isin(EMPTY_CELL_VALUES))]
    long_df["data"] = long_df["dia"].map(parse_date_label)
    long_df = long_df.dropna(subset=["data"])
    long_df["dia_label"] = long_df["dia"].map(normalize_text)
    long_df["dia_semana_excel"] = long_df["dia_semana_excel"].map(normalize_text)
    long_df["local"] = long_df["local"].map(clean_display_text)
    long_df["entries"] = long_df["conteudo"].map(split_multiline_cell)
    long_df = long_df.explode("entries", ignore_index=True).dropna(subset=["entries"])

    events = long_df.rename(columns={"entries": "artista_evento"})
    events["artista_evento"] = events["artista_evento"].map(clean_display_text)
    events["conteudo_original"] = events["conteudo"].map(clean_display_text)
    events = events[["data", "dia_label", "dia_semana_excel", "local", "artista_evento", "conteudo_original"]]
    if events.empty:
        return events

    events["dia_semana"] = events["data"].dt.day_name().map(DIAS_SEMANA_PT).fillna(events["dia_semana_excel"])
    events["fim_de_semana"] = events["data"].dt.dayofweek >= 4
    events["feriado"] = events["dia_label"].str.contains("Feriado", case=False, na=False)

    unique = events["artista_evento"].unique()
    events["categoria"] = events["artista_evento"].map({n: classify_event(n) for n in unique})
    events["artist_score"] = events["artista_evento"].map({n: get_artist_score(n) for n in unique})
    events["artist_profile_label"] = events["artista_evento"].map({n: get_headliner_profile(n) for n in unique})
    events = events.merge(events.groupby("data").size().rename("eventos_no_dia"), on="data", how="left")
    return events.sort_values(["data", "local", "artista_evento"]).reset_index(drop=True)


@st.cache_data(show_spinner=False)
def read_local_xlsx() -> Optional[bytes]:
    for path in DATA_PATHS:
        if path.exists():
            return path.read_bytes()
    return None


def get_anchor_date(df: pd.DataFrame) -> pd.Timestamp:
    today = pd.Timestamp.now().normalize()
    dates = sorted(pd.to_datetime(df["data"].dropna().unique()))
    if not dates:
        return today
    future = [d for d in dates if d >= today]
    return future[0] if future else dates[-1]


def slice_date_window(df: pd.DataFrame, anchor: pd.Timestamp, days: int) -> pd.DataFrame:
    window = df[df["data"].isin(pd.date_range(anchor, periods=days, freq="D"))]
    if window.empty:
        fallback = sorted(pd.to_datetime(df["data"].unique()))[:days]
        window = df[df["data"].isin(fallback)]
    return window


def _unique_top_acts(series: pd.Series) -> List[str]:
    seen, top = set(), []
    for value in series:
        cleaned = clean_display_text(value)
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            top.append(cleaned)
        if len(top) >= 5:
            break
    return top


def summarize_options(day_df: pd.DataFrame) -> pd.DataFrame:
    if day_df.empty:
        return pd.DataFrame()

    grouped = (
        day_df.groupby("local", sort=False)
        .agg(eventos=("artista_evento", "count"), atos_unicos=("artista_evento", "nunique"), score_notoriedade=("artist_score", "max"))
        .reset_index()
    )
    acts = day_df.groupby("local", sort=False)["artista_evento"].apply(_unique_top_acts).reset_index(name="top_atos")
    grouped = grouped.merge(acts, on="local")
    grouped["cabeca_cartaz"] = grouped["top_atos"].map(get_headliner_name)
    grouped["forca_cartaz"] = grouped["cabeca_cartaz"].map(get_artist_score)
    grouped["perfil_forca"] = grouped["cabeca_cartaz"].map(get_headliner_profile)
    grouped["score"] = grouped["forca_cartaz"].round(1)
    return grouped.sort_values(["score", "eventos", "atos_unicos"], ascending=False).reset_index(drop=True)


def _day_mood(day_df: pd.DataFrame) -> str:
    total, locais = len(day_df), day_df["local"].nunique()
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
    return {
        "date": pd.to_datetime(day_df["data"].iloc[0]),
        "day_name": clean_display_text(day_df["dia_semana"].iloc[0]).capitalize(),
        "total": len(day_df),
        "arraiais": day_df["local"].nunique(),
        "mood": _day_mood(day_df),
        "best_local": best["local"],
        "best_events": int(best["eventos"]),
        "best_unique": int(best["atos_unicos"]),
        "best_headliner": best.get("cabeca_cartaz", "Cartaz variado"),
        "best_score": round(float(best.get("score", 0)), 1),
        "best_profile": best.get("perfil_forca", "Notoriedade"),
        "top_acts": best["top_atos"] if isinstance(best["top_atos"], list) else [],
        "options": options,
    }


def build_heat_order_summaries(focus_df: pd.DataFrame, anchor: pd.Timestamp) -> List[dict]:
    summaries = []
    for day, day_df in focus_df.groupby("data", sort=True):
        summary = build_day_summary(day_df)
        if summary:
            summary["relative_label"] = relative_label(pd.Timestamp(day), anchor)
            summaries.append(summary)
    return sorted(summaries, key=lambda x: (x["best_score"], x["total"], x["arraiais"]), reverse=True)


def build_daily_chart_summary(chart_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for data, group in chart_df.groupby("data"):
        options = summarize_options(group)
        if options.empty:
            continue
        best = options.iloc[0]
        rows.append({
            "data": pd.Timestamp(data),
            "dia_semana": group["dia_semana"].iloc[0],
            "local": best["local"],
            "cabeca_cartaz": best["cabeca_cartaz"],
            "perfil_forca": best["perfil_forca"],
            "score": float(best["score"]),
        })
    return pd.DataFrame(rows).sort_values("data").reset_index(drop=True)
