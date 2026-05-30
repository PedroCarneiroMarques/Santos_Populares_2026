# Changelog

## 2026-05-30 — Filtros interativos

### Added

- Pesquisa por artista / cabeça de cartaz (ignora acentos e maiúsculas).
- Slider de notoriedade mínima do cartaz (0–10) para focar nos atos mais fortes.

### Changed

- Filtros de Local e Categoria passam a multi-seleção (vários em simultâneo).

---

## 2026-05-30 — Votação diária, identidade festiva e limpeza

### Added

- **Votação comunitária diária**: cada visitante escolhe o arraial preferido (um voto por dia, alterável até à meia-noite) com ranking diário agregado, guardado em SQLite (`data/votes.db`). Módulo `voting.py` + testes `tests/test_voting.py`.
- **Score acumulado por arraial**: a hierarquia soma a notoriedade dos artistas únicos do cartaz (máx. 10); o cabeça de cartaz continua a ser o nome mais forte.
- **Identidade visual dos Santos Populares**:
  - Bandeirinhas de papel (grinalda CSS) no topo do hero e de cada secção principal, com balanço suave.
  - Tipografia festiva: `Fredoka` nos títulos e `Caveat` (manuscrita) nas quadras, via Google Fonts.
  - Marca de água subtil de sardinhas e manjerico no fundo da página.
  - Brilho radial no hero, elevação dos cartões no hover, manjerico a "respirar" e brilho dourado no nº1 do ranking.
  - Todas as animações respeitam `prefers-reduced-motion`.

### Changed

- Módulo de votação renomeado de `votes` para `voting` (o pacote PyPI `votes` colidia no Streamlit Cloud).
- CSS injetado em cada rerun e recarregado por `mtime` (corrige UI sem estilo após interações e cache desatualizado).
- Título do hero em duas linhas equilibradas, sem o limite `14ch`; espaçamento de letras afinado e responsivo (desktop / 980px / 768px).
- Caminhos baseados em `ROOT_DIR` para funcionar no Streamlit Cloud.
- Copy: secção "Dica para boa disposição!" e diálogo do manjerico sem repetição ("Manjerico de Santo António" + "Versos para oferecer").

### Removed

- `setup_github.sh` (bootstrap usado uma só vez) e screenshots não referenciados em `images/`.
- `Archive.zip` deixou de ser versionado; `*.zip` e `.pytest_cache/` ignorados.

---

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
