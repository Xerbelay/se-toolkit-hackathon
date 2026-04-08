from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    app_name: str = Field(default='ExpenseMate API', alias='APP_NAME')
    debug: bool = Field(default=False, alias='DEBUG')
    port: int = Field(default=8000, alias='PORT')

    db_host: str = Field(default='localhost', alias='DB_HOST')
    db_port: int = Field(default=5432, alias='DB_PORT')
    db_name: str = Field(default='expensemate', alias='DB_NAME')
    db_user: str = Field(default='expensemate', alias='DB_USER')
    db_password: str = Field(default='expensemate', alias='DB_PASSWORD')

    cors_origins: list[str] = Field(default_factory=lambda: ['*'], alias='CORS_ORIGINS')

    openai_api_key: str = Field(default='', alias='OPENAI_API_KEY')
    openai_api_base_url: str = Field(default='https://openrouter.ai/api/v1', alias='OPENAI_API_BASE_URL')
    openai_model: str = Field(default='openrouter/free', alias='OPENAI_MODEL')

    openrouter_site_url: str = Field(default='http://localhost:8080', alias='OPENROUTER_SITE_URL')
    openrouter_app_title: str = Field(default='ExpenseMate', alias='OPENROUTER_APP_TITLE')

    session_cookie_name: str = Field(default='expensemate_session', alias='SESSION_COOKIE_NAME')
    session_max_age_days: int = Field(default=14, alias='SESSION_MAX_AGE_DAYS')
    session_cookie_secure: bool = Field(default=False, alias='SESSION_COOKIE_SECURE')

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def llm_enabled(self) -> bool:
        return bool(self.openai_api_key.strip())

    @property
    def session_max_age_seconds(self) -> int:
        return self.session_max_age_days * 24 * 60 * 60


settings = Settings()
