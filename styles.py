import streamlit as st

from config import ASSETS_DIR, COLORS


@st.cache_data(show_spinner=False)
def _load_css() -> str:
    return (ASSETS_DIR / "styles.css").read_text(encoding="utf-8")


def inject_css() -> None:
    root = "\n".join(
        f"    --{key.replace('_', '-')}: {value};"
        for key, value in COLORS.items()
    )
    st.markdown(f"<style>:root {{\n{root}\n}}\n{_load_css()}</style>", unsafe_allow_html=True)
