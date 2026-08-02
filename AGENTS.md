# Como se trabalha aqui

## O que é este projeto

Audite todos os XMLs de NF-e de um cliente por linha de comando.  
Sinalize problemas determinísticos sem abrir os arquivos manualmente.  
Gere relatório CSV reproduzível, sem estado e sem falso positivo no lote de aceite.

## Comandos

Use Python 3.11+ na raiz.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'

python -m nfe_auditor --input tests/fixtures/xmls --output build/output --config config.example.toml
python -m pytest -q
python -m ruff check src tests
```

## Portão de verificação

Rode, nesta ordem, ao fim de todo ciclo:

```bash
python -m ruff check src tests
python -m pytest -q
python -m pytest -m aceitacao -v
python verificar.py
git status --short
```

`verificar.py` compara esperado × achado por regra nas fixtures e imprime `FASE PROVADA` ou `NÃO PASSOU`. `git status --short` detecta arquivos fora do manifesto do DESIGN. Se qualquer comando falhar, a feature não está pronta. Não afrouxe testes.

No scaffold, o portão deve rodar com testes comuns passando, todos os aceites explicitamente pulados e `verificar.py` imprimindo `FASE 1 AINDA NÃO IMPLEMENTADA` mais o próximo comando. Aceite passando antes de existir sistema é defeito do teste. Depois da F1-07, qualquer aceite pulado reprova a fase.

## Código de retorno

- `0`: execução concluída sem bloqueante.
- `1`: execução concluída com bloqueante.
- `2`: execução falhou ou as contagens não fecharam.

Não trate `1` como falha interna. Preserve o contrato em todo ambiente.

## Estrutura de pastas

- `src/nfe_auditor/`: código de produção; nunca fixtures, clientes ou configuração concreta.
- `src/nfe_auditor/rules/`: uma regra registrada por arquivo; nunca um validador central.
- `tests/`: pacotes e testes sem rede, relógio ou estado externo. O scaffold cria `tests/test_scaffold.py` para suas verificações comuns e `tests/test_phase1_acceptance.py` para os quatro aceites puláveis.
- `tests/fixtures/xmls/`: os 50 XMLs canônicos e imutáveis.
- `tests/fixtures/manifest.json`: nomes e hashes; altere só após revisão.
- `tests/fixtures/expected_phase1.json`: ocorrências aprovadas, nunca saída não validada.
- `config.example.toml`: opções externas; nunca valores embutidos.
- `build/output/`: saídas descartáveis e não versionadas.
- `prompts/`: índice e cinco prompts independentes do ciclo; nunca código ou decisões novas.
- Raiz: documentação, `verificar.py`, configuração e empacotamento; nunca módulos de produção.

## Convenções de código

- Tipifique fronteiras; use dados imutáveis; faça regras apenas devolverem ocorrências.
- Construa `Decimal` direto da string; explicite escala e arredondamento.
- Crie arquivo versionado para regra nova ou correção; registre ID, versão, escopo e severidade.
- Trate namespaces e ordene inventário, ocorrências e CSV deterministicamente.
- No CSV, use só nomes de arquivo e contagens; nunca data, horário, duração, caminho absoluto, máquina ou usuário. Mande todo dado variável apenas ao log JSON da saída padrão.
- Não exponha dado fiscal no log. Garanta `lidos = processados + ilegíveis` e continue após ilegível.
- Teste acerto, erro e falso positivo por regra usando cópias temporárias.

## O que nunca fazer

- Nunca use `float` nem altere XML de entrada.
- Nunca omita ilegível nem aborte o lote por ele.
- Nunca escreva fora da saída; entrada é somente leitura.
- Nunca fixe caminho, configuração, segredo ou dado de cliente.
- Nunca persista cache, histórico ou estado.
- Nunca antecipe fase sem mudar PRD, PLAN e tasks.
- Nunca altere PRD, AGENTS ou o manifesto de fixtures sem revisão humana; PLAN e tasks mudam apenas com evidência do ciclo.
- Nunca copie cliente para imagem, fixture, log ou erro; separe relatório e log.
- Nunca alerte sem prova; registre ambiguidades como lacuna de requisito.

## Fluxo de trabalho

Pré-condição, uma vez: o scaffold de verificação existe, commitado e passando pelo portão com os aceites pulados.

1. Em sessão nova, cole `prompts/00-retomada.md`. Para criar a pré-condição uma única vez, use `prompts/01-scaffold.md`.
2. Toda mudança entra com `prompts/02-abertura-de-ciclo.md` — `/brainstorm` ou `/define`. Nunca comece pelo código.
3. Comece pelo teste nos 50 XMLs; implemente o mínimo.
4. Rode o teste específico e cole `prompts/03-portao.md`; se falhar, volte ao iterate.
5. Com o portão aprovado, cole `prompts/04-fechamento.md` e entregue evidências e aprendizado.

## Glossário do domínio

- **Lote:** XMLs de um cliente e período numa execução.
- **Ocorrência:** resultado com regra, gravidade, arquivo e motivo.
- **Bloqueante:** ocorrência que exige ação e retorna `1`.
- **Chave de acesso:** identificador único da NF-e presente em `infNFe/@Id`.
- **Série / número:** posição na sequência fiscal (`serie` e `nNF`).
- **CFOP:** código da operação; começa com `1`, `2` ou `3` na entrada e `5`, `6` ou `7` na saída.
- **NCM:** classificação da mercadoria com exatamente 8 dígitos.
- **vProd / vNF:** valor total dos produtos / valor total da nota.
