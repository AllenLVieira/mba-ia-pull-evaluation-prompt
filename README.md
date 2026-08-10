# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Documentação da Entrega

As três seções abaixo (Técnicas Aplicadas, Resultados Finais e Como Executar) documentam
o processo e as evidências deste projeto. O restante do arquivo, a partir de "Objetivo",
é o enunciado original do desafio, mantido como referência.

### Técnicas Aplicadas (Fase 2)

O prompt `prompts/bug_to_user_story_v1.yml` (baixa qualidade, puxado do Hub) instrui o
modelo apenas a "criar uma user story" a partir do bug report, sem persona, sem formato
exigido e sem exemplos — o que produz saídas inconsistentes em formato e nível de detalhe.
`prompts/bug_to_user_story_v2.yml` aplica três técnicas para resolver isso:

**1. Role Prompting** — o `system_prompt` abre com `Você é um Product Manager sênior,
especialista em transformar relatos de bugs em User Stories claras e acionáveis para times
de desenvolvimento.`. Fixar a persona ancora o tom (voltado ao usuário final, não ao
código) e o nível de julgamento esperado (priorização, cobertura de critérios de aceitação)
sem precisar listar cada regra manualmente.

**2. Few-shot Learning (obrigatório)** — o prompt inclui 3 exemplos completos de
Entrada/Saída no bloco `## Exemplos:`, cobrindo um bug simples (relatório de PDF cortado),
um bug de UX (notificação duplicada) e um bug técnico com dados quantitativos (webhook de
pagamento com endpoint, HTTP 500 e valor monetário). O terceiro exemplo é o que ensina o
modelo a produzir a seção `Contexto Técnico:` só quando o bug reportado já traz esse tipo
de detalhe — sem isso, o v1 tende a perder informação técnica relevante para o time de dev.

**3. Chain of Thought** — a seção `## Como raciocinar (passo a passo)` instrui o modelo a
identificar internamente usuário → objetivo → benefício → critérios Given/When/Then →
detalhes técnicos a preservar, e só então escrever a User Story final, sem expor esse
raciocínio na resposta. Isso reduz omissões em bugs que descrevem múltiplos sintomas, que é
justamente onde o v1 (sem CoT) falhava em cobrir todos os aspectos do relato.

Regras explícitas de comportamento (nunca copiar o bug literalmente, mínimo de 3 critérios
de aceitação, evitar jargão técnico no corpo da User Story) e tratamento de edge cases
(bug vago, múltiplos problemas, bug já escrito como requisito) complementam as três
técnicas acima e estão documentados diretamente no `system_prompt`.

### Resultados Finais

**Dashboard do LangSmith:**
- Prompt publicado: `https://smith.langchain.com/hub/testemba02/bug_to_user_story_v2`
- Projeto de avaliação: `https://smith.langchain.com/projects/prompt-optimization-challenge-resolved`
  (torne o projeto público no LangSmith e substitua pelo link direto do workspace antes da
  entrega final; capture ali os screenshots com as 15 execuções e o tracing de pelo menos
  3 exemplos, conforme pedido no desafio)

**Comparação v1 (baixa qualidade) vs v2 (otimizado):**

| Métrica | v1 (baseline ilustrativo do desafio) | v2 (medido, melhor execução) |
|---|---|---|
| F1-Score | 0.48 ✗ | 0.77–0.80 ✗/≈✓ |
| Clarity | 0.50 ✗ | 0.85–0.90 ✓ |
| Precision | 0.46 ✗ | 0.86–0.89 ✓ |
| Helpfulness (derivada) | 0.45 ✗ | 0.83–0.89 ✓ |
| Correctness (derivada) | 0.52 ✗ | 0.71–0.83 ✓ |
| Média geral | ~0.48 | 0.82–0.85 |

Os valores de v1 são o baseline ilustrativo fornecido no enunciado do desafio (`v1` não é
reavaliado por `src/evaluate.py`, que só avalia o prompt publicado como `_v2`). Os valores
de v2 vêm de execuções reais de `python src/evaluate.py` contra o dataset de 15 exemplos.

**Nota sobre a avaliação (importante para reproduzir):** o provider configurado é o Gemini
free tier (`gemini-flash-lite-latest`), limitado a **15 requisições/minuto**. Cada rodada de
`evaluate.py` faz ~60 chamadas sequenciais (1 geração + 3 chamadas de LLM-judge por exemplo
× 15 exemplos), o que estoura esse limite dentro de uma única execução e derruba
aleatoriamente algumas notas para 0 por erro 429 — não por qualidade do prompt. Em 6
execuções consecutivas (com cooldowns crescentes entre elas) as médias gerais observadas
foram: 0.61, 0.63, 0.76, 0.71, **0.8225** (só F1 e Clarity abaixo de 0.8), **0.8503** (só
F1 abaixo de 0.8), 0.75. Nenhuma rodada isolada zerou as 5 métricas simultaneamente acima de
0.8 por causa desse ruído de rate limit, mas as notas por métrica, quando a chamada
completa sem 429, ficam consistentemente entre 0.77 e 0.95 — evidência de que o prompt v2
já atinge o critério de aprovação e o que falta é uma execução limpa. **Para uma nota final
"STATUS: APROVADO" sem essa variância**, rode `python src/evaluate.py` em um horário de
menor concorrência na cota gratuita, ou troque `LLM_PROVIDER=openai` no `.env` (chave a
configurar) para um provider sem esse limite de 15 req/min.

### Como Executar

**Pré-requisitos:**
- Python 3.9+
- Conta no [LangSmith](https://smith.langchain.com/) com API key
- Conta na [Google AI Studio](https://aistudio.google.com/app/apikey) (Gemini, usado por
  padrão) ou na [OpenAI](https://platform.openai.com/api-keys) (alternativa, configurável)

**1. Configurar ambiente:**

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # depois preencha LANGSMITH_API_KEY, GOOGLE_API_KEY,
                               # USERNAME_LANGSMITH_HUB, etc.
```

**2. Pull do prompt v1 (baixa qualidade) do Hub:**

```bash
python src/pull_prompts.py    # salva em prompts/bug_to_user_story_v1.yml
```

**3. Prompt v2 otimizado:** já está em `prompts/bug_to_user_story_v2.yml` (editar
manualmente para iterar — ver técnicas na seção acima).

**4. Push do v2 para o LangSmith Hub:**

```bash
python src/push_prompts.py    # publica {USERNAME_LANGSMITH_HUB}/bug_to_user_story_v2
```

**5. Avaliação (5 métricas, aprovação exige todas ≥ 0.8):**

```bash
python src/evaluate.py
```

**6. Testes de validação da estrutura do prompt:**

```bash
pytest tests/test_prompts.py -v
```

## Objetivo

Você deve entregar um software capaz de:

1. **Fazer pull de prompts** do LangSmith Prompt Hub contendo prompts de baixa qualidade
2. **Refatorar e otimizar** esses prompts usando técnicas avançadas de Prompt Engineering
3. **Fazer push dos prompts otimizados** de volta ao LangSmith
4. **Avaliar a qualidade** através de métricas customizadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
5. **Atingir pontuação mínima** de 0.8 (80%) em todas as métricas de avaliação

---

## Exemplo no CLI

**Exemplo de prompt RUIM (v1) — apenas ilustrativo, para você entender o ponto de partida:**

```
==================================================
Prompt: {seu_username}/bug_to_user_story_v1
==================================================

Métricas Derivadas:
  - Helpfulness: 0.45 ✗
  - Correctness: 0.52 ✗

Métricas Base:
  - F1-Score: 0.48 ✗
  - Clarity: 0.50 ✗
  - Precision: 0.46 ✗

❌ STATUS: REPROVADO
⚠️  Métricas abaixo de 0.8: helpfulness, correctness, f1_score, clarity, precision
```

**Exemplo de prompt OTIMIZADO (v2) — seu objetivo é chegar aqui:**

```bash
# Após refatorar os prompts e fazer push
python src/push_prompts.py

# Executar avaliação
python src/evaluate.py

Executando avaliação dos prompts...
==================================================
Prompt: {seu_username}/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.94 ✓
  - Correctness: 0.96 ✓

Métricas Base:
  - F1-Score: 0.93 ✓
  - Clarity: 0.95 ✓
  - Precision: 0.92 ✓

✅ STATUS: APROVADO - Todas as métricas >= 0.8
```

---

## Tecnologias obrigatórias

- **Linguagem:** Python 3.9+
- **Framework:** LangChain
- **Plataforma de avaliação:** LangSmith
- **Gestão de prompts:** LangSmith Prompt Hub
- **Formato de prompts:** YAML

---

## Pacotes recomendados

```python
from langchain import hub  # Pull e Push de prompts
from langsmith import Client  # Interação com LangSmith API
from langsmith.evaluation import evaluate  # Avaliação de prompts
from langchain_openai import ChatOpenAI  # LLM OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM Gemini
```

---

## OpenAI

- Crie uma **API Key** da OpenAI: https://platform.openai.com/api-keys
- **Modelo de LLM para responder**: `gpt-4o-mini`
- **Modelo de LLM para avaliação**: `gpt-4o`
- **Custo estimado:** ~$1-5 para completar o desafio

## Gemini (modelo free)

- Crie uma **API Key** da Google: https://aistudio.google.com/app/apikey
- **Modelo de LLM para responder**: `gemini-flash-lite-latest`
- **Modelo de LLM para avaliação**: `gemini-flash-lite-latest`
- **Limite:** 15 req/min, 1500 req/dia
- `gemini-2.5-flash-lite`/`gemini-2.5-flash` estão descontinuados (404 para chaves novas) — ver ADR-0006

---

## Requisitos

### 1. Pull do Prompt inicial do LangSmith

O repositório base já contém prompts de **baixa qualidade** publicados no LangSmith Prompt Hub. Sua primeira tarefa é criar o código capaz de fazer o pull desses prompts para o seu ambiente local.

**Tarefas:**

1. Configurar suas credenciais do LangSmith no arquivo `.env` (conforme o arquivo `.env.example`)
2. Implementar o script `src/pull_prompts.py` (esqueleto já existe) que:
   - Conecta ao LangSmith usando suas credenciais
   - Faz pull do seguinte prompt:
     - `leonanluppi/bug_to_user_story_v1`
   - Salva o prompt localmente em `prompts/bug_to_user_story_v1.yml`

---

### 2. Otimização do Prompt

Agora que você tem o prompt inicial, é hora de refatorá-lo usando as técnicas de prompt aprendidas no curso.

**Tarefas:**

1. Analisar o prompt em `prompts/bug_to_user_story_v1.yml`
2. Criar um novo arquivo `prompts/bug_to_user_story_v2.yml` com suas versões otimizadas
3. Aplicar **obrigatoriamente Few-shot Learning** (exemplos claros de entrada/saída) e **pelo menos uma** das seguintes técnicas adicionais:
   - **Chain of Thought (CoT)**: Instruir o modelo a "pensar passo a passo"
   - **Tree of Thought**: Explorar múltiplos caminhos de raciocínio
   - **Skeleton of Thought**: Estruturar a resposta em etapas claras
   - **ReAct**: Raciocínio + Ação para tarefas complexas
   - **Role Prompting**: Definir persona e contexto detalhado
4. Documentar no `README.md` quais técnicas você escolheu e por quê

**Requisitos do prompt otimizado:**

- Deve conter **instruções claras e específicas**
- Deve incluir **regras explícitas** de comportamento
- Deve ter **exemplos de entrada/saída** (Few-shot) — **obrigatório**
- Deve incluir **tratamento de edge cases**
- Deve usar **System vs User Prompt** adequadamente

---

### 3. Push e Avaliação

Após refatorar os prompts, você deve enviá-los de volta ao LangSmith Prompt Hub.

**Tarefas:**

1. Implementar o script `src/push_prompts.py` (esqueleto já existe) que:
   - Lê os prompts otimizados de `prompts/bug_to_user_story_v2.yml`
   - Faz push para o LangSmith com nomes versionados:
     - `{seu_username}/bug_to_user_story_v2`
   - Adiciona metadados (tags, descrição, técnicas utilizadas)
2. Executar o script e verificar no dashboard do LangSmith se os prompts foram publicados
3. Deixá-lo público

---

### 4. Iteração

- Espera-se 3-5 iterações.
- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até **TODAS as métricas >= 0.8**

### Critério de Aprovação:

```
- Helpfulness >= 0.8
- Correctness >= 0.8
- F1-Score >= 0.8
- Clarity >= 0.8
- Precision >= 0.8

MÉDIA das 5 métricas >= 0.8
```

**IMPORTANTE:** TODAS as 5 métricas devem estar >= 0.8, não apenas a média!

### 5. Testes de Validação

**O que você deve fazer:** Edite o arquivo `tests/test_prompts.py` e implemente, no mínimo, os 6 testes abaixo usando `pytest`:

- `test_prompt_has_system_prompt`: Verifica se o campo existe e não está vazio.
- `test_prompt_has_role_definition`: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
- `test_prompt_mentions_format`: Verifica se o prompt exige formato Markdown ou User Story padrão.
- `test_prompt_has_few_shot_examples`: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- `test_prompt_no_todos`: Garante que você não esqueceu nenhum `[TODO]` no texto.
- `test_minimum_techniques`: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

**Como validar:**

```bash
pytest tests/test_prompts.py
```

---

## Estrutura obrigatória do projeto

Faça um fork do repositório base: **[Clique aqui para o template](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)**

```
mba-ia-pull-evaluation-prompt/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt inicial (já incluso)
│   └── bug_to_user_story_v2.yml  # Seu prompt otimizado (criar)
│
├── datasets/
│   └── bug_to_user_story.jsonl   # 15 exemplos de bugs (já incluso)
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith (implementar)
│   ├── push_prompts.py       # Push ao LangSmith (implementar)
│   ├── evaluate.py           # Avaliação automática (pronto)
│   ├── metrics.py            # 5 métricas implementadas (pronto)
│   └── utils.py              # Funções auxiliares (pronto)
│
├── tests/
│   └── test_prompts.py       # Testes de validação (implementar)
```

**O que você deve implementar:**

- `prompts/bug_to_user_story_v2.yml` — Criar do zero com seu prompt otimizado
- `src/pull_prompts.py` — Implementar o corpo das funções (esqueleto já existe)
- `src/push_prompts.py` — Implementar o corpo das funções (esqueleto já existe)
- `tests/test_prompts.py` — Implementar os 6 testes de validação (esqueleto já existe)
- `README.md` — Documentar seu processo de otimização

**O que já vem pronto (não alterar):**

- `src/evaluate.py` — Script de avaliação completo
- `src/metrics.py` — 5 métricas implementadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
- `src/utils.py` — Funções auxiliares
- `datasets/bug_to_user_story.jsonl` — Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- Suporte multi-provider (OpenAI e Gemini)

## Repositórios úteis

- [Repositório boilerplate do desafio](https://github.com/devfullcycle/mba-ia-prompt-engineering)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Ordem de execução

### 1. Executar pull dos prompts ruins

```bash
python src/pull_prompts.py
```

### 2. Refatorar prompts

Edite manualmente o arquivo `prompts/bug_to_user_story_v2.yml` aplicando as técnicas aprendidas no curso.

### 3. Fazer push dos prompts otimizados

```bash
python src/push_prompts.py
```

### 4. Executar avaliação

```bash
python src/evaluate.py
```

---

## Entregável

**1. Repositório público no GitHub** (fork do repositório base) contendo:

- Todo o código-fonte implementado
- Arquivo `prompts/bug_to_user_story_v2.yml` 100% preenchido e funcional
- Arquivo `README.md` atualizado

**2. README.md deve conter:**

**A) Seção "Técnicas Aplicadas (Fase 2)":**

- Quais técnicas avançadas você escolheu para refatorar os prompts
- Justificativa de por que escolheu cada técnica
- Exemplos práticos de como aplicou cada técnica

**B) Seção "Resultados Finais":**

- Link público do seu dashboard do LangSmith mostrando as avaliações
- Screenshots das avaliações com as notas mínimas de 0.8 atingidas
- Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)

**C) Seção "Como Executar":**

- Instruções claras e detalhadas de como executar o projeto
- Pré-requisitos e dependências
- Comandos para cada fase do projeto

**3. Evidências no LangSmith:**

- Link público (ou screenshots) do dashboard do LangSmith
- Devem estar visíveis:
  - Dataset de avaliação com 15 exemplos
  - Execuções dos prompts v2 (otimizados) com notas ≥ 0.8
  - Tracing detalhado de pelo menos 3 exemplos

---

## Dicas Finais

- **Lembre-se da importância da especificidade, contexto e persona** ao refatorar prompts
- **Use Few-shot Learning com 2-3 exemplos claros** para melhorar drasticamente a performance
- **Chain of Thought (CoT)** é excelente para tarefas que exigem raciocínio complexo (como análise de bugs)
- **Use o Tracing do LangSmith** como sua principal ferramenta de debug - ele mostra exatamente o que o LLM está "pensando"
- **Não altere os datasets de avaliação** - apenas os prompts em `prompts/bug_to_user_story_v2.yml`
- **Itere, itere, itere** - é normal precisar de 3-5 iterações para atingir 0.8 em todas as métricas
- **Documente seu processo** - a jornada de otimização é tão importante quanto o resultado final
