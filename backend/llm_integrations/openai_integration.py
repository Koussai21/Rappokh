"""OpenAI integration for clarification and research"""
from openai import OpenAI
from backend.config import settings
from typing import List

class OpenAIIntegration:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY not configured")
            self._client = OpenAI(api_key=settings.openai_api_key)
        return self._client

    def generate_clarification_questions(self, brainstorm_notes: str, current_gaps: List[str] = None) -> List[str]:
        """Générer des questions pour clarifier les informations manquantes"""
        gaps_text = "\n".join(f"- {gap}" for gap in (current_gaps or []))

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""Basé sur ces notes de brainstorming, identifiez les informations manquantes et générez 3-5 questions pertinentes pour clarifier:

Notes: {brainstorm_notes}

{f"Lacunes identifiées: {gaps_text}" if gaps_text else ""}

Générez des questions qui aideront à créer un rapport plus complet et professionnel.
Formatez en liste avec une question par ligne."""
                }
            ]
        )

        questions = response.choices[0].message.content.split('\n')
        return [q.strip() for q in questions if q.strip() and not q.startswith('#')]

    def evaluate_completeness(self, brainstorm_notes: str) -> dict:
        """Évaluer si les informations sont suffisantes pour générer le rapport"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""Évaluez la complétude de ces notes pour générer un rapport professionnel:

{brainstorm_notes}

Répondez en JSON avec:
- is_complete: boolean
- confidence: 0-100 (%)
- missing_areas: liste des domaines manquants
- suggestions: conseils pour améliorer"""
                }
            ]
        )
        return {"evaluation": response.choices[0].message.content}
