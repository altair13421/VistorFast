
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

async def get_song_metadata(file_path: Path) -> dict:
    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

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

async def scan_directory(directory: Path = BASE_DIR) -> list[Path]:
    if not directory.exists() or not directory.is_dir():
        raise NotADirectoryError(f"Directory not found: {directory}")

    song_files = []
    for ext in MIME_TYPES.keys():
        song_files.extend(directory.rglob(f"*.{ext}"))

    return song_files
