from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    app_env: str = "development"
    debug: bool = True
    port: int = 8000
    host: str = "0.0.0.0"

    # API Keys
    anthropic_api_key: str
    openai_api_key: str
    perplexity_api_key: Optional[str] = None

    # Report generation
    max_clarification_rounds: int = 3
    report_language: str = "fr"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
