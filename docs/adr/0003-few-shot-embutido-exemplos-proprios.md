# Few-shot embutido no system_prompt com exemplos próprios

Os exemplos de Few-shot são escritos como texto dentro do `system_prompt` (não via
`FewShotChatMessagePromptTemplate`), para sobreviver ao ciclo push→hub→pull como um
`ChatPromptTemplate` simples e serem detectáveis pelos testes por string. Os exemplos são
escritos à mão e DISTINTOS dos 15 do dataset de avaliação, para evitar vazamento/overfitting
que inflaria as notas artificialmente.
