"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

PROMPT_NAME = "leonanluppi/bug_to_user_story_v1"
OUTPUT_PATH = "prompts/bug_to_user_story_v1.yml"

# Metadados descritivos do prompt v1: não fazem parte do template em si
# (hub.pull retorna só as mensagens), então ficam fixos aqui.
DESCRIPTION = "Prompt para converter relatos de bugs em User Stories"
VERSION = "v1"
TAGS = ["bug-analysis", "user-story", "product-management"]


def pull_prompts_from_langsmith() -> dict:
    """
    Faz pull do prompt `bug_to_user_story_v1` do LangSmith Hub.

    Returns:
        Dicionário no formato aceito por `save_yaml`, com o prompt aninhado
        sob a chave `bug_to_user_story_v1` (mesmo esquema do arquivo local).

    Raises:
        Exception: se o prompt não for encontrado ou a conexão falhar.
    """
    print(f"   Puxando prompt do LangSmith Hub: {PROMPT_NAME}")

    try:
        prompt_template = hub.pull(PROMPT_NAME)
    except Exception as e:
        error_msg = str(e).lower()

        if "not found" in error_msg or "404" in error_msg:
            raise Exception(
                f"Prompt '{PROMPT_NAME}' não encontrado no LangSmith Hub.\n"
                f"Verifique se o nome do prompt está correto e se ele está publicado em:\n"
                f"  https://smith.langchain.com/hub/{PROMPT_NAME}"
            ) from e
        raise

    system_prompt = ""
    user_prompt = ""

    for message in prompt_template.messages:
        content = message.prompt.template if hasattr(message, "prompt") else ""

        if isinstance(message, SystemMessagePromptTemplate):
            system_prompt = content
        elif isinstance(message, HumanMessagePromptTemplate):
            user_prompt = content

    prompt_key = PROMPT_NAME.split("/")[-1]

    data = {
        prompt_key: {
            "description": DESCRIPTION,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "version": VERSION,
            "tags": TAGS,
        }
    }

    print(f"   ✓ Prompt carregado com sucesso")
    return data


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPT DO LANGSMITH HUB")

    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return 1

    try:
        data = pull_prompts_from_langsmith()
    except Exception as e:
        print(f"\n❌ Erro ao puxar prompt do LangSmith Hub: {e}\n")
        print("Verifique:")
        print("- LANGSMITH_API_KEY está configurada corretamente no .env")
        print("- Você tem acesso ao workspace do LangSmith")
        print("- Sua conexão com a internet está funcionando")
        return 1

    if not save_yaml(data, OUTPUT_PATH):
        print(f"❌ Falha ao salvar prompt em {OUTPUT_PATH}")
        return 1

    print(f"✓ Prompt salvo em {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
