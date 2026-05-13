"""Claude (Anthropic) integration for report generation and research"""
import anthropic
from backend.config import settings

class ClaudeIntegration:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def understand_content(self, brainstorm_notes: str) -> dict:
        """Comprendre et structurer le contenu du rapport"""
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""Analysez les notes de brainstorming suivantes et fournissez:
1. Les thèmes principaux identifiés
2. La structure recommandée du rapport
3. Les sections suggérées
4. Les points clés à développer

Notes: {brainstorm_notes}

Répondez en JSON structuré."""
                }
            ]
        )
        return {"analysis": message.content[0].text}

    def generate_section(self, topic: str, context: str, section_title: str) -> str:
        """Générer une section spécifique du rapport"""
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": f"""Générez une section complète et professionnelle pour un rapport.

Titre de la section: {section_title}
Contexte: {context}
Sujet principal: {topic}

Écrivez de manière professionnelle et structurée."""
                }
            ]
        )
        return message.content[0].text

    def review_and_polish(self, draft_report: str) -> str:
        """Relire et polir le rapport"""
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[
                {
                    "role": "user",
                    "content": f"""Relisez et améliorez ce rapport:

{draft_report}

Améliorations à apporter:
- Fluidité et clarté
- Cohérence
- Professionnalisme
- Éliminez les redondances

Fournissez le rapport amélioré."""
                }
            ]
        )
        return message.content[0].text
