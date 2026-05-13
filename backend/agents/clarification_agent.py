"""Agent for asking clarification questions and improving content"""
from typing import List, Dict
from backend.llm_integrations.openai_integration import OpenAIIntegration

class ClarificationAgent:
    def __init__(self, max_rounds: int = 3):
        self.openai = OpenAIIntegration()
        self.max_rounds = max_rounds
        self.clarifications_asked = 0

    def ask_clarification_questions(self, brainstorm_notes: str) -> List[str]:
        """Demander des questions de clarification"""
        if self.clarifications_asked >= self.max_rounds:
            return []

        questions = self.openai.generate_clarification_questions(brainstorm_notes)
        self.clarifications_asked += 1
        return questions

    def evaluate_content_completeness(self, brainstorm_notes: str) -> Dict:
        """Évaluer si le contenu est suffisant"""
        evaluation = self.openai.evaluate_completeness(brainstorm_notes)
        return evaluation

    def should_ask_more_questions(self, brainstorm_notes: str) -> bool:
        """Déterminer si plus de questions sont nécessaires"""
        if self.clarifications_asked >= self.max_rounds:
            return False

        evaluation = self.evaluate_content_completeness(brainstorm_notes)
        # Simple heuristic: si l'évaluation contient "not_complete", poser plus de questions
        return "not complete" in evaluation.get("evaluation", "").lower()

    def collect_user_feedback(self, questions: List[str]) -> Dict[str, str]:
        """Préparer une structure pour collecter les réponses utilisateur"""
        return {
            f"question_{i}": q
            for i, q in enumerate(questions, 1)
        }
