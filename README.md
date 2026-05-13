# Santos Populares 2026 Dashboard

Dashboard interativo em Streamlit para explorar a programação dos Santos Populares 2026 a partir de um ficheiro Excel.

## Funcionalidades

- Leitura e transformação automática do ficheiro `santos.xlsx`
- Filtros por intervalo de datas, local, categoria, intensidade e artista
- KPIs de resumo
- Heatmap diário
- Curva temporal de eventos
- Ranking de arraiais
- Distribuição por categoria
- Timeline da programação
- Top artistas / entradas
- Exportação da tabela filtrada para CSV

## Estrutura do projeto

```txt
.
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    └── santos.xlsx
```

## Instalação local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Este projeto pode ser publicado diretamente no Streamlit Community Cloud a partir do GitHub.

- Repository: o teu repositório GitHub
- Branch: `main`
- Main file path: `app.py`

## Dados

O dashboard espera encontrar o ficheiro Excel em:

```txt
data/santos.xlsx
```

Se o ficheiro não existir localmente, a app também permite upload manual do Excel pela interface.