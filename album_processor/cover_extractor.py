from mutagen.id3 import ID3
from mutagen.mp3 import MP3
import tempfile
import os

class CoverExtractor:
    @staticmethod
    def extract_cover(mp3_path: str, output_dir: str = None):
        """Extrae la portada de un MP3 y guarda como archivo temporal"""
        audio = MP3(mp3_path, ID3=ID3)
        
        for tag in audio.tags.values():
            if tag.FrameID == 'APIC':  # Portada incrustada
                ext = 'jpg' if tag.mime == 'image/jpeg' else 'png'
                temp_path = os.path.join(
                    output_dir or tempfile.gettempdir(),
                    f"cover_{os.path.basename(mp3_path)}.{ext}"
                )
                with open(temp_path, 'wb') as f:
                    f.write(tag.data)
                return temp_path
        return None