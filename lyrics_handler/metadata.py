from mutagen.id3 import ID3
from typing import Optional

class MetadataLyricsExtractor:
    @staticmethod
    def extract_from_file(file_path: str) -> Optional[str]:
        """Extrae letras de los metadatos ID3"""
        try:
            audio = ID3(file_path)
            if 'USLT::eng' in audio:
                return audio['USLT::eng'].text
            return None
        except Exception as e:
            print(f"Error extrayendo letras: {e}")
            return None
        
    def get_metadata_for_api(file_path: str) -> tuple:
        """Extrae artista/título para búsqueda en API"""
        audio = ID3(file_path)
        artist = audio.get('TPE1', ['Unknown'])[0]
        title = audio.get('TIT2', ['Unknown'])[0]
        return artist, title