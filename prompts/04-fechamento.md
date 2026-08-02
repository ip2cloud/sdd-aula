Quando usar: depois de o portão declarar PORTÃO APROVADO para uma tarefa ou grupo.
Pré-condição: há evidência dos cinco comandos aprovados e do critério de pronto observado nos 50 XMLs.
Não faz: não acrescenta funcionalidade, não corrige código, não altera fonte protegida sem revisão humana e não inventa mecanismo de arquivo.

Feche o ciclo atual. Se o ID da tarefa ou os IDs do grupo não estiverem explícitos nem puderem ser determinados pela evidência do portão, pergunte-os e espere a resposta.

Leia integralmente PRD.md, PLAN.md, tasks.md e AGENTS.md. Confirme que o portão resultou em `PORTÃO APROVADO` e que o critério de pronto dos IDs foi observado. Se não houver evidência, pare e mande voltar ao iterate; não faça ship.

1. Resuma o entregue por ID, arquivos alterados, comandos, códigos de retorno e resultados nos 50 XMLs.
2. Registre apenas aprendizado verificável: decisão confirmada, risco descoberto, hipótese invalidada e efeito nas próximas tarefas.
3. Atualize PLAN.md somente se arquitetura, decisão, risco ou premissa mudou. Atualize tasks.md somente para estado, dependência ou critério afetado pela evidência.
4. Não altere PRD.md, AGENTS.md nem tests/fixtures/manifest.json sem revisão humana explícita, conforme proteção definida no AGENTS.md.
5. Arquive a feature somente pelo mecanismo já documentado. Se não houver mecanismo definido, pergunte onde registrar; não crie pasta, formato, commit ou convenção.
6. Mostre o diff documental proposto e peça revisão antes de modificar fonte protegida.

Entregue: IDs encerrados; evidências do portão; esperado × achado por regra; aprendizado; documentos atualizados; fontes protegidas não alteradas; local do arquivo da feature.

Cite a origem de cada restrição: PRD.md para produto, PLAN.md para decisões, tasks.md para execução e AGENTS.md para procedimento. Se faltar informação, pergunte; não suponha nem invente requisito.
