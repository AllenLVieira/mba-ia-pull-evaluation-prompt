# Esquema do YAML v2 no nível raiz

O `v1.yml` aninha os campos sob a chave `bug_to_user_story_v1:`, mas
`utils.validate_prompt_structure` (usado no push e nos testes) lê os campos no NÍVEL RAIZ.
Decidimos que o `v2.yml` usa esquema plano na raiz (`description`, `version`,
`system_prompt`, `user_prompt`, `techniques_applied`, `tags`) para casar com a validação
existente e simplificar os testes, aceitando a inconsistência estrutural com o v1.
