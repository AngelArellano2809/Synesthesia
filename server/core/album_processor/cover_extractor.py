import tempfile
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3

class CoverExtractor:
    @staticmethod
    def extract_cover(mp3_path: str) -> str:
        """Extrae la portada de un MP3 y guarda como archivo temporal
        
        Returns:
            Ruta del archivo temporal de la imagen o None si no hay portada
        """
        try:
            audio = MP3(mp3_path, ID3=ID3)
            
            # Buscar todas las imágenes (puede haber varias)
            images = []
            for tag in audio.tags.values():
                if isinstance(tag, APIC):
                    images.append(tag)
            
            if not images:
                return None
                
            # Seleccionar la imagen de mayor tamaño (asumimos que es la portada)
            largest_image = max(images, key=lambda img: len(img.data))
            
            # Determinar extensión
            ext = 'jpg' if largest_image.mime == 'image/jpeg' else 'png'
            
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{ext}') as temp_file:
                temp_file.write(largest_image.data)
                return temp_file.name
                
        except Exception as e:
            print(f"Error extrayendo portada: {e}")
            return None