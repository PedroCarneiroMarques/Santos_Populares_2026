# Changelog

## 2026-05-29 — Refactor modular e otimizações

### Added

- Arquitetura modular: `config`, `data`, `artists`, `text_utils`, `quadras`, `components`, `charts`, `styles`.
- CSS externalizado em `assets/styles.css`.
- Quadras externalizadas em `data/quadras_hero.txt` e `data/quadras_manjerico.txt`.

### Changed

- `app.py` reduzido a entry point Streamlit (~140 linhas).
- Pipeline de dados vectorizado (`explode` + `map` em vez de `iterrows`).
- Lookup de artistas pré-normalizado com `@lru_cache` em scores e perfis.
- `build_focus` / `build_chart_window` unificados em `slice_date_window`.
- CSS injetado uma vez por sessão; leitura do Excel em cache.

### Preserved

- Hero, manjerico, diálogo modal, gráfico de 7 dias, ranking nº1 destacado e ordenação por calor do cartaz.

---

## 2026-05-29 — Updates visuais e funcionais

### Added

- Destaque visual dedicado para o arraial nº1 no ranking do dia.
- Ordenação por calor do cartaz no bloco de dias em foco.
- Estilo `day-heat-hero` para o dia mais forte da janela ativa.

### Changed

- Bloco “Hoje / Amanhã / Depois” ordenado por `best_score`, `total` e `arraiais`.
- Indicador de métricas reflete o dia mais quente da janela ativa.
- Ranking separa o 1.º classificado dos restantes.
