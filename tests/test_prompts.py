"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


class TestPrompts:
    @pytest.fixture(autouse=True)
    def setup_prompt(self):
        prompt_file = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
        if not prompt_file.exists():
            pytest.skip("Arquivo prompts/bug_to_user_story_v2.yml ainda não existe")
        data = load_prompts(str(prompt_file))
        self.prompt = data.get("bug_to_user_story_v2", {})

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in self.prompt, "Campo system_prompt não encontrado"
        assert self.prompt["system_prompt"].strip() != "", "System prompt está vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = self.prompt.get("system_prompt", "").lower()
        role_keywords = ["product manager", "analista", "especialista", "product owner", "pm", "po", "gerente de produto", "role", "persona", "assistente"]
        has_role = any(kw in system_prompt for kw in role_keywords)
        assert has_role, "O prompt deve definir uma persona/papel claro no system_prompt."

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = self.prompt.get("system_prompt", "").lower()
        format_keywords = ["markdown", "como um", "eu quero", "para que", "user story", "template", "estrutura"]
        has_format = any(kw in system_prompt for kw in format_keywords)
        assert has_format, "O prompt deve exigir um formato específico (Markdown ou User Story padrão)."

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = self.prompt.get("system_prompt", "").lower()
        few_shot_keywords = ["exemplo", "example", "few-shot", "few shot", "caso", "cenário", "entrada", "saída"]
        has_few_shot = any(kw in system_prompt for kw in few_shot_keywords)
        assert has_few_shot, "O prompt deve conter exemplos de Few-shot learning."

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        system_prompt = self.prompt.get("system_prompt", "")
        user_prompt = self.prompt.get("user_prompt", "")
        
        assert "TODO" not in system_prompt, "Encontrado TODO em uppercase no system prompt"
        assert "TODO" not in user_prompt, "Encontrado TODO em uppercase no user prompt"
        assert "[todo]" not in system_prompt.lower(), "Encontrado [todo] no system prompt"
        assert "[todo]" not in user_prompt.lower(), "Encontrado [todo] no user prompt"

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = self.prompt.get("techniques_applied", [])
        assert isinstance(techniques, list), "techniques_applied deve ser uma lista nos metadados"
        assert len(techniques) >= 2, f"Mínimo de 2 técnicas aplicadas requeridas nos metadados, encontradas: {len(techniques)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])