from text_utils import format_pt_date


def section(label: str, copy: str) -> str:
    return (
        _garland(flags=20, mini=True)
        + f"<div class='section-label'>{label}</div><div class='section-copy'>{copy}</div>"
    )


_GARLAND_COLORS = ("#E53935", "#F4B400", "#43A047", "#1E88E5", "#FB8C00")


def _garland(flags: int = 48, mini: bool = False) -> str:
    spans = "".join(
        f'<span class="festa-flag" style="border-top-color:{_GARLAND_COLORS[i % len(_GARLAND_COLORS)]}"></span>'
        for i in range(flags)
    )
    cls = "festa-garland festa-garland-mini" if mini else "festa-garland"
    return f'<div class="{cls}" aria-hidden="true">{spans}</div>'


def hero(quadra_html: str) -> str:
    title_lines = (
        "Guia Oficial das Festas de Lisboa",
        "para o (B)enfica(B)eer(C)lub",
    )
    title_html = "".join(
        f'<span class="hero-title-line" style="display:block">{line}</span>'
        for line in title_lines
    )
    return f"""
    <div class="hero">
      {_garland()}
      <div class="eyebrow">🇵🇹💃🎉 Santos Populares 2026 💃🎉🇵🇹</div>
      <div class="hero-title">{title_html}</div>
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


def _chips(events: int, profile: str, score: float, votes: int = 0) -> str:
    vote_chip = f"<span class='chip chip-vote'>{votes} voto{'s' if votes != 1 else ''}</span>" if votes else ""
    return (
        f"<span class='chip chip-red'>{events} eventos</span>"
        f"<span class='chip chip-olive'>{profile}</span>"
        f"<span class='chip chip-gold'>Score {score}/10</span>"
        f"{vote_chip}"
    )


def ranking(top_options, vote_counts: dict | None = None) -> str:
    vote_counts = vote_counts or {}
    parts = [
        '<div class="card-strong">',
        '<div class="card-kicker">Arraiais mais quentes do dia</div>'
        '<div class="card-copy">A hierarquia soma a notoriedade dos artistas únicos do cartaz (máx. 10). O cabeça de cartaz continua a ser o nome mais forte.</div>',
    ]
    if top_options.empty:
        parts.append("</div>")
        return "".join(parts)

    top = top_options.iloc[0]
    top_votes = vote_counts.get(top["local"], 0)
    parts.append(f"""
    <div class="top-rank-hero">
      <div class="top-rank-grid">
        <div class="top-rank-badge"><small>Top</small><strong>1</strong></div>
        <div>
          <div class="top-rank-title">{top['local']}</div>
          <div class="card-copy">Cabeça de cartaz: {top.get('cabeca_cartaz', 'Cartaz variado')}</div>
          <div style="height:.55rem"></div>
          {_chips(int(top.get('eventos', 0)), top.get('perfil_forca', 'Notoriedade'), round(float(top.get('score', 0)), 1), top_votes)}
        </div>
      </div>
    </div>""")

    for i, row in enumerate(top_options.iloc[1:].itertuples(index=False), start=2):
        row_votes = vote_counts.get(row.local, 0)
        vote_note = f" · {row_votes} voto{'s' if row_votes != 1 else ''}" if row_votes else ""
        parts.append(
            f"<div class='rank-row'><div class='rank-place'>{i}. {row.local}</div>"
            f"<div class='rank-meta'>{row.cabeca_cartaz} · Score {row.score}/10 · {row.perfil_forca}{vote_note}</div></div>"
        )
    parts.append("</div>")
    return "".join(parts)


def vote_leaderboard_html(leaderboard) -> str:
    if leaderboard.empty:
        return "<div class='card-copy'>Ainda não há votos. Sê o primeiro a escolher o teu arraial!</div>"
    rows = "".join(
        f"<div class='vote-leader-row'><span class='vote-leader-name'>{i}. {row.local}</span>"
        f"<span class='vote-leader-count'>{int(row.votes)} voto{'s' if row.votes != 1 else ''}</span></div>"
        for i, row in enumerate(leaderboard.itertuples(index=False), start=1)
    )
    return f"<div class='vote-leaderboard'>{rows}</div>"


def day_card(summary: dict, featured: bool, vote_counts: dict | None = None) -> str:
    vote_counts = vote_counts or {}
    title = f"{format_pt_date(summary['date'])} · {summary['day_name']}"
    copy = f"{summary['total']} entradas distribuídas por {summary['arraiais']} arraiais."
    span = "span-2" if featured else "span-1"
    card_class = "card-strong day-heat-hero" if featured else "card"
    best_votes = vote_counts.get(summary["best_local"], 0)
    vote_line = f" · {best_votes} voto{'s' if best_votes != 1 else ''} da comunidade" if best_votes else ""

    if featured:
        return f"""
        <div class="{card_class} {span}">
          <div class="day-order-note">Dia mais forte da janela ativa</div>
          <div class="card-kicker">{summary['relative_label']} · {summary['mood']}</div>
          <div class="card-title">{title}</div>
          <div class="card-copy">{copy} O score acumula artistas únicos do cartaz até 10; o destaque nominal é o cabeça de cartaz.</div>
          <div style="height:.75rem"></div>
          <div class="pick-card">
            <div class="card-kicker">Arraial em destaque</div>
            <div class="card-title">{summary['best_local']}</div>
            <div class="card-copy">Cabeça de cartaz: {summary['best_headliner']}{vote_line}</div>
          </div>
          <div style="height:.75rem"></div>
          {_chips(summary['best_events'], summary['best_profile'], summary['best_score'], best_votes)}
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
        <div class="rank-meta">Cabeça de cartaz: {summary['best_headliner']} · Score {summary['best_score']}/10{vote_line}</div>
      </div>
    </div>"""


def manjerico_dialog_html(quadra_html: str) -> str:
    return f"""
    <div style="padding:.25rem .15rem;">
      <div style="font-size:.78rem; color:#C62828; font-weight:900; text-transform:uppercase; letter-spacing:.06em; margin-bottom:.6rem;">Versos para oferecer</div>
      <div style="background:#F4E24F; border:1px solid #CBB53A; border-radius:16px; padding:1rem .95rem; box-shadow:0 8px 20px rgba(92,54,18,.10);">
        <div class="quadra-text" style="font-size:1.5rem; line-height:1.3; color:#3E2615; font-weight:700;">{quadra_html}</div>
      </div>
    </div>"""
