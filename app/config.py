from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str = "sqlite+aiosqlite:///./f1.db"
    FASTF1_CACHE_DIR: str = "./fastf1_cache"
    SYNC_TOKEN: str | None = None
    CORS_ORIGINS: list[str] = ["*"]
    PAGE_SIZE: int = 50
    APP_ENV: str = "development"


settings = Settings()
