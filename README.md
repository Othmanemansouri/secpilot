# Secpilot

Outil CI/CD qui suggère des corrections de code en utilisant un LLM lorsque les tests échouent.

## Aperçu

Secpilot est une pipeline CI/CD intelligente qui :
1. Exécute des tests pour du code Python, JavaScript et Java
2. Détecte les échecs de tests
3. Analyse les échecs avec un LLM (Ollama, Claude ou GPT-4)
4. Suggère des corrections basées sur le contexte métier

## Structure du projet

```
secpilot/
├── .github/workflows/     # Configuration de la pipeline CI/CD
├── src/                   # Code source bugué (pour démonstration)
│   ├── python/
│   ├── javascript/
│   └── java/
├── tests/                 # Tests unitaires qui détectent les bugs
├── contexts/              # Documentation du contexte métier
├── scripts/               # Scripts d'intégration LLM
└── config/                # Configurations des frameworks de test
```

## Domaines métier

### E-Commerce
- **Règle critique** : Les prix ne peuvent pas être négatifs
- **Code** : `src/*/ecommerce/`

### Banque
- **Règle critique** : Refuser les virements si solde insuffisant
- **Code** : `src/*/banking/`

### Santé
- **Règle critique** : Les dosages ne doivent pas dépasser les limites maximales sûres
- **Code** : `src/*/healthcare/`

## Types de bugs

### Bugs classiques
Erreurs de programmation courantes :
- Troncature de division entière
- Erreurs off-by-one
- NullPointerException
- Comparaison de virgule flottante
- Coercition de type
- Sensibilité à la casse

### Bugs contextuels
Nécessitent la connaissance du domaine métier :
- Validation de prix négatif (e-commerce)
- Vérification du solde (banque)
- Application de dose maximale (santé)

## Installation

### Prérequis
- Python 3.11+
- Node.js 20+
- Java 17+
- Maven 3.9+

### Installation locale

```bash
# Cloner le dépôt
git clone https://github.com/votre-org/secpilot.git
cd secpilot

# Installer les dépendances Python
pip install -r requirements.txt

# Installer les dépendances JavaScript
npm install

# Compiler le projet Java
mvn -f config/pom.xml compile
```

## Configuration

### Variables GitHub

| Variable | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `LLM_PROVIDER` | Provider LLM (`ollama`, `anthropic`, `openai`, `mock`) | `mock` |
| `OLLAMA_URL` | URL du serveur Ollama | `http://localhost:11434` |
| `OLLAMA_MODEL` | Modèle Ollama à utiliser | `llama2` |

### Secrets GitHub

| Secret | Description |
|--------|-------------|
| `LLM_API_KEY` | Clé API pour Anthropic ou OpenAI |

## Exécution des tests localement

```bash
# Python
pytest tests/python/ -v -c config/pytest.ini

# JavaScript
npm test

# Java
mvn -f config/pom.xml test
```

## Pipeline CI/CD

La pipeline se déclenche sur :
- Push vers `main`, `develop`, ou `feature/*`
- Pull requests vers `main`

### Étapes de la pipeline
1. Exécution des tests en parallèle pour les trois langages
2. Si des tests échouent → déclenchement de l'analyse LLM
3. Génération des suggestions de correction
4. Post des suggestions en commentaire de PR (pour les pull requests)
5. Upload des suggestions comme artefact du workflow

## Intégration LLM

Le LLM reçoit :
- La sortie des tests échoués
- Le code source pertinent
- La documentation du contexte métier

Il retourne :
- Analyse de la cause racine
- Classification du bug (classique vs contextuel)
- Suggestions de code corrigé
- Conseils de prévention

### Providers supportés

- **Ollama** : Modèles locaux (llama2, codellama, etc.)
- **Anthropic** : Claude
- **OpenAI** : GPT-4
- **Mock** : Provider de test (pas de vraie API)

## Contribution

1. Forker le dépôt
2. Créer une branche feature
3. Apporter les modifications
4. Exécuter tous les tests
5. Soumettre une pull request

## Auteur

BOUREDJI Amine - CI/CD & QA

## Licence

MIT License
