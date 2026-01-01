from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "supersecretkey"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    BASE_DIR: str = os.environ.get("BASE_DIR", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    LIBRARY_DIR: str = os.environ.get("LIBRARY_DIR", 'Library')
    DOWNLOAD_DIR: str = os.environ.get("DOWNLOAD_DIR", 'Downloads')
    MEDIA_DIR: str = os.environ.get("MEDIA_DIR", 'Media')
    SAVED_TORRENTS_DIR: str = os.environ.get("SAVED_TORRENTS_DIR", '_torrent_files')

    # Nyaa.si specific settings
    BASE_URL: str = "https://nyaa.si"

    categories: dict[str, dict] = {
        "1": {
            "name": "Anime",
            "sub_cats": {
                "1": "Anime Music Video",
                "2": "English-translated",
                "3": "Non-English-translated",
                "4": "Raw"
            }
        },
        "2": {
            "name": "Audio",
            "sub_cats": {
                "1": "Lossless",
                "2": "Lossy"
            }
        },
        "3": {
            "name": "Literature",
            "sub_cats": {
                "1": "English-translated",
                "2": "Non-English-translated",
                "3": "Raw"
            }
        },
        "4": {
            "name": "Live Action",
            "sub_cats": {
                "1": "English-translated",
                "2": "Idol/Promotional Video",
                "3": "Non-English-translated",
                "4": "Raw"
            }
        },
        "5": {
            "name": "Pictures",
            "sub_cats": {
                "1": "Graphics",
                "2": "Photos"
            }
        },
        "6": {
            "name": "Software",
            "sub_cats": {
                "1": "Applications",
                "2": "Games"
            }
        }
    }
    # Internet Configs
    headers = {
        "User-Agent": "PostmanRuntime/7.46.1",
        # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        # "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }

    class Config:
        env_file = ".env"

    def _get_category_name(self, category_id: str) -> str:
        cat, sub_cat = category_id.split("_")
        return f"{self.categories[cat]['name']} - {self.categories[cat]['sub_cats'][sub_cat]}"

settings = Settings()
__version__ = "0.10.3"
