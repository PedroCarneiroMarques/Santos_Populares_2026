# Contributing

Contribuições são bem-vindas.

## Fluxo de trabalho

1. Faz fork do repositório
2. Cria uma branch: `git checkout -b feat/nova-melhoria`
3. Faz as alterações
4. Testa localmente com `streamlit run app.py`
5. Commit com mensagem descritiva
6. Push e abre um Pull Request para `main`

## Convenção de commits

```txt
feat: adicionar novo bloco editorial
fix: corrigir parsing de datas
docs: atualizar README e changelog
style: melhorar contraste visual do dashboard
refactor: reorganizar lógica de scoring
```

## Dados

Se alterares a origem dos dados, garante que a app continua compatível com o ficheiro Excel esperado em `data/santos.xlsx` ou com upload manual.

## Reportar bugs

Abre uma issue com:

- Descrição do problema
- Passos para reproduzir
- Print do erro, se existir
- Versão do Python
- Versão do Streamlit
