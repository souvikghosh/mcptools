"""Application configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    news_rss_url: str = "https://feeds.finance.yahoo.com/rss/2.0/headline"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
