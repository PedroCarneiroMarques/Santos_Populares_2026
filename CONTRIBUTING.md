# Contributing

## Objetivo

Este projeto privilegia clareza visual, leitura rápida e decisões orientadas por destaque de cartaz, mantendo uma estética popular e editorial inspirada nos Santos Populares.

## Estrutura do código

- **`app.py`** — orquestração Streamlit; evitar lógica de negócio aqui.
- **`data.py`** — pipeline Excel e agregações; reutilizar `summarize_options`, `build_day_summary`, `build_heat_order_summaries`.
- **`artists.py`** — perfis e scoring; não duplicar scores noutros módulos.
- **`components.py`** — HTML da interface; manter templates reutilizáveis.
- **`assets/styles.css`** — estilos; variáveis de cor definidas em `config.COLORS` e injetadas por `styles.py`.

## Regras para alterações futuras

- Preservar a lógica de ordenação por calor do cartaz no bloco diário.
- Manter o nº1 do ranking visualmente destacado (`top-rank-hero`).
- Confirmar comportamento em desktop e mobile (grelha 4 → 2 → 1 colunas nos breakpoints do CSS).
- Manter textos e labels em português.
- Preservar a identidade festiva: grinalda de bandeirinhas (`festa-garland`), fontes `Fredoka`/`Caveat` e marca de água no fundo.
- Qualquer animação nova tem de ser desativada em `@media (prefers-reduced-motion: reduce)`.
- Votação: um voto por pessoa por dia (`voting.py`); não reintroduzir o nome `votes` (colide no PyPI/Streamlit Cloud).

## Boas práticas

- Usar `best_score` e cabeça de cartaz da lógica existente — não criar scores paralelos.
- Editar quadras nos ficheiros `data/quadras_*.txt`, não inline no Python.
- Correr `pytest tests/` antes de fechar alterações.

## Checklist

- [ ] Dia mais forte aparece como destaque principal, não o primeiro cronológico.
- [ ] Ranking mostra card hero para nº1 e linhas compactas para o resto.
- [ ] Manjerico e diálogo de quadras continuam funcionais após alterações.
