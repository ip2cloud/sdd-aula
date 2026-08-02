Quando usar: antes de iniciar qualquer tarefa ou grupo paralelo do tasks.md.
Pré-condição: o scaffold está commitado e o portão está no estado esperado; a tarefa pretendida existe no tasks.md.
Não faz: não escreve código, não altera arquivos, não escolhe solução pelo usuário e não antecipa tarefa ou fase.

Abra um ciclo de trabalho. Primeiro, peça o ID da tarefa ou os IDs do grupo caso eles não estejam explícitos na conversa; faça essa pergunta sozinha e espere a resposta.

Depois, leia integralmente PRD.md, PLAN.md, tasks.md e AGENTS.md e localize os IDs. Cite a origem de cada restrição: PRD.md para valor de negócio, escopo, qualidade e portabilidade; PLAN.md para arquitetura, stack e decisões; tasks.md para arquivos, dependências e critério de pronto; AGENTS.md para convenções, proibições, fluxo e portão.

1. Verifique se as dependências estão concluídas. Se houver grupo, confirme no tasks.md que as tarefas podem rodar em paralelo; caso contrário, proponha sequência.
2. Faça perguntas uma por vez antes de propor solução. Pergunte apenas o que não puder ser descoberto no repositório e cuja resposta altere a execução.
3. Depois das respostas, apresente 2 ou 3 alternativas compatíveis com os quatro documentos, com prós, contras, arquivos afetados e riscos. Recomende uma e espere minha escolha.
4. Defina antes do código um critério verificável apoiado nos 50 XMLs, com resultados e arquivos esperados conforme tasks.md. Quando aplicável, preserve exatamente duas divergências em NFe_0004.xml e NFe_0038.xml e zero falso positivo da regra nas outras 48 notas.
5. Exponha qualquer conflito entre documentos e pergunte como resolvê-lo.

Encerre com entendimento, dependências, alternativas, recomendação, critério verificável e perguntas abertas. Não escreva código até eu escolher. Se faltar informação, pergunte; não suponha nem invente requisito.
