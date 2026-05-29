# Contributing

## Objetivo

Este projeto privilegia clareza visual, leitura rápida e decisões orientadas por destaque de cartaz, mantendo uma estética popular e editorial inspirada nos Santos Populares.[file:438]

## Regras para alterações futuras

- Preservar o ficheiro base mais recente validado pelo utilizador antes de introduzir novos ajustes.[file:438]
- Sempre que houver alterações visuais, confirmar se o comportamento continua coerente entre desktop e mobile, porque a grelha muda de 4 colunas para 2 e depois 1 coluna nos breakpoints definidos no CSS.[file:438]
- Não reverter a lógica de ordenação por calor do cartaz no bloco diário sem validação explícita, porque esta foi uma decisão funcional recente.[file:438]
- Não voltar a uniformizar o ranking diário; o nº1 deve continuar visualmente destacado.[file:438]

## Boas práticas de desenvolvimento

- Centralizar novos estilos dentro de `inject_css()` para manter consistência com a arquitetura atual.[file:438]
- Reutilizar as funções de resumo existentes (`summarize_options`, `build_day_summary`, `build_heat_order_summaries`) antes de criar lógica duplicada.[file:438]
- Sempre que um novo bloco visual dependa de força de cartaz, usar `best_score` e o cabeça de cartaz resultante da lógica atual, em vez de criar scores paralelos.[file:438]
- Manter os textos e labels em português para coerência com a interface e com os dados tratados pela app.[file:438]

## Checklist antes de fechar alterações

- Confirmar que o topo diário mostra o dia mais forte e não apenas o primeiro dia cronológico.[file:438]
- Confirmar que o ranking mostra um card hero para o nº1 e linhas compactas para as restantes posições.[file:438]
- Confirmar que a interação do manjerico continua funcional após qualquer alteração estrutural da hero section.[file:438]
