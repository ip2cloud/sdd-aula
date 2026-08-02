# PLAN — Conferência de XMLs de notas fiscais eletrônicas

Este documento descreve o caminho técnico de alto nível para entregar o produto definido no PRD. Ele não detalha código nem divide o trabalho em tarefas.

## 1. Arquitetura em uma página

A solução será uma aplicação de linha de comando, modular e sem estado entre execuções. Ela processará uma pasta inteira, aplicará regras determinísticas por documento e sobre o lote e produzirá um relatório na pasta de saída.

```text
Comando
  ├── caminho da entrada
  ├── caminho da saída
  └── configuração externa
             │
             ▼
     Coordenador da execução
             │
             ├── inventaria todos os XMLs
             │
             ├── Leitor e normalizador ───────┐
             │       │                        │
             │       ├── XML legível          │
             │       │       ▼                │
             │       │  Regras por documento │ execução paralelizável
             │       │                        │
             │       └── XML ilegível         │
             │               ▼                │
             │       ocorrência de severidade alta
             │                                │
             └────────────────────────────────┘
                              │
                              ▼
                    Resultado dos documentos
                              │
                              ▼
                       Regras do lote
                 (duplicidades e possíveis lacunas)
                              │
                              ▼
                   Consolidador de ocorrências
                              │
               ┌──────────────┼──────────────┐
               ▼              ▼              ▼
        Relatório CSV   log estruturado   código 0/1/2
        na saída        na saída padrão
```

### Componentes

- **Interface de comando:** recebe os caminhos de entrada e saída e a localização da configuração, valida os argumentos e inicia a execução.
- **Coordenador da execução:** inventaria os arquivos, controla o fluxo, reúne as contagens e determina o código de retorno.
- **Leitor e normalizador:** lê cada XML sem alterar o original e converte seus campos para um modelo interno consistente. Valores monetários entram diretamente como números decimais exatos.
- **Registry de regras:** descobre e registra regras independentes, identifica se cada uma atua sobre um documento ou sobre o lote e garante uma assinatura única.
- **Regras por documento:** validam estrutura, campos obrigatórios, valores, impostos e dados cadastrais. Como não compartilham estado, podem ser executadas em paralelo.
- **Regras do lote:** trabalham sobre os resultados normalizados do conjunto para encontrar duplicidades e possíveis lacunas. Só começam depois da leitura dos documentos.
- **Consolidador:** ordena ocorrências de modo estável, atribui severidade e mantém a identidade do arquivo e o motivo do alerta.
- **Gerador de relatório:** grava o relatório compartilhável exclusivamente na pasta de saída.
- **Registro operacional:** escreve eventos estruturados na saída padrão, sem misturar dados operacionais com o relatório.

### Fluxo e invariantes

1. O comando valida os caminhos e carrega a configuração externa.
2. O coordenador cria um inventário fechado dos XMLs encontrados.
3. Cada arquivo é lido e normalizado uma única vez.
4. XML legível segue para todas as regras por documento; XML ilegível gera ocorrência de severidade alta e não interrompe o lote.
5. Quando todos os arquivos terminam, as regras do lote analisam apenas os dados válidos disponíveis, sem ocultar os ilegíveis.
6. O relatório é gravado na saída e as contagens são conferidas: `lidos = processados + ilegíveis`.
7. O processo termina com `0` sem ocorrência bloqueante, `1` com ocorrência bloqueante ou `2` quando a execução não consegue concluir de forma confiável.

Não há banco de dados, serviço permanente ou estado reaproveitado entre execuções.

## 2. Stack

### Linguagem e execução

- **Python 3.11 ou superior:** adequado para leitura de XML, processamento de arquivos, números decimais exatos e execução tanto local quanto em contêiner.
- **Linha de comando com a biblioteca padrão:** mantém o contrato pequeno e reduz dependências operacionais.
- **Concorrência por processos da biblioteca padrão:** opção para paralelizar regras por documento quando as medições demonstrarem necessidade, sem alterar o desenho das regras.

### Bibliotecas

- **lxml:** leitura segura e validação estrutural dos XMLs, incluindo suporte aos namespaces e esquemas da NF-e.
- **Decimal da biblioteca padrão:** representação obrigatória de todo valor monetário.
- **csv e json da biblioteca padrão:** geração do relatório e dos registros estruturados.
- **tomllib da biblioteca padrão:** leitura de configuração externa em formato TOML.
- **pytest:** testes unitários, testes por regra, testes do lote, critérios absolutos de qualidade e teste de equivalência entre execução local e contêiner.

Dependências devem ter versão fixada e finalidade explícita. Nenhuma biblioteca poderá converter valores monetários para ponto flutuante durante leitura, cálculo, comparação ou serialização.

### Entrada

- Uma pasta indicada no comando, contendo arquivos XML.
- Uma pasta de saída indicada no comando.
- Um arquivo de configuração externo, informado por argumento ou variável de ambiente.
- Os XMLs originais são somente leitura e nunca são copiados para a imagem de contêiner.

### Saída

- Um relatório CSV em UTF-8 na pasta de saída, com resumo da execução e ocorrências ordenadas de forma estável por gravidade, arquivo e regra.
- Para cada ocorrência: identificador da regra, gravidade, arquivo, motivo e dados necessários para conferência.
- Logs estruturados em JSON na saída padrão.
- Código de retorno `0`, `1` ou `2`, conforme o contrato do PRD.

## 3. Decisões

### D1 — Uma regra por arquivo, registry e assinatura única

**Contexto:** as validações fiscais e estruturais crescerão ao longo do tempo. Regras por documento precisam ser independentes para permitir testes isolados e execução paralela; regras do lote precisam usar o mesmo contrato operacional sem se misturar às primeiras.

**Escolha:** cada regra será uma função pura em seu próprio arquivo e será registrada de forma explícita em um registry. Todas obedecerão à mesma assinatura lógica: recebem um contexto imutável apropriado ao seu escopo e devolvem zero ou mais ocorrências, sem efeitos colaterais. O registry declarará ID, versão e escopo da regra. Regra nova significa arquivo novo; uma regra existente não será ampliada para absorver outro comportamento.

**Motivo:** o isolamento reduz o impacto de mudanças, torna cada regra rastreável e testável e permite paralelizar regras por documento. A assinatura única simplifica coordenação, consolidação e instrumentação.

**Alternativas rejeitadas:** um validador único com uma cadeia de condicionais, porque concentra risco; classes de regra, porque adicionam estado e cerimônia sem benefício na Fase 1; e registro automático por importação ou decorador, porque depende de efeito colateral e pode omitir silenciosamente uma regra não importada.

**Consequência:** haverá mais arquivos pequenos e o registry passa a ser um contrato central verificável. Testes provarão que toda regra esperada está registrada uma vez e é executada uma vez. Arquivos de regras existentes são imutáveis. Tanto um novo critério quanto a correção de um comportamento serão introduzidos em um novo arquivo, com nova versão ou identificação, testes próprios e troca explícita no registry.

### D2 — Valores monetários exclusivamente decimais

**Contexto:** conferências fiscais exigem igualdade monetária exata. Uma divergência criada pelo próprio sistema destrói a confiança do analista e viola o critério de zero alerta indevido.

**Escolha:** todo valor monetário será representado como `Decimal`, criado diretamente a partir da string presente no XML. O uso de `float` é proibido em todo o projeto, inclusive em testes, cálculos intermediários, comparações e geração do relatório. Na regra de total, `diferenca = vNF - soma dos vProd` preserva o sinal, mas a ocorrência é decidida por `abs(diferenca) > tolerancia`. O texto e o valor do CSV usam hífen ASCII, ponto decimal, exatamente duas casas, nenhum separador de milhar ou moeda e nenhuma dependência da localização do sistema.

**Motivo:** números decimais preservam a representação exata dos valores fiscais e permitem que regras de escala e arredondamento sejam explícitas, em vez de dependerem de aproximações binárias.

**Alternativa rejeitada:** usar `float` e arredondar no momento da comparação. Foi rejeitada porque o arredondamento mascara a origem do erro em vez de eliminá-la e pode fazer o auditor criar divergências de centavos.

**Consequência:** conversões e operações monetárias terão revisão e testes específicos. Qualquer integração futura deverá provar que preserva números decimais antes de entrar no fluxo.

### D3 — XML ilegível gera ocorrência e não interrompe o lote

**Contexto:** um lote mensal pode conter centenas de documentos e alguns podem estar corrompidos ou malformados. A rotina de fechamento precisa conhecer esses arquivos sem perder a análise dos demais.

**Escolha:** cada XML ilegível produzirá uma ocorrência de severidade alta, identificando o arquivo e o motivo possível. O processamento continuará com os demais arquivos. Ao final, a contagem deverá sempre respeitar `lidos = processados + ilegíveis`.

**Motivo:** a decisão preserva o valor da análise do lote completo, torna a falha visível e permite que o analista trate o arquivo problemático sem repetir todo o processo.

**Alternativas rejeitadas:** abortar o lote no primeiro XML ilegível, porque isso inviabiliza a rotina de fechamento; e pular o arquivo em silêncio, porque cria exatamente o erro silencioso que o produto existe para eliminar.

**Consequência:** regras por documento e do lote não poderão assumir que todos os XMLs são válidos. O relatório e o resumo operacional sempre mostrarão os totais lidos, processados e ilegíveis; divergência nessa equação será falha de execução e produzirá código de retorno `2`.

### D4 — Execução deliberadamente sem estado

**Contexto:** a arquitetura escolhida começa cada análise do zero. O escopo atual não inclui histórico nem detecção de anomalias, e o mesmo lote precisa produzir o mesmo resultado nas mesmas condições.

**Escolha:** nenhuma execução reutilizará resultados, cache ou dados de execuções anteriores. Entrada, configuração e versão das regras determinarão integralmente a saída.

**Motivo:** ausência de estado torna a execução reproduzível, simplifica auditoria e elimina contaminação por resíduos de lotes anteriores.

**Alternativa rejeitada:** manter uma base local ou cache persistente entre execuções. Foi rejeitada porque cria ciclo de vida e migração de dados, dificulta reproduzir resultados e aproxima a solução de histórico e anomalias, que estão fora do escopo.

**Consequência:** começar do zero é uma garantia desejada, não uma limitação. Reexecutar o mesmo lote com a mesma configuração e a mesma versão deverá produzir as mesmas ocorrências e a mesma ordenação; apenas informações operacionais inevitavelmente variáveis, como horário e duração, poderão mudar.

### D5 — Aplicação CLI modular em processo único

**Contexto:** o volume inicial é de centenas de XMLs por cliente, não há interface gráfica nem integração externa, e a execução deve ser idêntica na máquina e no contêiner.

**Escolha:** adotar uma aplicação CLI modular, iniciada como um único processo coordenador. A paralelização será interna e limitada às regras por documento, preservando uma única consolidação do lote.

**Motivo:** é a menor arquitetura que atende leitura, regras individuais, regras coletivas, relatório, portabilidade e códigos de retorno sem introduzir componentes operacionais desnecessários.

**Alternativas rejeitadas:** um pipeline com arquivos intermediários, porque adiciona estados e risco de resíduos; e uma base local por execução, porque acrescenta persistência sem benefício proporcional ao volume atual.

**Consequência:** o processo deve caber nos recursos de uma única máquina. Antes de aumentar a complexidade, desempenho será tratado por leitura eficiente, ausência de releitura e paralelismo controlado medido em testes.

### D6 — Relatório tabular e logs estruturados separados

**Contexto:** o analista precisa de um artefato simples para conferir e compartilhar, enquanto a operação agendada precisa de registros que possam ser coletados automaticamente.

**Escolha:** gerar `relatorio.csv` em UTF-8 na pasta de saída e emitir logs JSON na saída padrão. O cabeçalho fixo será `tipo,arquivo,regra,severidade,motivo,valor`. O resumo terá uma linha por contador, sempre na ordem `lidos`, `processados`, `ilegiveis`, `bloqueantes`, `avisos`; depois virão as ocorrências. A coluna `tipo` aceitará `resumo` e `ocorrencia`. Ocorrências registrarão somente o nome do arquivo; quando houver valor natural, `valor` conterá o dado formatado para filtro, além do motivo em prosa. Regras sem valor natural deixarão a coluna vazia. O motivo da regra de total seguirá exatamente `Total da nota {vNF} difere da soma dos produtos {soma} em {diferenca}; tolerância {tolerancia}.`

O CSV será comparável byte a byte: não conterá horário, data de execução, duração, caminho absoluto, máquina ou usuário. Todo dado variável existirá exclusivamente no log JSON. A configuração externa definirá o nome de cada severidade, se é bloqueante e seu rank numérico. Ocorrências serão ordenadas pelo rank, depois por arquivo e regra; nunca pela ordem alfabética da severidade.

**Motivo:** CSV é portátil e abre em ferramentas já usadas pela equipe, sem exigir interface gráfica da aplicação. JSON na saída padrão atende operação local e em contêiner sem arquivo de log próprio.

**Alternativas rejeitadas:** relatório HTML, por se aproximar de uma interface e exigir decisões de apresentação fora do escopo; planilha, porque o formato pode embutir metadados variáveis, como horários de criação, e impedir comparação byte a byte, quebrando a exigência de saída reproduzível; e logs em arquivo, por criar escrita operacional e rotação desnecessárias.

**Consequência:** o contrato de colunas, largura uniforme, codificação, terminadores de linha, ordenação, formatação numérica, resumo e severidades será versionado e testado por comparação byte a byte entre caminhos diferentes. Não serão adicionadas colunas específicas por regra, pois isso criaria tabela larga e esparsa; se detalhes heterogêneos se tornarem necessários na Fase 2, será avaliado um arquivo separado. Informações sensíveis não devem ser despejadas nos logs.

## 4. Fases de entrega

### Fase 1 — Primeira conferência útil

Entregar o menor fluxo completo que já reduz trabalho manual:

- comando com entrada, saída e configuração externa;
- inventário de todos os XMLs;
- leitura segura e identificação de arquivos ilegíveis;
- registry e primeira regra fiscal por documento: conferir o total da nota contra a soma dos valores dos produtos, usando tolerância decimal explícita na configuração;
- relatório CSV com gravidade, arquivo, regra e motivo;
- contagens fechando em `lidos = processados + ilegíveis`;
- códigos de retorno `0`, `1` e `2` e log estruturado na saída padrão.

Essa regra entra na Fase 1 porque trata o erro mais caro do fechamento, depende somente dos dados da própria nota e faz a primeira entrega apontar problemas reais sem exigir regras ou histórico adicionais.

O critério de aceite funcional da Fase 1 é absoluto: com a tolerância aprovada, o lote canônico de 50 XMLs deve produzir exatamente 2 ocorrências de total divergente e nenhum falso positivo da regra nas 48 notas sem divergência de total. As divergências esperadas são `NFe_0004.xml` e `NFe_0038.xml`; qualquer ocorrência adicional ou ausência de uma delas reprova a fase.

Ao final, o analista já consegue apontar uma pasta e descobrir XMLs ilegíveis e divergências reais de total sem abrir documento por documento.

### Fase 2 — Cobertura das regras por documento

Completar as regras determinísticas individuais previstas no PRD:

- integridade e estrutura dos XMLs de NF-e;
- impostos;
- dados cadastrais;
- severidades e motivos validados com a equipe contábil;
- lote de teste com problemas conhecidos e notas íntegras.

A fase termina somente quando as regras incluídas encontram 100% de seus problemas conhecidos e não geram alerta em nenhuma nota íntegra do lote de aceite.

### Fase 3 — Conferência do lote e aceite integral

Adicionar as regras que dependem do conjunto completo:

- identificação de documentos duplicados;
- identificação de possíveis lacunas, conforme critérios aprovados;
- consolidação e ordenação determinística das ocorrências;
- paralelização controlada das regras por documento, se necessária para desempenho;
- validação do limite de 5 minutos por cliente no volume acordado;
- aceite integral de qualidade, códigos de retorno, escrita restrita e reprodução da execução.

Ao final desta fase, todo o escopo funcional da primeira versão estará concluído.

### Fase 4 — Empacotamento em contêiner

Empacotar exatamente a funcionalidade aceita nas fases anteriores, sem adicionar ou alterar regras de negócio:

- imagem base slim, sem ferramenta de build no resultado final;
- processo executado sem privilégio administrativo;
- entrada e saída montadas como volumes, nunca copiadas para dentro da imagem;
- configuração montada externamente e sobrescrevível por variável de ambiente;
- nenhum dado de cliente dentro da imagem, inclusive exemplos, testes, cache ou camadas intermediárias;
- preservação do contrato de códigos `0`, `1` e `2`;
- logs estruturados na saída padrão;
- teste de que o mesmo comando roda localmente e no contêiner, mudando apenas o caminho da pasta.

A Fase 4 só será barata se as Fases 1 a 3 respeitarem desde o início os requisitos de portabilidade do PRD: caminhos externos, configuração não embutida, ausência de interface gráfica, escrita restrita e logs na saída padrão. Se o empacotamento exigir mudança de código, o critério de portabilidade falhou e a fase anterior não está aceita.

## 5. Riscos e premissas

### Riscos

- **Regras fiscais ainda indefinidas:** valores, impostos e dados cadastrais fora do padrão precisam de critérios objetivos; critérios ambíguos entram em conflito com zero falso positivo.
- **Lacunas sem universo conhecido:** uma ausência só pode ser afirmada quando houver uma sequência esperada bem definida por emitente, série, modelo e período. Sem essa referência, o alerta deve ser conservador ou a regra não deve ser ativada.
- **Lote de aceite insuficiente:** atingir 100% no lote não prova cobertura fora dele. Um lote pequeno ou pouco diverso pode criar confiança indevida.
- **Esquemas e variações de NF-e:** versões, eventos, namespaces e documentos auxiliares podem exigir delimitação explícita do que é aceito como entrada.
- **Falso positivo por configuração:** uma regra correta com parâmetro inadequado ainda pode gerar alerta indevido. Configuração precisa ser validada e identificada no relatório.
- **Paralelismo não determinístico:** concorrência pode alterar ordem de resultados ou esconder falhas se a consolidação não for estável.
- **Dados sensíveis nos registros:** logs estruturados facilitam operação, mas não devem expor conteúdo fiscal desnecessário.
- **Meta de desempenho sem volume de referência:** cinco minutos só é verificável depois de fixar quantidade e tamanho máximos do lote e capacidade mínima da máquina.
- **CSV e regionalização:** acentos, separador de campos e abertura em diferentes ferramentas podem afetar a experiência do analista; o contrato precisa ser validado com arquivos reais.
- **Nota sem itens:** a regra de total somaria zero e poderia acusar o valor integral da nota. A decisão de negócio provavelmente é alertar, mas deve ser confirmada antes da produção; não bloqueia a Fase 1 porque o caso não existe no lote de aceite.

### Premissas

- A primeira versão recebe NF-e no leiaute e nas versões explicitamente aprovados para o projeto.
- A pasta de entrada representa um lote de um cliente e um período de conferência por execução.
- Os arquivos de entrada permanecem disponíveis e somente para leitura durante toda a execução.
- A equipe contábil fornecerá regras objetivas, exemplos positivos e negativos e aprovará as severidades.
- O lote de aceite conterá todos os problemas conhecidos que a versão declara detectar e um conjunto representativo de notas íntegras.
- A mesma versão do sistema, a mesma configuração e os mesmos arquivos deverão produzir as mesmas ocorrências.
- O ambiente local e o contêiner disponibilizarão recursos suficientes para o volume máximo acordado.
- O agendador de produção tratará código `1` como lote concluído com bloqueante e código `2` como falha da execução.
