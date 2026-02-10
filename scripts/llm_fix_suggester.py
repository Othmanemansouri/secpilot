#!/usr/bin/env python3
"""
LLM Fix Suggester pour la pipeline CI/CD Secpilot

Analyse les échecs de tests et suggère des corrections en utilisant des APIs LLM.
Supporte Ollama (local), Anthropic Claude et OpenAI GPT.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from abc import ABC, abstractmethod

# Import conditionnel des clients LLM
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class LLMProvider(ABC):
    """Interface abstraite pour les providers LLM"""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Génère une réponse à partir du prompt"""
        pass


class OllamaProvider(LLMProvider):
    """Provider pour Ollama (modèles locaux)"""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url.rstrip('/')
        self.model = model

    def generate(self, prompt: str) -> str:
        if not HAS_REQUESTS:
            raise ImportError("Le package 'requests' est requis pour Ollama")

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json().get("response", "")


class AnthropicProvider(LLMProvider):
    """Provider pour Anthropic Claude"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
            self.model = model
        except ImportError:
            raise ImportError("Le package 'anthropic' est requis pour ce provider")

    def generate(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text


class OpenAIProvider(LLMProvider):
    """Provider pour OpenAI GPT"""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key)
            self.model = model
        except ImportError:
            raise ImportError("Le package 'openai' est requis pour ce provider")

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content


class MockProvider(LLMProvider):
    """Provider de test qui retourne une réponse statique"""

    def generate(self, prompt: str) -> str:
        return """## Analyse des échecs de tests

### Cause racine
Les tests ont échoué en raison de bugs dans le code source.

### Suggestion de correction
Veuillez corriger les bugs identifiés dans les logs de tests.

*Ce message est généré par le provider de test. Configurez un vrai provider LLM pour des suggestions détaillées.*
"""


def get_provider(provider_name: str) -> LLMProvider:
    """Factory pour créer le provider LLM approprié"""

    provider_name = provider_name.lower()

    if provider_name == "ollama":
        base_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
        model = os.environ.get("OLLAMA_MODEL", "llama2")
        return OllamaProvider(base_url=base_url, model=model)

    elif provider_name == "anthropic":
        api_key = os.environ.get("LLM_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY ou LLM_API_KEY requis pour Anthropic")
        return AnthropicProvider(api_key=api_key)

    elif provider_name == "openai":
        api_key = os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY ou LLM_API_KEY requis pour OpenAI")
        return OpenAIProvider(api_key=api_key)

    elif provider_name == "mock":
        return MockProvider()

    else:
        raise ValueError(f"Provider inconnu : {provider_name}")


class LLMFixSuggester:
    """Analyse les échecs de tests et génère des suggestions de correction"""

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def load_context(self, contexts_dir: Path) -> Dict[str, str]:
        """Charge tous les documents de contexte métier"""
        contexts = {}
        if contexts_dir.exists():
            for context_file in contexts_dir.glob('*.md'):
                domain = context_file.stem
                contexts[domain] = context_file.read_text(encoding='utf-8')
        return contexts

    def load_source_code(self, src_dir: Path, language: str, domain: str) -> str:
        """Charge le code source pertinent pour l'analyse"""
        extensions = {
            'python': '.py',
            'javascript': '.js',
            'java': '.java'
        }
        ext = extensions.get(language, '')

        for src_file in src_dir.rglob(f'*{domain}*{ext}'):
            try:
                return src_file.read_text(encoding='utf-8')
            except Exception:
                continue
        return ""

    def parse_test_output(self, test_output: str) -> Dict:
        """Parse la sortie des tests pour extraire les informations d'échec"""
        return {
            'raw_output': test_output,
            'failed_tests': self._extract_failed_tests(test_output),
            'error_messages': self._extract_errors(test_output)
        }

    def _extract_failed_tests(self, output: str) -> List[str]:
        """Extrait les noms des tests échoués"""
        failed = []
        for line in output.split('\n'):
            if any(marker in line for marker in ['FAILED', 'FAIL:', '✗', 'Error']):
                failed.append(line.strip())
        return failed[:20]  # Limite à 20 pour éviter les prompts trop longs

    def _extract_errors(self, output: str) -> List[str]:
        """Extrait les messages d'erreur"""
        errors = []
        lines = output.split('\n')
        capture = False
        current_error = []

        for line in lines:
            if any(keyword in line for keyword in ['Error', 'Exception', 'AssertionError', 'FAILED']):
                capture = True
            if capture:
                current_error.append(line)
                if line.strip() == '' and current_error:
                    errors.append('\n'.join(current_error))
                    current_error = []
                    capture = False

        if current_error:
            errors.append('\n'.join(current_error))

        return errors[:10]  # Limite à 10

    def generate_fix_suggestion(
        self,
        test_failure: Dict,
        source_code: str,
        context: str,
        language: str
    ) -> str:
        """Génère une suggestion de correction avec le LLM"""

        prompt = f"""Tu es un assistant de revue de code aidant à corriger des bugs dans une pipeline CI/CD.

## Contexte métier
{context[:2000]}

## Code source ({language})
```{language}
{source_code[:3000]}
```

## Sortie des tests échoués
```
{test_failure['raw_output'][:2000]}
```

## Tests échoués
{chr(10).join(test_failure['failed_tests'][:10])}

## Tâche
Analyse les échecs de tests et fournis :

1. **Analyse de la cause racine** : Identifie pourquoi chaque test échoue
2. **Classification du bug** : Est-ce un bug classique (syntaxe, logique, erreur courante) ou contextuel (nécessite la connaissance du domaine métier) ?
3. **Correction suggérée** : Fournis le code corrigé avec explications
4. **Conseils de prévention** : Comment éviter ce type de bug à l'avenir

Formate ta réponse en Markdown avec des sections claires et des blocs de code.
"""

        return self.provider.generate(prompt)

    def process_artifacts(
        self,
        artifacts_dir: Path,
        contexts_dir: Path,
        src_dir: Path
    ) -> str:
        """Traite tous les artefacts de test et génère les suggestions"""

        contexts = self.load_context(contexts_dir)
        suggestions = ["# Suggestions de correction LLM\n"]
        suggestions.append("Généré par la pipeline CI/CD Secpilot\n\n")

        # Parcourt les résultats de tests de chaque langage
        for artifact_folder in artifacts_dir.iterdir():
            if not artifact_folder.is_dir():
                continue

            language = self._detect_language(artifact_folder.name)
            if not language:
                continue

            test_output_file = artifact_folder / 'test-output.txt'
            if not test_output_file.exists():
                continue

            suggestions.append(f"## Échecs de tests {language.title()}\n\n")

            try:
                test_output = test_output_file.read_text(encoding='utf-8')
            except Exception as e:
                suggestions.append(f"Erreur de lecture du fichier : {e}\n\n")
                continue

            test_failure = self.parse_test_output(test_output)

            if not test_failure['failed_tests']:
                suggestions.append("Aucun échec détecté.\n\n")
                continue

            # Détermine le domaine à partir des noms de fichiers de test
            for domain in ['ecommerce', 'banking', 'healthcare']:
                if domain in test_output.lower():
                    source_code = self.load_source_code(src_dir, language, domain)
                    context = contexts.get(domain, "Aucun contexte disponible")

                    try:
                        fix = self.generate_fix_suggestion(
                            test_failure,
                            source_code,
                            context,
                            language
                        )

                        suggestions.append(f"### Domaine {domain.title()}\n\n")
                        suggestions.append(fix)
                        suggestions.append("\n\n---\n\n")
                    except Exception as e:
                        suggestions.append(f"Erreur de génération LLM : {e}\n\n")

        return ''.join(suggestions)

    def _detect_language(self, folder_name: str) -> Optional[str]:
        """Détecte le langage depuis le nom du dossier d'artefact"""
        folder_lower = folder_name.lower()
        if 'python' in folder_lower:
            return 'python'
        elif 'javascript' in folder_lower or 'js' in folder_lower:
            return 'javascript'
        elif 'java' in folder_lower:
            return 'java'
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Génère des suggestions de correction LLM pour les échecs de tests'
    )
    parser.add_argument(
        '--artifacts-dir',
        required=True,
        help='Répertoire contenant les artefacts de test'
    )
    parser.add_argument(
        '--contexts-dir',
        required=True,
        help='Répertoire contenant les documents de contexte'
    )
    parser.add_argument(
        '--src-dir',
        required=True,
        help='Répertoire contenant le code source'
    )
    parser.add_argument(
        '--output-file',
        required=True,
        help='Fichier de sortie pour les suggestions'
    )
    parser.add_argument(
        '--provider',
        default=os.environ.get('LLM_PROVIDER', 'mock'),
        choices=['ollama', 'anthropic', 'openai', 'mock'],
        help='Provider LLM à utiliser (défaut: mock)'
    )

    args = parser.parse_args()

    try:
        provider = get_provider(args.provider)
        suggester = LLMFixSuggester(provider)

        suggestions = suggester.process_artifacts(
            Path(args.artifacts_dir),
            Path(args.contexts_dir),
            Path(args.src_dir)
        )

        Path(args.output_file).write_text(suggestions, encoding='utf-8')
        print(f"Suggestions écrites dans {args.output_file}")

    except Exception as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
