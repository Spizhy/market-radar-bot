from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # AI Configuration
    LLM_PROVIDER: Literal["mock", "openai", "gemini"] = "mock"
    LLM_MODEL: str = "gpt-4o-mini"
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    # Bot Delivery
    DELIVERY_MODE: Literal["mock", "telegram", "slack", "both"] = "mock"
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    SLACK_WEBHOOK_URL: str = ""

    # Storage
    DATABASE_PATH: str = "data/market_radar.sqlite3"
    MIN_IMPACT_ALERT_SCORE: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
