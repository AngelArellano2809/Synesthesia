import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from typing import List, Tuple
import matplotlib.colors as mcolors

class ColorExtractor:
    def __init__(self, n_colors: int = 3):
        self.n_colors = n_colors
    
    def extract_colors(self, image_path: str) -> List[Tuple[str, Tuple[int, int, int]]]:
        """Extrae la paleta de colores dominantes usando K-Means"""
        # 1. Cargar imagen
        img = Image.open(image_path)
        img_array = np.array(img)
        
        # 2. Preprocesamiento (redimensionar para eficiencia)
        small_img = img.resize((100, 100))
        pixels = np.array(small_img).reshape(-1, 3)
        
        # 3. K-Means para encontrar colores dominantes
        kmeans = KMeans(n_clusters=self.n_colors, random_state=42)
        kmeans.fit(pixels)
        
        # 4. Convertir centros a RGB y HEX
        colors = []
        for center in kmeans.cluster_centers_:
            rgb = tuple(np.round(center).astype(int))
            hex_color = mcolors.rgb2hex(np.array(rgb)/255)
            colors.append((hex_color, rgb))
        
        # Ordenar por frecuencia (opcional)
        return sorted(colors, key=lambda x: -np.sum(x[1]))

    def get_contrast_color(self, rgb_color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Calcula un color contrastante (para texto)"""
        luminance = 0.299*rgb_color[0] + 0.587*rgb_color[1] + 0.114*rgb_color[2]
        return (255, 255, 255) if luminance < 128 else (0, 0, 0)