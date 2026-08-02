# PRD — Conferência de XMLs de notas fiscais eletrônicas

## Problema

Todos os meses, a empresa recebe de cada cliente uma pasta com centenas de XMLs de notas fiscais eletrônicas. A conferência atual depende de planilhas e ferramentas auxiliares, mas ainda exige análise manual e é feita por amostragem. Como nem todos os documentos são verificados, arquivos inválidos, duplicidades, ausências e dados fora do padrão podem passar despercebidos.

Esses problemas costumam aparecer apenas por volta do dia 5 do fechamento, quando já há pouco ou nenhum tempo para investigá-los e tratá-los. Isso gera risco para o fechamento, retrabalho, consumo de tempo da equipe e baixa visibilidade sobre a qualidade dos documentos recebidos.

## Quem usa

O usuário principal é a equipe contábil responsável por receber e conferir os XMLs dos clientes antes do fechamento.

## O que queremos

Queremos permitir que a equipe indique uma pasta com os XMLs de um cliente, inicie a análise por comando e receba uma análise de todos os documentos, sem precisar abrir cada arquivo.

O sistema deve destacar, no mínimo:

- arquivos inválidos, corrompidos ou incompletos;
- documentos duplicados;
- possíveis ausências na sequência de documentos;
- valores, impostos ou dados cadastrais fora do padrão esperado.

O resultado deve ser um relatório que possa ser guardado e compartilhado. Os alertas devem ser classificados por gravidade, indicar o arquivo relacionado e explicar, em linguagem clara, por que foram sinalizados.

O sistema deve apoiar a tomada de decisão da equipe. A avaliação e o tratamento de cada alerta continuam sob responsabilidade de uma pessoa.

## Sucesso (com números)

A primeira versão será considerada bem-sucedida quando:

- analisar 100% dos XMLs presentes na pasta indicada para cada cliente;
- concluir a análise em até 5 minutos por cliente;
- encontrar 100% dos problemas conhecidos no lote de teste;
- não gerar nenhum alerta indevido para uma nota íntegra.

Os dois últimos itens são critérios de aceite absolutos, não metas aproximadas. Se um problema conhecido não for encontrado ou uma nota íntegra gerar alerta indevido, a entrega não será aceita. Falsos positivos são especialmente críticos porque levam o analista a gastar tempo em uma conferência desnecessária e reduzem sua confiança no sistema.

A portabilidade também é um critério de aceite: o mesmo comando deve funcionar na máquina do analista e no contêiner, mudando apenas o caminho da pasta. Se for necessário alterar o código, a entrega não será aceita.

## Restrições

- A primeira versão deve funcionar por linha de comando no computador do usuário.
- O usuário deve indicar uma pasta de entrada e iniciar a análise.
- A análise deve funcionar sem que o usuário precise abrir os XMLs individualmente.
- O resultado precisa ser compreensível pela equipe contábil e explicar o motivo de cada alerta.
- O sistema deve preservar os arquivos recebidos, sem alterá-los.
- O relatório deve ser gravado na pasta de saída indicada.
- Nenhum caminho pode estar fixado no código.
- Nenhuma configuração pode estar embutida no código.
- O funcionamento não pode depender de interface gráfica.
- O sistema não pode escrever fora das pastas de entrada e saída indicadas.
- O código de retorno deve ser `0` quando não houver problema bloqueante, `1` quando houver problema bloqueante e `2` quando a própria análise falhar.
- O registro da execução deve ser apresentado na saída padrão.

## Como o sistema é entregue e operado

O sistema será entregue e operado em três estágios, preservando o mesmo comando e o mesmo comportamento:

### E1 — Local

O analista executa um comando na própria máquina, informa as pastas de entrada e saída e inicia a análise. Esta é a forma de operação da primeira versão.

### E2 — Empacotado

O sistema é entregue como uma imagem de contêiner, sem exigir a instalação de seus componentes diretamente na máquina do usuário.

### E3 — Produção

O contêiner é executado de forma agendada, com as pastas de entrada e saída disponibilizadas como volumes. A execução mantém os mesmos códigos de retorno e registros na saída padrão, permitindo acompanhamento operacional.

O fluxo de operação será:

1. O usuário reúne os XMLs de um cliente em uma pasta.
2. O usuário executa o comando, indicando as pastas de entrada e saída.
3. O sistema verifica todos os XMLs recebidos e identifica situações que exigem atenção.
4. O sistema grava na pasta de saída um relatório com os alertas classificados por gravidade, o arquivo relacionado e o motivo de cada alerta.
5. O usuário consulta, arquiva ou compartilha o relatório para apoiar o tratamento das ocorrências.

## Fora de escopo

Não fazem parte da primeira versão:

- corrigir ou alterar XMLs automaticamente;
- transmitir documentos ou se comunicar com órgãos fiscais;
- integrar-se ao sistema contábil existente;
- enviar mensagens diretamente aos clientes;
- decidir automaticamente qual providência deve ser tomada diante de um alerta;
- executar o tratamento fiscal ou contábil dos problemas encontrados;
- oferecer interface gráfica, tela de resumo, pesquisa ou filtros;
- receber pastas compactadas por envio;
- detectar comportamentos incomuns por comparação com outros documentos do cliente;
- manter ou consultar histórico para detecção de anomalias.

A detecção de comportamentos incomuns e anomalias poderá ser reconsiderada em uma versão futura.

## Perguntas em aberto

- Quais regras definem valores, impostos e dados cadastrais fora do padrão esperado?
- Como identificar possíveis ausências de documentos quando a sequência esperada não estiver disponível nos arquivos recebidos?
- Quais níveis de gravidade serão usados e quais situações pertencem a cada nível?
- Qual é o volume máximo esperado de arquivos e de tamanho por pasta?
- Por quanto tempo os resultados e os relatórios devem permanecer disponíveis?
- Como serão montados e aprovados o lote de teste, os problemas conhecidos e as notas íntegras usados nos critérios de aceite?
- Qual formato de relatório será necessário para compartilhamento e arquivamento?
- Quem será responsável por agendar e acompanhar a execução em produção?
