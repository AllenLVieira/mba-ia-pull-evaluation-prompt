# Otimização e Avaliação de Prompts (bug_to_user_story)

Desafio de Prompt Engineering: puxar um prompt ruim do LangSmith Hub, otimizá-lo,
publicar de volta e provar qualidade ≥ 0,8 em métricas via LLM-as-judge.

## Language

**Bug report**:
Relato de defeito em linguagem livre, entrada do prompt (variável `{bug_report}`).
_Avoid_: issue, ticket, chamado

**User story**:
Saída esperada, no formato "Como um... eu quero... para que..." + Critérios de Aceitação.
_Avoid_: tarefa, requisito

**Métricas base**:
As 3 realmente calculadas pelo `evaluate.py` via LLM-judge: F1-Score, Clarity, Precision.
_Avoid_: métricas gerais

**Métricas derivadas**:
Helpfulness = média(Clarity, Precision); Correctness = média(F1, Precision). Seguem as base.
_Avoid_: métricas calculadas

**Métricas específicas**:
As 4 funções extras em `metrics.py` (tone, acceptance, format, completeness) — NÃO usadas
pelo `evaluate.py`. Código morto para este desafio.

**Aprovação**:
F1 ≥ 0,8 E Clarity ≥ 0,8 E Precision ≥ 0,8 (as derivadas seguem). Todas, não só a média.

**Contrato do YAML v2**:
Campos no nível raiz: `description`, `version`, `system_prompt`, `user_prompt`,
`techniques_applied` (≥ 2), `tags`. É o que `validate_prompt_structure` e os testes leem.

**Âncoras dos testes**:
Strings garantidas no `system_prompt` do v2 para os testes serem estáveis: persona
"Você é um...", "Markdown" + template "Como um... eu quero... para que...", bloco
"Exemplos:"/"Entrada:"/"Saída:".

**Provider**:
Google Gemini, modelo único `gemini-flash-lite-latest` para responder e julgar
(`gemini-2.5-flash-lite` foi descontinuado — ver ADR-0006).
_Avoid_: OpenAI (considerado e descartado)
