# Provider: Gemini 2.5-flash-lite como modelo único

> **Superada pela ADR-0006** — `gemini-2.5-flash-lite` foi descontinuado pela Google.

Escolhemos Google Gemini `gemini-2.5-flash-lite` para responder e avaliar (LLM-judge),
em vez de OpenAI (gpt-4o-mini + gpt-4o), pelo custo zero no free tier. Trade-off aceito:
limite ~15 RPM / 500 RPD e cada `evaluate.py` dispara ~60 chamadas (15 exemplos × 4),
dando ~8 rodadas/dia e notas um pouco mais ruidosas perto de 0,8 por ser um modelo lite
atuando como juiz. Fallback: `gemini-2.5-flash`. Mantemos `requirements.txt` intacto
(a lib 2.0.8 repassa o nome do modelo à API); só bumpamos se o smoke-test inicial falhar.
