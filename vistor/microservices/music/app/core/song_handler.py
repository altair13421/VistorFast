
from mutagen import File as MutagenFile

from pathlib import Path
import mimetypes

from app.core.config import settings

BASE_DIR = Path(settings.song_dir)
MIME_TYPES = {
    "mp3": "audio/mpeg",
    "flac": "audio/flac",
    "wav": "audio/wav",
    "aac": "audio/aac",
    "ogg": "audio/ogg",
}

def get_song_metadata(file_path: Path) -> dict:
    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File {file_path} does not exist.")

    audio = MutagenFile(file_path)
    if audio is None:
        raise ValueError(f"Unsupported or corrupted audio file: {file_path}")

    metadata = {
        "title": audio.tags.get("TIT2").text[0] if audio.tags.get("TIT2") else file_path.stem,
        "artists": audio.tags.get("TPE1").text[0] if audio.tags.get("TPE1") else "Unknown Artist",
        "albums": audio.tags.get("TALB").text[0] if audio.tags.get("TALB") else "Unknown Album",
        "duration": int(audio.info.length) if audio.info else 0,
        "bitrate": int(audio.info.bitrate) if audio.info and hasattr(audio.info, 'bitrate') else 0,
    }
    return metadata
