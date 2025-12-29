from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_url: str = os.environ.get("DATABASE_URL", "sqlite:///./test.db")
    song_dir: str = os.environ.get("SONG_DIR", "/app/music")
    log_level: str = os.environ.get("LOG_LEVEL", "info")
    class Config:
        env_file = ".env"

settings = Settings()
