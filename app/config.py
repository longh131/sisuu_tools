"""
Application configuration.
All sensitive values are loaded from .env — never hardcode secrets.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "Seller Toolkit"
    debug: bool = False
    secret_key: str = "change-me"
    domain: str = "sisuu.com"

    # Database
    database_url: str = "mysql+pymysql://root:@localhost:3306/sisuu_tools"

    # DeepSeek AI
    deepseek_api_key: str = ""
    deepseek_api_base: str = "https://api.deepseek.com"

    # Admin
    admin_username: str = "admin"
    admin_password: str = "admin123"

    # Logging
    log_level: str = "INFO"
    log_dir: str = "logs"

    # Usage limits (overridable via .env)
    guest_ai_daily_limit: int = 3
    registered_ai_daily_limit: int = 10

    # Analytics — Google Analytics 4 (leave empty to disable)
    ga_measurement_id: str = ""

    # Payment provider (stub | stripe | paddle — future)
    payment_provider: str = "stub"

    @property
    def site_url(self) -> str:
        """Canonical site URL used for SEO meta tags."""
        return f"https://{self.domain}"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
