from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_url: str = os.environ.get("DATABASE_URL", "sqlite:///./test.db")
    postgres_db: str = os.environ.get("POSTGRES_DB")
    postgres_host: str = os.environ.get("POSTGRES_HOST")
    postgres_port: int = os.environ.get("POSTGRES_PORT")
    postgres_user: str = os.environ.get("POSTGRES_USER")
    postgres_password: str = os.environ.get("POSTGRES_PASSWORD")

    song_dir: str = os.environ.get("SONG_DIR", "/app/music")
    log_level: str = os.environ.get("LOG_LEVEL", "info")

    class Config:
        env_file = ".env"

settings = Settings()
