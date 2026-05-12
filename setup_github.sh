#!/usr/bin/env bash
# Executa uma vez para inicializar o repositório local e ligar ao GitHub.
# Uso: bash setup_github.sh <SEU_USERNAME_GITHUB>

set -euo pipefail

USERNAME=${1:?"Uso: bash setup_github.sh <USERNAME_GITHUB>"}
REPO="santos-populares-2026"

echo "→ Inicializando Git..."
git init
git add .
git commit -m "feat: initial release — Santos Populares 2026 dashboard"

echo "→ Criar repositório no GitHub via gh CLI..."
gh repo create "$REPO" \
  --public \
  --description "Dashboard interativo dos Santos Populares de Lisboa 2026 — Streamlit + Plotly" \
  --source=. \
  --remote=origin \
  --push

echo ""
echo "✅ Repositório criado e publicado em:"
echo "   https://github.com/$USERNAME/$REPO"
echo ""
echo "Para atualizar os dados no futuro:"
echo "   cp ~/novo_santos.xlsx data/santos.xlsx"
echo "   git add data/santos.xlsx"
echo "   git commit -m 'data: atualizar agenda 2027'"
echo "   git push"
