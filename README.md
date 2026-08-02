## Antes de qualquer comando

```bash
source .venv/bin/activate
```

Sem isso, `python` não existe nesta máquina e todo comando falha com
`command not found`. O prompt do terminal deve mostrar `(.venv)` antes de
você rodar qualquer coisa deste projeto.

Se o `.venv` ainda não existir:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
```

# Auditor de NF-e

Auditoria determinística de XMLs de NF-e por linha de comando.

## Executar

```bash
python -m nfe_auditor \
  --input tests/fixtures/xmls \
  --output build/output \
  --config config.example.toml
```

Retornos: `0` sem bloqueante, `1` com bloqueante e `2` em falha da execução.

## Verificação

```bash
python -m ruff check src tests
python -m pytest -q
python -m pytest -m aceitacao -v
python verificar.py
git status --short
```
# sdd-aula
