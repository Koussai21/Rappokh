"""Perplexity integration for research and fact-finding"""
import requests
from backend.config import settings
from typing import Optional

class PerplexityIntegration:
    def __init__(self):
        self.api_key = settings.perplexity_api_key
        self.base_url = "https://api.perplexity.ai"

    def research_topic(self, topic: str, context: str = "") -> Optional[str]:
        """Effectuer une recherche approfondie sur un sujet"""
        if not self.api_key:
            return None

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "pplx-7b-online",
                    "messages": [
                        {
                            "role": "user",
                            "content": f"""Fournissez une recherche complète et actuelle sur:

Sujet: {topic}
{f"Contexte: {context}" if context else ""}

Incluez:
- Définitions et concepts clés
- Développements récents
- Statistiques et données
- Considérations pratiques"""
                        }
                    ]
                }
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Perplexity API error: {e}")

        return None

    def get_latest_information(self, topic: str) -> Optional[str]:
        """Obtenir les informations les plus récentes"""
        if not self.api_key:
            return None

        return self.research_topic(f"Dernières actualités et informations sur {topic}")
