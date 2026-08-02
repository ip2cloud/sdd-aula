Quando usar: ao fim de toda iteração e antes de considerar uma feature pronta.
Pré-condição: existe uma mudança ou um scaffold a verificar, e AGENTS.md define o estágio esperado do aceite.
Não faz: não corrige código, não contorna testes, não muda expectativas, não faz ship e não amplia escopo.

Verifique a mudança atual sem alterar arquivos.

Leia integralmente AGENTS.md para interpretar o portão, tasks.md para o critério da tarefa ativa, PLAN.md para os contratos técnicos e PRD.md para os critérios absolutos. Se a tarefa ativa não estiver explícita nem puder ser determinada pelo estado, pergunte seu ID antes de continuar.

Rode exatamente nesta ordem, sem omitir nem combinar comandos:

python -m ruff check src tests
python -m pytest -q
python -m pytest -m aceitacao -v
python verificar.py
git status --short

Para cada comando, informe código de retorno e resumo da saída. Interprete os aceites conforme AGENTS.md: no scaffold, devem estar explicitamente pulados e nunca aprovados; depois da F1-07, qualquer aceite pulado reprova a fase. Interprete verificar.py como `FASE 1 AINDA NÃO IMPLEMENTADA` no scaffold, `FASE PROVADA` no aceite concluído ou `NÃO PASSOU` em reprovação. Use `git status --short` para apontar arquivo fora do manifesto da tarefa.

Se um comando falhar ou o resultado não corresponder ao estágio, declare `FEATURE NÃO PRONTA`, identifique a causa verificável e mande voltar ao iterate; não vá ao ship. Só declare `PORTÃO APROVADO` quando os cinco comandos e o critério do tasks.md forem satisfeitos.

Cite a origem das restrições: PRD.md para produto, PLAN.md para decisões, tasks.md para aceite e AGENTS.md para procedimento. Se a interpretação depender de informação ausente, pergunte; não suponha nem invente requisito.
