# Contributing

Contribuições são bem-vindas! Segue estes passos:

## Fluxo de trabalho

1. Faz fork do repositório
2. Cria uma branch: `git checkout -b feat/nova-funcionalidade`
3. Faz as alterações e corre os testes: `pytest tests/ -v`
4. Commit com mensagem descritiva (ver convenção abaixo)
5. Push e abre um Pull Request para `main`

## Convenção de commits

```
feat: adicionar filtro por distrito
fix: corrigir parsing de datas com acento
docs: atualizar README com instruções de deploy
refactor: extrair lógica de normalização para utils.py
test: adicionar teste para células com múltiplos artistas
```

## Atualizar dados

Para atualizar o ficheiro Excel com uma nova edição dos Santos Populares,
segue as instruções em [README.md → Atualizar os dados](README.md#atualizar-os-dados-xlsx).

## Reportar bugs

Abre uma [Issue](../../issues/new) com:
- Descrição do problema
- Passos para reproduzir
- Versão do Python e do Streamlit (`pip show streamlit`)
