# Rappokh - AI-Powered Report Generator

Rappokh est un chatbot IA spécialisé dans la génération de rapports documentaires. Il utilise une combinaison de différents LLMs (Claude, Perplexity, OpenAI) pour générer des rapports complets basés sur les informations fournies par l'utilisateur.

## Caractéristiques Principales

- **Brainstorming conversationnel**: Les utilisateurs fournissent les idées principales du rapport
- **Multi-LLM**: Utilise Claude, Perplexity et OpenAI selon leurs spécialités
- **Agent intelligent**: Pose des questions clarificatrices si des informations manquent
- **Support des templates**: Adapte la génération aux templates Word personnalisés
- **Rapport complet**: Compréhension du contenu, recherche approfondie et écriture

## Architecture

```
Rappokh/
├── backend/              # API FastAPI
│   ├── app.py
│   ├── agents/           # Agents pour clarifications
│   ├── llm_integrations/ # Intégrations LLMs
│   ├── report_gen/       # Génération de rapports
│   └── config.py
├── frontend/             # CLI interface
│   └── cli.py
├── requirements.txt
├── .env.example
└── CLAUDE.md            # Documentation du projet
```

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configuration
cp .env.example .env
# Éditer .env avec vos clés API
```

## Démarrage Rapide

```bash
# Lancer l'API
python -m backend.app

# Ou utiliser la CLI
python -m frontend.cli
```

## API Endpoints (MVP)

- `POST /api/report/brainstorm` - Débuter session brainstorming
- `POST /api/report/generate` - Générer le rapport
- `POST /api/report/clarify` - Questions de clarification
