import streamlit as st

from config import ASSETS_DIR, COLORS


@st.cache_data(show_spinner=False)
def _load_css(_mtime: float) -> str:
    return (ASSETS_DIR / "styles.css").read_text(encoding="utf-8")


def inject_css() -> None:
    css_path = ASSETS_DIR / "styles.css"
    root = "\n".join(
        f"    --{key.replace('_', '-')}: {value};"
        for key, value in COLORS.items()
    )
    css = _load_css(css_path.stat().st_mtime)
    st.markdown(f"<style>:root {{\n{root}\n}}\n{css}</style>", unsafe_allow_html=True)
