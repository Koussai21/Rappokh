from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", case_sensitive=False)

    app_env: str = "development"
    debug: bool = True
    port: int = 8000
    host: str = "0.0.0.0"

    # API Keys - Optional for development
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    perplexity_api_key: Optional[str] = None

    # Report generation
    max_clarification_rounds: int = 3
    report_language: str = "fr"

try:
    settings = Settings()
except Exception as e:
    # Fallback for development without .env
    settings = Settings(
        anthropic_api_key=None,
        openai_api_key=None,
        perplexity_api_key=None
    )
