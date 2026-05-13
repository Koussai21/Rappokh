"""Main report generation orchestrator"""
from typing import Dict, List, Optional
from backend.llm_integrations.claude import ClaudeIntegration
from backend.llm_integrations.openai_integration import OpenAIIntegration
from backend.llm_integrations.perplexity import PerplexityIntegration
from backend.agents.clarification_agent import ClarificationAgent

class ReportGenerator:
    def __init__(self):
        self.claude = ClaudeIntegration()
        self.openai = OpenAIIntegration()
        self.perplexity = PerplexityIntegration()
        self.clarification_agent = ClarificationAgent()

    def start_brainstorming_session(self, initial_notes: str) -> Dict:
        """Initier une session de brainstorming"""
        # Understand the content structure
        analysis = self.claude.understand_content(initial_notes)

        # Check if we need clarifications
        questions = []
        if self.clarification_agent.should_ask_more_questions(initial_notes):
            questions = self.clarification_agent.ask_clarification_questions(initial_notes)

        return {
            "session_id": "temp_session",
            "initial_analysis": analysis,
            "clarification_questions": questions,
            "needs_more_info": len(questions) > 0
        }

    def generate_full_report(self, brainstorm_notes: str, answers: Optional[Dict] = None) -> str:
        """Générer un rapport complet"""
        # Combine notes and answers
        combined_content = brainstorm_notes
        if answers:
            combined_content += "\n\nRéponses aux clarifications:\n"
            for key, value in answers.items():
                combined_content += f"- {value}\n"

        # Understand the structure
        analysis = self.claude.understand_content(combined_content)

        # Research if available
        research = self.perplexity.research_topic(brainstorm_notes[:100]) or ""

        # Generate sections
        sections = []
        section_titles = [
            "Introduction",
            "Contexte et analyse",
            "Résultats et constats",
            "Recommandations",
            "Conclusion"
        ]

        for title in section_titles:
            section_content = self.claude.generate_section(
                brainstorm_notes,
                f"Recherche: {research}\nAnalyse: {analysis}",
                title
            )
            sections.append(f"## {title}\n\n{section_content}")

        # Combine sections
        draft_report = "\n\n".join(sections)

        # Polish the report
        final_report = self.claude.review_and_polish(draft_report)

        return final_report

    def add_template_formatting(self, report_content: str, template_data: Optional[Dict] = None) -> str:
        """Adapter le rapport à un template Word (future feature)"""
        # Pour le MVP, on retourne juste le rapport
        # La fonctionnalité complète sera ajoutée plus tard
        return report_content
