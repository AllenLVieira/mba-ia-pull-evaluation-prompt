# Modelo: gemini-flash-lite-latest substitui gemini-2.5-flash-lite

Supera a ADR-0001. `gemini-2.5-flash-lite` e o fallback `gemini-2.5-flash` retornam 404
("no longer available to new users") na API do Google — indisponíveis para chaves novas,
não é problema de configuração. Testamos as alternativas citadas no INFO.md e no próprio
Google AI Studio: `gemini-flash-lite-latest` e `gemini-3.1-flash-lite` respondem normalmente
(`invoke` real, resposta OK). Adotamos `gemini-flash-lite-latest` — mesma faixa de custo/limite
do lite original, sem exigir troca de família de modelo. `LLM_PROVIDER=google`,
`LLM_MODEL`/`EVAL_MODEL=gemini-flash-lite-latest` em `.env` e `.env.example`.
