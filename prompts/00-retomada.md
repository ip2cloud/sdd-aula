Quando usar: no início de toda sessão nova, antes de alterar arquivos.
Pré-condição: PRD.md, PLAN.md, tasks.md e AGENTS.md existem na raiz do projeto.
Não faz: não instala dependências, não corrige falhas, não altera arquivos e não implementa tarefas.

Retome este projeto sem implementar nem alterar arquivos.

1. Leia integralmente PRD.md, PLAN.md, tasks.md e AGENTS.md. Use PRD.md como fonte de problema, escopo, métricas e restrições; PLAN.md como fonte de arquitetura e decisões; tasks.md como fonte da Fase 1, dependências e critérios verificáveis; e AGENTS.md como fonte do modo de trabalho e do portão.
2. Explore o estado atual do repositório e rode, nesta ordem, o portão definido no AGENTS.md:

   python -m ruff check src tests
   python -m pytest -q
   python -m pytest -m aceitacao -v
   python verificar.py
   git status --short

3. Não corrija nada e não instale o que faltar.
4. Responda somente:
   - Fase atual: cite a evidência encontrada.
   - Próxima tarefa: informe o ID e o nome exatos do tasks.md, respeitando dependências.
   - Quebrado agora: liste comandos que falharam, aceites indevidamente aprovados ou pulados para o estágio atual, veredito do verificar.py e arquivos inesperados do git status.

Cada restrição deve citar sua origem: PRD.md para produto, PLAN.md para decisões técnicas, tasks.md para execução e AGENTS.md para procedimento. Se não puder determinar uma resposta, diga qual informação falta e pergunte; não suponha nem invente requisito.
