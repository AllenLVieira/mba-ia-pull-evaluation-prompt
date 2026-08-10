# Escopo travado; arquivos congelados intactos

Implementamos apenas 5 arquivos: `src/pull_prompts.py`, `src/push_prompts.py`,
`tests/test_prompts.py`, `prompts/bug_to_user_story_v2.yml` e `README.md`. Não tocamos em
`evaluate.py`, `metrics.py`, `utils.py` nem no dataset (proibido pelo INFO.md). O `.env.example`
é template editável e será atualizado para `gemini-2.5-flash-lite`; o pull sobrescreve
`prompts/bug_to_user_story_v1.yml` com a versão fiel do Hub, conforme a tarefa 1 do INFO.md.
