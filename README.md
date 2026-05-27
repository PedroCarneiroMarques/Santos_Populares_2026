# Santos Populares 2026 Dashboard

Dashboard interativo em Streamlit para explorar a programação dos Santos Populares de Lisboa 2026 a partir de um ficheiro Excel.

## O que faz

A aplicação foi redesenhada com foco editorial e rapidez de leitura:

- Hero principal com quadras populares rotativas
- KPIs resumidos para janela ativa, eventos, arraiais e maior cartaz
- Destaque diário do melhor arraial com base na força do cabeça de cartaz
- Ranking de arraiais com lógica editorial por notoriedade
- Tabela filtrada com exportação CSV
- Gráfico temporal por arraial com mapeamento de cores consistente
- Upload manual do Excel caso o ficheiro local não exista

## Lógica de destaque

O ranking dos arraiais não depende apenas do número de eventos.  
Cada artista recebe um score editorial com base em:

- Legado
- Popularidade mass market
- Relevância atual
- Fit com o contexto dos Santos Populares

O destaque do dia é definido pelo artista mais forte presente no cartaz de cada arraial.

## Estrutura do projeto

```txt
.
├── app.py
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
├── requirements.txt
├── setup_github.sh
├── .gitignore
└── data/
    └── santos.xlsx
```

## Requisitos

- Python 3.11+
- pip

## Instalação local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dados

A app procura o ficheiro Excel nestes caminhos:

```txt
data/santos.xlsx
santos.xlsx
./data/santos.xlsx
```

Se não encontrar o ficheiro localmente, permite upload manual pela interface.

## Deploy

Pode ser publicado diretamente no Streamlit Community Cloud.

- Repository: teu repositório GitHub
- Branch: `main`
- Main file path: `app.py`

## Atualizar dados

1. Substitui o ficheiro Excel em `data/santos.xlsx`
2. Corre localmente para validar
3. Faz commit das alterações

Exemplo:

```bash
cp ~/novo_santos.xlsx data/santos.xlsx
streamlit run app.py
git add .
git commit -m "data: atualizar programação"
git push
```
