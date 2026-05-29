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
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith() -> bool:
    """
    Faz pull do prompt do LangSmith Hub e salva localmente.
    """
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return False

    print_section_header("PULL PROMPT FROM LANGSMITH HUB")
    
    prompt_name = "leonanluppi/bug_to_user_story_v1"
    output_path = "prompts/bug_to_user_story_v1.yml"
    
    try:
        print(f"Puxando prompt '{prompt_name}' do hub...")
        prompt = hub.pull(prompt_name)
        print("   ✓ Prompt puxado com sucesso")
        
        # Extrair system_prompt e user_prompt
        system_prompt = ""
        user_prompt = ""
        
        from langchain_core.prompts import ChatPromptTemplate
        if isinstance(prompt, ChatPromptTemplate):
            for msg in prompt.messages:
                msg_type = type(msg).__name__
                if "System" in msg_type:
                    system_prompt = msg.prompt.template
                elif "Human" in msg_type or "User" in msg_type:
                    user_prompt = msg.prompt.template
        else:
            # Fallback para PromptTemplate
            system_prompt = getattr(prompt, "template", str(prompt))
            user_prompt = ""
            
        prompt_data = {
            "bug_to_user_story_v1": {
                "description": "Prompt para converter relatos de bugs em User Stories",
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "version": "v1",
                "created_at": "2025-01-15",
                "tags": ["bug-analysis", "user-story", "product-management"]
            }
        }
        
        print(f"Salvando prompt em '{output_path}'...")
        if save_yaml(prompt_data, output_path):
            print("   ✓ Arquivo YAML salvo com sucesso!")
            return True
        else:
            print("   ❌ Erro ao salvar arquivo YAML")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao fazer pull do prompt: {e}")
        return False


def main():
    """Função principal"""
    print_section_header("PULL PROMPTS FROM LANGSMITH")
    
    # Executa o pull
    success = pull_prompts_from_langsmith()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
