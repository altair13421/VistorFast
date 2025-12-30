# app/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    # DATABASE_URL should already contain the full connection string:
    #   postgresql://user:pass@host:port/dbname
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

    # Optional explicit parts – handy if you build the URL manually
    postgres_db: str | None = os.getenv("POSTGRES_DB")
    postgres_host: str | None = os.getenv("POSTGRES_HOST")
    postgres_port: int | None = os.getenv("POSTGRES_PORT", 5432)
    postgres_user: str | None = os.getenv("POSTGRES_USER")
    postgres_password: str | None = os.getenv("POSTGRES_PASSWORD")

    # App‑specific
    song_dir: str = os.getenv("SONG_DIR", "/app/music")
    log_level: str = os.getenv("LOG_LEVEL", "info")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
