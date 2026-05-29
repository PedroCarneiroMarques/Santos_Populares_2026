# Changelog

## 2026-05-29

### Added

- Destaque visual dedicado para o arraial nº1 no ranking do dia com bloco maior, badge “Top 1” e metadados reforçados.[file:438]
- Ordenação por calor do cartaz no bloco de dias em foco através de `build_heat_order_summaries(...)`.[file:438]
- Estilo visual especial para o dia mais forte da janela ativa com `day-heat-hero`.[file:438]

### Changed

- O bloco “Hoje / Amanhã / Depois” deixou de seguir estritamente a cronologia e passou a priorizar `best_score`, seguido de volume total e número de arraiais.[file:438]
- O indicador de destaque superior na área de métricas passou a refletir o “dia mais quente” da janela ativa em vez do primeiro dia cronológico.[file:438]
- O ranking diário passou a separar o primeiro classificado dos restantes em vez de mostrar todos com o mesmo peso visual.[file:438]

### Preserved

- Hero principal, sistema de quadras, manjerico, diálogo modal e gráfico de 7 dias foram mantidos como base da versão mais recente considerada correta pelo utilizador.[file:438]
