from pathlib import Path

COLORS = {
    "bg": "#F4E6C8",
    "surface": "#FFF7E8",
    "surface_alt": "#F9EED8",
    "border": "#D8B98A",
    "border_strong": "#B88746",
    "text": "#3E2615",
    "muted": "#6E4B2A",
    "soft": "#8C6337",
    "accent": "#C62828",
    "accent_soft": "#FBE0D6",
    "section_tint": "#F3D94C",
    "shadow": "0 8px 22px rgba(92,54,18,.14)",
    "green_zone": "#4CAF50",
    "green_zone_dark": "#2E7D32",
    "green_zone_light": "#7BC96F",
    "green_zone_text": "#F7FFE9",
}

MESES_PT = {
    "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4,
    "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8,
    "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12,
}

DIAS_SEMANA_PT = {
    "Monday": "segunda-feira", "Tuesday": "terça-feira", "Wednesday": "quarta-feira",
    "Thursday": "quinta-feira", "Friday": "sexta-feira", "Saturday": "sábado", "Sunday": "domingo",
}

DATA_PATHS = (Path("data/santos.xlsx"), Path("santos.xlsx"))
QUADRAS_DIR = Path("data")
ASSETS_DIR = Path("assets")

PAGE_TITLE = "Guia Oficial das Festas de Lisboa para o (B)enfica(B)eer(C)lub"
