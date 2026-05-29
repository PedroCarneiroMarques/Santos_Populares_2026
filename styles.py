import streamlit as st

from config import ASSETS_DIR, COLORS

_CSS = (ASSETS_DIR / "styles.css").read_text(encoding="utf-8")


def inject_css() -> None:
    root = "\n".join(
        f"    --{key.replace('_', '-')}: {value};"
        for key, value in COLORS.items()
    )
    st.markdown(f"<style>:root {{\n{root}\n}}\n{_CSS}</style>", unsafe_allow_html=True)
