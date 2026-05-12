"""
Basic sanity tests for the data pipeline.
Run with: pytest tests/
"""
import re
import pandas as pd
import pytest
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "santos.xlsx"

MONTHS_PT = {
    "janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4,
    "maio": 5, "junho": 6, "julho": 7, "agosto": 8, "setembro": 9,
    "outubro": 10, "novembro": 11, "dezembro": 12,
}


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


def load_raw():
    raw = pd.read_excel(DATA_PATH, header=None)
    header_idx = raw.index[raw.iloc[:, 0].astype(str).str.strip().eq("Dia")][0]
    df = raw.iloc[header_idx:].copy()
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)
    return df


def test_xlsx_exists():
    assert DATA_PATH.exists(), f"Ficheiro não encontrado: {DATA_PATH}"


def test_xlsx_has_dia_column():
    raw = pd.read_excel(DATA_PATH, header=None)
    dia_rows = raw.iloc[:, 0].astype(str).str.strip().eq("Dia")
    assert dia_rows.any(), "Coluna 'Dia' não encontrada no ficheiro Excel"


def test_date_parsing():
    df = load_raw()
    df = df.rename(columns={"Dia": "dia_raw"})
    dates = df["dia_raw"].apply(parse_pt_date)
    valid = dates.dropna()
    assert len(valid) >= 10, f"Apenas {len(valid)} datas válidas — verifica o ficheiro"


def test_at_least_one_local_column():
    df = load_raw()
    id_cols = {"Dia", "Dia da Semana"}
    local_cols = [c for c in df.columns if c not in id_cols and not str(c).startswith("Unnamed")]
    assert len(local_cols) >= 1, "Nenhuma coluna de local encontrada"


def test_no_empty_data_file():
    df = load_raw()
    assert len(df) > 0, "Ficheiro Excel vazio"
