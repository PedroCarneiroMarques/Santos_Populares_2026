# Guia Oficial das Festas de Lisboa

Dashboard Streamlit para explorar o cartaz dos Santos Populares de Lisboa 2026 — leitura rápida, destaque visual e apoio à decisão sobre onde começar a festa.

Repositório: [PedroCarneiroMarques/Santos_Populares_2026](https://github.com/PedroCarneiroMarques/Santos_Populares_2026)

## Funcionalidades

- Leitura automática do Excel com normalização de datas, locais, artistas e categorias.
- Notoriedade por artista com perfis ponderados (`legado`, `mass_market`, `relevancia_atual`, `fit_santos`).
- Resumo diário por arraial com cabeça de cartaz mais forte (sem somar nomes do lineup).
- Termómetro da festa com até 7 dias e artista destacado em cada ponto do gráfico.
- Manjerico interativo com quadras em diálogo dedicado.
- Votação comunitária: cada visitante escolhe o arraial preferido (um voto por sessão, alterável) com ranking agregado.
- Cards diários ordenados por calor do cartaz, não por cronologia.

## Estrutura do projeto

```
app.py              # Entry point Streamlit (~140 linhas)
config.py           # Cores, constantes e paths
data.py             # Pipeline Excel e agregações
artists.py          # Perfis de artistas e scoring
text_utils.py       # Normalização e parsing de texto/datas
quadras.py          # Lógica das quadras (session state)
votes.py            # Sistema de votação (SQLite)
components.py       # Templates HTML da interface
charts.py           # Gráfico Plotly
styles.py           # Injeção de CSS
assets/styles.css   # Estilos da aplicação
data/
  santos.xlsx       # Agenda oficial (fonte de dados)
  quadras_hero.txt
  quadras_manjerico.txt
tests/              # Testes de sanidade do pipeline
```

## Execução

```bash
pip install -r requirements.txt
streamlit run app.py
```

1. Colocar `santos.xlsx` em `data/` (ou na raiz) — ou carregar manualmente pela interface.
2. Ajustar filtros na sidebar: intervalo, local, categoria e fim de semana.

## Lógica principal

| Módulo | Responsabilidade |
|--------|------------------|
| `data.load_and_prepare_data` | Excel → DataFrame normalizado com scores |
| `data.summarize_options` | Métricas por local e cabeça de cartaz |
| `data.build_day_summary` | Resumo de um dia |
| `data.build_heat_order_summaries` | Dias ordenados por força do cartaz |
| `artists.get_artist_score` | Score 0–10 com cache |
| `components.*` | HTML reutilizável (hero, ranking, cards) |
| `votes.*` | Registo e agregação de votos (SQLite em `data/votes.db`) |

## Notas de manutenção

- Os cards “Hoje / Amanhã / Depois” são contexto temporal; a ordem visual segue `best_score`, `total` e `arraiais`.
- O ranking principal usa o dia mais quente da janela ativa, não o primeiro dia cronológico.
- Novos estilos: editar `assets/styles.css`; variáveis de cor vêm de `config.COLORS` via `styles.py`.
- Novas quadras: editar `data/quadras_hero.txt` ou `data/quadras_manjerico.txt`.

## Testes

```bash
pytest tests/
```
