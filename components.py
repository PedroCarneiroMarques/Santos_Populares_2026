from config import PAGE_TITLE
from text_utils import format_pt_date


def section(label: str, copy: str) -> str:
    return f"<div class='section-label'>{label}</div><div class='section-copy'>{copy}</div>"


def hero(quadra_html: str) -> str:
    return f"""
    <div class="hero">
      <div class="eyebrow">🇵🇹💃🎉 Santos Populares 2026 💃🎉🇵🇹</div>
      <div class="hero-title">{PAGE_TITLE}</div>
      <div class="hero-copy">{quadra_html}</div>
    </div>"""


MANJERICO_HTML = """
<div class="hero-manjerico-wrap">
  <div class="manjerico-shell">
    <a class="manjerico-link-reset" href="?manjerico=open" target="_self">
      <div class="manjerico-plant-zone" role="button" aria-label="Ver quadra do manjerico">
        <span class="manjerico-green-button">Ver quadra</span>
      </div>
    </a>
    <div class="manjerico-pot"></div>
  </div>
</div>"""


def metric_grid(focus_days: int, events: int, arraiais: int, hot_day: dict) -> str:
    cards = [
        ("Janela ativa", f"{focus_days} dias", "Festa à vista"),
        ("Eventos", str(events), "Momentos em cartaz"),
        ("Arraiais", str(arraiais), "Arraiais a mexer"),
        ("Dia mais quente", format_pt_date(hot_day["date"]), f"{hot_day['best_local']} · Nota {hot_day['best_score']}/10"),
    ]
    body = "".join(
        f"<div class='metric-card'><div class='metric-label'>{label}</div>"
        f"<div class='metric-value'>{value}</div><div class='metric-note'>{note}</div></div>"
        for label, value, note in cards
    )
    return f"<div class='metric-grid'>{body}</div>"


def _chips(events: int, profile: str, score: float) -> str:
    return (
        f"<span class='chip chip-red'>{events} eventos</span>"
        f"<span class='chip chip-olive'>{profile}</span>"
        f"<span class='chip chip-gold'>Score {score}/10</span>"
    )


def ranking(top_options) -> str:
    parts = [
        '<div class="card-strong">',
        '<div class="card-kicker">Arraiais mais quentes do dia</div>'
        '<div class="card-copy">A hierarquia é definida pela maior nota individual de notoriedade do dia.</div>',
    ]
    if top_options.empty:
        parts.append("</div>")
        return "".join(parts)

    top = top_options.iloc[0]
    parts.append(f"""
    <div class="top-rank-hero">
      <div class="top-rank-grid">
        <div class="top-rank-badge"><small>Top</small><strong>1</strong></div>
        <div>
          <div class="top-rank-title">{top['local']}</div>
          <div class="card-copy">Cabeça de cartaz: {top.get('cabeca_cartaz', 'Cartaz variado')}</div>
          <div style="height:.55rem"></div>
          {_chips(int(top.get('eventos', 0)), top.get('perfil_forca', 'Notoriedade'), round(float(top.get('score', 0)), 1))}
        </div>
      </div>
    </div>""")

    for i, row in enumerate(top_options.iloc[1:].itertuples(index=False), start=2):
        parts.append(
            f"<div class='rank-row'><div class='rank-place'>{i}. {row.local}</div>"
            f"<div class='rank-meta'>{row.cabeca_cartaz} · Score {row.score}/10 · {row.perfil_forca}</div></div>"
        )
    parts.append("</div>")
    return "".join(parts)


def day_card(summary: dict, featured: bool) -> str:
    title = f"{format_pt_date(summary['date'])} · {summary['day_name']}"
    copy = f"{summary['total']} entradas distribuídas por {summary['arraiais']} arraiais."
    span = "span-2" if featured else "span-1"
    card_class = "card-strong day-heat-hero" if featured else "card"

    if featured:
        return f"""
        <div class="{card_class} {span}">
          <div class="day-order-note">Dia mais forte da janela ativa</div>
          <div class="card-kicker">{summary['relative_label']} · {summary['mood']}</div>
          <div class="card-title">{title}</div>
          <div class="card-copy">{copy} O destaque é definido pelo artista mais forte do cartaz, sem somar nomes.</div>
          <div style="height:.75rem"></div>
          <div class="pick-card">
            <div class="card-kicker">Arraial em destaque</div>
            <div class="card-title">{summary['best_local']}</div>
            <div class="card-copy">Cabeça de cartaz: {summary['best_headliner']}</div>
          </div>
          <div style="height:.75rem"></div>
          {_chips(summary['best_events'], summary['best_profile'], summary['best_score'])}
        </div>"""

    note = f"{summary['relative_label']} · {summary['mood']}"
    return f"""
    <div class="{card_class} {span}">
      <div class="card-kicker">{note}</div>
      <div class="card-title">{title}</div>
      <div class="card-copy">{copy}</div>
      <div style="height:.5rem"></div>
      <div class="soft-card">
        <div class="rank-place">{summary['best_local']}</div>
        <div class="rank-meta">Cabeça de cartaz: {summary['best_headliner']} · Score {summary['best_score']}/10</div>
      </div>
    </div>"""


def manjerico_dialog_html(quadra_html: str) -> str:
    return f"""
    <div style="padding:.25rem .15rem;">
      <div style="font-size:.78rem; color:#C62828; font-weight:900; text-transform:uppercase; letter-spacing:.06em; margin-bottom:.6rem;">Bilhete do manjerico</div>
      <div style="background:#F4E24F; border:1px solid #CBB53A; border-radius:16px; padding:1rem .95rem; box-shadow:0 8px 20px rgba(92,54,18,.10);">
        <div style="font-size:.94rem; line-height:1.6; color:#3E2615; font-weight:700;">{quadra_html}</div>
      </div>
    </div>"""
