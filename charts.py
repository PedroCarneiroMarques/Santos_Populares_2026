import plotly.graph_objects as go
import pandas as pd

from config import COLORS
from text_utils import abbreviate_label, short_weekday_pt


def build_festival_chart(chart_df: pd.DataFrame) -> go.Figure:
    base = chart_df.copy()
    base["dia_curto"] = base["dia_semana"].map(short_weekday_pt)
    base["data_curta"] = pd.to_datetime(base["data"]).dt.strftime("%d/%m")
    base["artist_label"] = base["cabeca_cartaz"].map(lambda x: abbreviate_label(x, 14))
    base["x_label"] = base["dia_curto"] + " " + base["data_curta"]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=base["x_label"],
            y=base["score"],
            mode="lines+markers+text",
            text=base["artist_label"],
            textposition="top center",
            textfont=dict(size=11, color=COLORS["text"]),
            line=dict(color=COLORS["accent"], width=3.5, shape="spline", smoothing=0.45),
            marker=dict(size=11, color=COLORS["accent"], line=dict(color=COLORS["surface"], width=2)),
            customdata=base[["local", "cabeca_cartaz", "perfil_forca", "data_curta"]],
            hovertemplate=(
                "<b>%{customdata[3]}</b><br>"
                "Arraial em destaque: %{customdata[0]}<br>"
                "Cabeça de cartaz: %{customdata[1]}<br>"
                "Perfil dominante: %{customdata[2]}<br>"
                "Score: %{y:.1f}/10<br><extra></extra>"
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
    fig.update_yaxes(range=[0, 10], tickmode="array", tickvals=list(range(0, 11, 2)),
                     gridcolor="rgba(110,75,42,0.18)", zeroline=False)
    return fig
