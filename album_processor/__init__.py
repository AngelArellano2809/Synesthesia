from .cover_extractor import CoverExtractor
from .color_palette import ColorPaletteExtractor
import os

class AlbumProcessor:
    def __init__(self, n_colors=5):
        self.n_colors = n_colors
        self.cover_extractor = CoverExtractor()
        self.palette_extractor = ColorPaletteExtractor(n_colors=n_colors)
    
    def process_album(self, mp3_path: str) -> dict:
        """Procesa un archivo MP3 para extraer paleta de colores de la portada
        
        Returns:
            Diccionario con información de la paleta o None si no hay portada
        """
        cover_path = self.cover_extractor.extract_cover(mp3_path)
        if not cover_path:
            return None
        
        palette = self.palette_extractor.extract_palette(cover_path)
        
        # Limpiar archivo temporal
        try:
            os.unlink(cover_path)
        except:
            pass
        
        return palette