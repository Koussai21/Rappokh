# Rappokh - Documentation du Projet

## Vue d'ensemble

Rappokh est un **chatbot IA spécialisé dans la génération de rapports documentaires**. Il utilise une combinaison de différents LLMs (Claude, Perplexity, OpenAI) pour générer des rapports professionnels complets.

## Architecture

```
Rappokh/
├── backend/
│   ├── app.py                    # API FastAPI principale
│   ├── config.py                 # Configuration (env variables)
│   ├── llm_integrations/         # Intégrations LLM
│   │   ├── claude.py             # Anthropic Claude
│   │   ├── openai_integration.py # OpenAI GPT
│   │   └── perplexity.py         # Perplexity Research
│   ├── agents/
│   │   └── clarification_agent.py # Agent pour clarifications
│   └── report_gen/
│       └── generator.py           # Orchestrateur principal
├── frontend/
│   └── cli.py                    # Interface CLI
├── requirements.txt
├── .env.example
└── CLAUDE.md
```

## Flux Principal

1. **Brainstorming** → Utilisateur fournit ses notes/idées
2. **Analyse** → Claude comprend et structure le contenu
3. **Évaluation** → OpenAI évalue si info sont suffisantes
4. **Clarification** → Si nécessaire, pose des questions
5. **Recherche** → Perplexity effectue une recherche approfondie
6. **Génération** → Claude génère les sections du rapport
7. **Révision** → Claude relit et polit le rapport

## API Endpoints

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Message de bienvenue |
| `/health` | GET | Vérifier l'état du serveur |
| `/api/report/brainstorm` | POST | Débuter session brainstorming |
| `/api/report/clarify` | POST | Obtenir questions de clarification |
| `/api/report/generate` | POST | Générer rapport complet |
| `/api/report/evaluate` | POST | Évaluer complétude des infos |

## CLI Commandes

```bash
# Brainstorming interactif
python -m frontend.cli brainstorm

# Générer rapport avec clarifications
python -m frontend.cli generate --clarify

# Évaluer complétude
python -m frontend.cli evaluate

# Lancer API
python -m frontend.cli server
```

## Configuration

### Variables d'environnement (.env)

```
ANTHROPIC_API_KEY=...       # Claude API key
OPENAI_API_KEY=...          # OpenAI API key
PERPLEXITY_API_KEY=...      # Perplexity key (optionnel)
APP_ENV=development         # development | production
DEBUG=true                  # true | false
PORT=8000                   # Port du serveur
MAX_CLARIFICATION_ROUNDS=3  # Nombre max de questions
REPORT_LANGUAGE=fr          # Langue du rapport
```

## Classes Principales

### ReportGenerator
Orchestrateur principal qui coordonne tous les LLMs:
- `start_brainstorming_session()` - Initiater session
- `generate_full_report()` - Générer rapport complet
- `add_template_formatting()` - Adapter à template Word (future)

### ClaudeIntegration
Gère la génération et révision du contenu:
- `understand_content()` - Analyser le brainstorming
- `generate_section()` - Générer section spécifique
- `review_and_polish()` - Réviser et améliorer

### OpenAIIntegration
Gère les clarifications et évaluations:
- `generate_clarification_questions()` - Poser questions
- `evaluate_completeness()` - Évaluer suffisance infos

### PerplexityIntegration
Gère la recherche approfondie:
- `research_topic()` - Recherche sur un sujet
- `get_latest_information()` - Info les plus récentes

### ClarificationAgent
Gère le dialogue pour clarifications:
- `ask_clarification_questions()` - Poser questions
- `should_ask_more_questions()` - Déterminer si + questions
- `evaluate_content_completeness()` - Évaluer complétude

## Prochaines Étapes (Future Scope)

- [ ] Support des templates Word (.docx)
- [ ] Interface web React/Vue
- [ ] Stockage des rapports (DB)
- [ ] Historique des sessions
- [ ] Export PDF
- [ ] Support multilingue complet
- [ ] Intégrations avec Plus de LLMs
- [ ] Système de templates prédéfinis
- [ ] Analytics et usage tracking
- [ ] Authentication utilisateur

## Installation et Setup

```bash
# 1. Clone le repo
git clone <repo_url>
cd Rappokh

# 2. Virtual env
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# 3. Dépendances
pip install -r requirements.txt

# 4. Configuration
cp .env.example .env
# Éditer .env avec clés API

# 5. Lancer
python -m frontend.cli server
```

## Notes pour le Développement

- **Modèles Claude**: Utilise Claude 3.5 Sonnet (meilleur rapport qualité/prix)
- **Modèles OpenAI**: Utilise GPT-4o-mini (plus rapide pour clarifications)
- **Timeout requests**: À implémenter si recherches Perplexity trop lentes
- **Error handling**: Chaque LLM a ses propres gestions d'erreur
- **Rate limits**: À monitorer notamment pour OpenAI
