# Guia Oficial das Festas de Lisboa

Aplicação Streamlit para explorar o cartaz dos Santos Populares de Lisboa com foco em leitura rápida, destaque visual e apoio à decisão sobre onde começar a festa.[file:438]

## Estado atual

A versão atual mantém como base o ficheiro `paste.txt` mais recente partilhado pelo utilizador e incorpora os últimos ajustes debatidos na conversa.[file:438]

### Últimos updates aplicados

- O card de ranking **nº1** passou a ser renderizado como destaque visual maior através de um bloco dedicado com badge, título reforçado e chips próprios.[file:438]
- O bloco “Hoje / Amanhã / Depois” deixou de ser apresentado por ordem cronológica e passou a ser ordenado por calor do cartaz com base em `best_score`, `total` e `arraiais`.[file:438]
- O dia mais forte da janela ativa passou a ocupar o card principal do bloco diário, usando uma variante visual própria (`day-heat-hero`).[file:438]
- O resto da estrutura recente foi preservado, incluindo hero, manjerico, diálogo da quadra e gráfico de 7 dias.[file:438]

## Funcionalidades principais

- Leitura e preparação automática do ficheiro Excel com normalização de datas, locais, artistas e categorias.[file:438]
- Cálculo de notoriedade por artista com perfis ponderados (`legado`, `mass_market`, `relevancia_atual`, `fit_santos`).[file:438]
- Resumo diário por arraial com escolha do cabeça de cartaz mais forte sem somar nomes do lineup.[file:438]
- Visualização do termómetro da festa com até 7 dias e identificação do cabeça de cartaz por ponto no gráfico.[file:438]
- Bloco interativo do manjerico com abertura de quadras em diálogo dedicado.[file:438]

## Estrutura lógica relevante

### Funções novas ou ajustadas

- `build_heat_order_summaries(...)`: agrega os dias da janela de foco e ordena-os por força do cartaz em vez de cronologia.[file:438]
- `build_day_summary(...)`: resume cada dia e devolve os indicadores usados nos cards e ranking.[file:438]
- `summarize_options(...)`: calcula métricas por local, incluindo cabeça de cartaz, score e perfil dominante.[file:438]

### Componentes visuais novos ou ajustados

- `top-rank-hero`, `top-rank-grid`, `top-rank-badge`, `top-rank-title` para o destaque do ranking nº1.[file:438]
- `day-heat-hero` e `day-order-note` para o dia mais forte dentro da janela ativa.[file:438]

## Execução

1. Garantir que existe um ficheiro `santos.xlsx` em `data/`, na raiz do projeto, ou carregar manualmente o ficheiro pela interface.[file:438]
2. Instalar dependências do projeto Streamlit e executar a aplicação principal.[file:438]
3. Ajustar filtros na sidebar para intervalo, local, categoria e opção de fim de semana.[file:438]

## Notas de manutenção

- A ordenação visual dos cards diários já não corresponde necessariamente à ordem temporal; os rótulos “Hoje”, “Amanhã” e “Depois” funcionam apenas como contexto temporal.[file:438]
- O ranking principal usa o dia mais quente da janela ativa, não apenas o primeiro dia cronológico do intervalo focado.[file:438]
