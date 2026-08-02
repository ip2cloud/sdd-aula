Quando usar: uma única vez, no bootstrap, antes de executar F1-01 do tasks.md.
Pré-condição: PRD.md, PLAN.md, tasks.md e AGENTS.md estão aprovados, e o repositório ainda não possui o scaffold de verificação.
Não faz: não implementa F1-01 a F1-08, não move os XMLs e não cria leitor, regra, CLI, relatório, manifesto ou configuração de execução.

Crie somente o scaffold de verificação deste projeto.

Leia integralmente PRD.md, PLAN.md, tasks.md e AGENTS.md antes de alterar arquivos. O estado inicial e o portão vêm do AGENTS.md; Python 3.11+ vem do PLAN.md; os quatro comportamentos de aceite vêm da Fase 1 do PLAN.md e da F1-08 do tasks.md.

Crie:

- pyproject.toml mínimo com `requires-python = ">=3.11"`, dependências de teste e lint e marcador pytest `aceitacao` registrado; não adicione lxml, pois isso pertence à F1-01 do tasks.md;
- .gitignore e README.md mínimos;
- src/nfe_auditor/__init__.py e tests/__init__.py vazios;
- um teste comum do scaffold que passe sem implementar o auditor;
- tests/test_phase1_acceptance.py com quatro testes marcados `@pytest.mark.aceitacao`: detectar exatamente NFe_0004.xml e NFe_0038.xml; gerar zero falso positivo da regra nas 48 notas sem divergência; provar que a regra é genérica adulterando em tempo de execução uma cópia temporária de nota limpa; e fechar `lidos = processados + ilegíveis`;
- verificar.py, que enquanto o sistema não existir retorna 0, imprime `FASE 1 AINDA NÃO IMPLEMENTADA` e informa como próximo comando `python -m pytest -m aceitacao -v`.

Faça cada teste de aceitação chamar `pytest.skip` com uma razão explícita enquanto o módulo necessário não existir. Não use assert vazio, resultado fabricado ou condição que faça o aceite passar. Antes da implementação, aceite passando é defeito; o resultado obrigatório é `4 skipped`. Não implemente nenhuma tarefa do tasks.md.

Inicialize o repositório antes do portão:

git init

Rode o portão nesta ordem e mostre código de retorno e saída de cada comando. Neste primeiro portão, `git status --short` deve listar os arquivos como não rastreados:

python -m ruff check src tests
python -m pytest -q
python -m pytest -m aceitacao -v
python verificar.py
git status --short

Aceite o scaffold somente se os testes comuns passarem, os quatro aceites pularem explicitamente, verificar.py disser `FASE 1 AINDA NÃO IMPLEMENTADA`, `git status --short` listar o scaffold ainda não rastreado e nenhuma tarefa do tasks.md estiver implementada.

Por fim, execute:

git add .
git commit -m "bootstrap: scaffold de verificação"

Rode novamente `git status --short`; o resultado deve estar vazio. Mostre também o hash do primeiro commit. Se faltar informação ou alguma condição exigir decisão não escrita em PRD.md, PLAN.md, tasks.md ou AGENTS.md, pare e pergunte; não suponha nem invente requisito.
