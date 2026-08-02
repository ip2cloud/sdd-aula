# Auditor de NF-e

Scaffold de verificação da Fase 1. A implementação começa em `F1-01`, conforme `tasks.md`.

## Verificação

```bash
python -m ruff check src tests
python -m pytest -q
python -m pytest -m aceitacao -v
python verificar.py
git status --short
```
