# 🎊 Santos Populares 2026 — Dashboard Lisboa

Dashboard interativo para explorar a agenda dos Santos Populares de Lisboa 2026.  
Construído com **Streamlit**, **Pandas** e **Plotly**.

![Python](https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/streamlit-1.35%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![CI](https://github.com/<SEU_USERNAME>/santos-populares-2026/actions/workflows/ci.yml/badge.svg)

---

## Funcionalidades

- **Filtros dinâmicos** — intervalo de datas, local, artista, tipo de evento, contexto (feriado / fim de semana)
- **Métricas de resumo** — total de eventos, locais ativos, artistas, dia mais intenso
- **Heatmap calendário** — densidade de eventos por dia e mês
- **Curva temporal** — pulso diário da programação
- **Ranking** — top locais e artistas/momentos
- **Agenda interativa** — scatter plot por local e data
- **Planeamento rápido** — local recomendado por dia e presença de artistas
- **Exportação CSV** — tabela filtrada para download

---

## Estrutura do repositório

```
santos-populares-2026/
├── app.py                      # Aplicação Streamlit principal
├── requirements.txt            # Dependências Python
├── .python-version             # Versão Python (pyenv / asdf)
├── .streamlit/
│   └── config.toml             # Configuração do Streamlit
├── data/
│   └── santos.xlsx             # Dados da agenda (substituível — ver abaixo)
├── tests/
│   ├── __init__.py
│   └── test_data_loading.py    # Testes de sanidade ao pipeline de dados
├── .github/
│   └── workflows/
│       └── ci.yml              # CI: testes automáticos no push/PR
├── .gitignore
└── README.md
```

---

## Instalação rápida

```bash
# 1. Clonar
git clone https://github.com/<SEU_USERNAME>/santos-populares-2026.git
cd santos-populares-2026

# 2. Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Correr o dashboard
streamlit run app.py
```

O browser abre automaticamente em `http://localhost:8501`.

---

## Atualizar os dados (xlsx)

O dashboard foi desenhado para aceitar versões atualizadas da agenda sem alterar código.

### Passo a passo

1. Obtém o novo ficheiro Excel atualizado.
2. **Verifica que o formato está correto** (ver secção abaixo).
3. Substitui `data/santos.xlsx` pelo novo ficheiro:
   ```bash
   cp ~/Downloads/santos_2027.xlsx data/santos.xlsx
   ```
4. (Opcional) Corre os testes para confirmar que o ficheiro é válido:
   ```bash
   pytest tests/ -v
   ```
5. Reinicia o Streamlit — os dados são recarregados automaticamente (cache TTL: 1 hora).  
   Para forçar recarga imediata: abre o menu ⋮ no canto superior direito → **Clear cache**.

### Formato esperado do Excel

| Requisito | Detalhe |
|---|---|
| Coluna `Dia` | Datas em português: `"16 de maio"`, `"10 de junho (Feriado)"` |
| Coluna `Dia da Semana` | Nome do dia em português minúsculas: `"sábado"` |
| Restantes colunas | Uma coluna por local/arraial |
| Células | Nome do artista ou evento; múltiplos por célula separados por nova linha |
| Células vazias | OK — são ignoradas |

> **Nota:** O app deteta automaticamente a linha de cabeçalho procurando pela célula com valor `"Dia"`.  
> Não é necessário que seja a primeira linha do ficheiro.

---

## Testes

```bash
pip install pytest
pytest tests/ -v
```

Os testes verificam:
- Existência do ficheiro `data/santos.xlsx`
- Presença da coluna `Dia`
- Parsing correto de datas em português
- Pelo menos uma coluna de local
- Ficheiro não vazio

---

## Deploy (Streamlit Community Cloud)

1. Faz fork/push para o teu GitHub.
2. Vai a [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Seleciona o repositório, branch `main`, ficheiro `app.py`.
4. Deploy — a app fica pública e gratuita.

> Para atualizar os dados na cloud: faz commit do novo `data/santos.xlsx` e faz push.  
> O Streamlit Cloud faz redeploy automaticamente.

---

## Dependências

| Pacote | Versão mínima | Uso |
|---|---|---|
| `streamlit` | 1.35 | Interface web e componentes |
| `pandas` | 2.2 | Leitura e transformação do Excel |
| `plotly` | 5.22 | Gráficos interativos |
| `openpyxl` | 3.1.2 | Engine de leitura de `.xlsx` |
| `numpy` | 1.26 | Operações vetoriais |

---

## Licença

MIT — usa, modifica e distribui livremente.

---

*Boas festas Lisboa!* 🎉
