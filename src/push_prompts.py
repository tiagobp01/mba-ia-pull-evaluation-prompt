"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt no hub (ex: username/prompt_name)
        prompt_data: Dados do prompt (contendo system_prompt e user_prompt)

    Returns:
        True se sucesso, False caso contrário
    """
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return False

    try:
        print(f"Enviando prompt '{prompt_name}' ao hub...")
        
        system_prompt = prompt_data.get("system_prompt", "")
        user_prompt = prompt_data.get("user_prompt", "")
        
        # Constrói o ChatPromptTemplate
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])
        
        # Adiciona metadados
        prompt_template.metadata = {
            "description": prompt_data.get("description", ""),
            "version": prompt_data.get("version", ""),
            "techniques_applied": prompt_data.get("techniques_applied", []),
            "tags": prompt_data.get("tags", [])
        }
        
        # Faz o push
        hub.push(prompt_name, prompt_template, new_repo_is_public=True)
        print(f"   ✓ Prompt '{prompt_name}' publicado com sucesso no LangSmith Hub!")
        return True
    except Exception as e:
        print(f"   ❌ Erro ao enviar prompt: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    return validate_prompt_structure(prompt_data)


def main():
    """Função principal"""
    username = os.getenv("USERNAME_LANGSMITH_HUB")
    if not username:
        print("❌ USERNAME_LANGSMITH_HUB não configurada no .env")
        return 1
        
    prompt_file = "prompts/bug_to_user_story_v2.yml"
    data = load_yaml(prompt_file)
    if not data:
        print(f"❌ Falha ao carregar {prompt_file}")
        return 1
        
    prompt_data = data.get("bug_to_user_story_v2")
    if not prompt_data:
        print(f"❌ Chave 'bug_to_user_story_v2' não encontrada no arquivo {prompt_file}")
        return 1
        
    print_section_header("VALIDANDO PROMPT OTIMIZADO")
    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ Prompt inválido:")
        for err in errors:
            print(f"   - {err}")
        return 1
    print("   ✓ Prompt válido!")
    
    prompt_name = f"{username}/bug_to_user_story_v2"
    success = push_prompt_to_langsmith(prompt_name, prompt_data)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
