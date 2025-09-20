import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
import requests
import time
from typing import List, Dict, Optional

class ColorPaletteExtractor:
    def __init__(self, n_colors=5, resize=(200, 200)):
        self.n_colors = n_colors
        self.resize = resize
    
    def extract_palette(self, image_path: str) -> dict:
        """Extrae la paleta de colores dominantes de una imagen
        
        Returns:
            Diccionario con:
            - 'hex_colors': Lista de colores HEX (#RRGGBB)
            - 'rgb_colors': Lista de tuplas RGB
            - 'color_names': Nombres aproximados de colores
        """
        # 1. Cargar y redimensionar imagen
        img = Image.open(image_path)
        img = img.resize(self.resize)
        img_array = np.array(img)
        
        # 2. Convertir a lista de píxeles
        if img_array.shape[2] == 4:  # Imagen con canal alpha
            mask = img_array[:, :, 3] > 128  # Máscara para píxeles no transparentes
            pixels = img_array[mask][:, :3]
        else:
            pixels = img_array.reshape(-1, 3)
        
        # 3. Aplicar K-Means
        kmeans = KMeans(n_clusters=self.n_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # 4. Obtener colores dominantes
        colors = kmeans.cluster_centers_.astype(int)
        
        # 5. Ordenar por frecuencia
        counts = np.bincount(kmeans.labels_)
        sorted_indices = np.argsort(counts)[::-1]
        sorted_colors = colors[sorted_indices]
        
        # 6. Convertir a HEX
        hex_colors = [self.rgb_to_hex(color) for color in sorted_colors]

        # 7. Obtener nombres de colores
        color_names = []
        for color in hex_colors:
            name = self.get_color_name(color)
            if name:
                color_names.append(name)
        
        return {
            'hex_colors': hex_colors,
            'rgb_colors': [tuple(color) for color in sorted_colors],
            'prompt_description': self.create_prompt_description(color_names)
        }
    
    @staticmethod
    def rgb_to_hex(rgb: tuple) -> str:
        """Convierte un color RGB a formato HEX"""
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
    
    def get_color_name(self, hex_color: str, max_retries=3) -> Optional[str]:
        """Obtiene el nombre del color usando The Color API con manejo de errores"""
        hex_code = hex_color.lstrip('#')
        if not hex_code:
            return None
        
        api_url = f"https://www.thecolorapi.com/id?hex={hex_code}"
        
        for attempt in range(max_retries):
            try:
                response = requests.get(api_url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    color_name = data['name']['value']
                    return color_name
            except (requests.RequestException, KeyError):
                time.sleep(0.5 * (attempt + 1))  # Espera exponencial
    
    def create_prompt_description(self, color_names: list) -> str:
        """Crea una descripción de paleta para prompts de Stable Diffusion"""
        # Remover duplicados manteniendo orden
        unique_names = []
        for name in color_names:
            if name not in unique_names:
                unique_names.append(name)
        
        if len(unique_names) == 1:
            return f"dominant color: {unique_names[0]}"
        
        return f"color palette: {', '.join(unique_names[:5])}"