import os
import hashlib
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
from typing import List, Dict, Tuple, Optional
from ..config import Config
import random

class ArtisticTextRenderer:
    def __init__(self, font_path: str = None, base_font_size: int = 60):
        self.cfg = Config.TEXT_RENDERING
        self.font_path = font_path or self.cfg['DEFAULT_FONT']
        self.base_font_size = base_font_size
        self.font_cache = {}
        self.template_cache = {}
        
    def load_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Carga una fuente con tamaño específico (con cache)"""
        key = f"{self.font_path}_{size}"
        if key not in self.font_cache:
            try:
                self.font_cache[key] = ImageFont.truetype(self.font_path, size)
            except IOError:
                # Fallback a fuente básica
                self.font_cache[key] = ImageFont.load_default()
                print(f"⚠ No se pudo cargar la fuente {self.font_path}. Usando fuente por defecto.")
        return self.font_cache[key]
    
    def calculate_text_bbox(self, text: str, font: ImageFont.FreeTypeFont) -> Tuple[int, int, int, int]:
        """Calcula el cuadro delimitador del texto"""
        # Usar un método más preciso para obtener el bbox
        return font.getbbox(text)
    
    def calculate_text_size(self, text: str, font: ImageFont.FreeTypeFont) -> Tuple[int, int]:
        """Calcula ancho y alto del texto"""
        left, top, right, bottom = self.calculate_text_bbox(text, font)
        return right - left, bottom - top
    
    def calculate_optimal_font_size(self, text: str, max_width: int, max_height: int) -> int:
        """Calcula el tamaño de fuente máximo que cabe en el área designada"""
        font_size = self.base_font_size
        while font_size > 15:
            font = self.load_font(font_size)
            text_width, text_height = self.calculate_text_size(text, font)
            if text_width <= max_width and text_height <= max_height:
                return font_size
            font_size -= 2
        return max(15, font_size)  # Tamaño mínimo
    
    def get_template_id(self, text: str) -> int:
        """Genera un ID de plantilla consistente para el mismo texto"""
        # Usar hash del texto para que la misma estrofa siempre tenga la misma plantilla
        return int(hashlib.sha256(text.encode()).hexdigest(), 16) % 8
    
    def get_text_position_and_anchor(self, template_id: int, img_width: int, img_height: int) -> Tuple[Tuple[int, int], str]:
        """Obtiene la posición y código de anclaje basado en la plantilla"""
        if template_id == 0:  # Centro dominante
            return (img_width // 2, img_height // 3), 'mm'
        elif template_id == 1:  # Centro inferior
            return (img_width // 2, img_height - img_height // 4), 'md'
        elif template_id == 2:  # Diagonal superior izquierda
            return (img_width // 6, img_height // 4), 'la'
        elif template_id == 3:  # Diagonal inferior derecha
            return (img_width - img_width // 6, img_height - img_height // 4), 'rd'
        elif template_id == 4:  # Izquierda centro
            return (img_width // 10, img_height // 2), 'lm'
        elif template_id == 5:  # Derecha centro
            return (img_width - img_width // 10, img_height // 2), 'rm'
        elif template_id == 6:  # Superior centro con ángulo
            return (img_width // 2, img_height // 5), 'ma'
        else:  # Aleatorio dentro de márgenes
            x = random.randint(img_width // 10, img_width - img_width // 10)
            y = random.randint(img_height // 5, img_height - img_height // 3)
            return (x, y), 'mm'
    
    def get_text_color(self, palette: List[str], position: Tuple[int, int], img: Image.Image) -> Tuple[int, int, int, int]:
        """Determina el color del texto basado en la paleta y la posición en la imagen"""
        if palette:
            # Convertir colores HEX a RGB
            rgb_colors = []
            for hex_color in palette:
                hex_color = hex_color.lstrip('#')
                if len(hex_color) == 6:
                    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                    rgb_colors.append(rgb)
            
            if rgb_colors:
                # Seleccionar un color aleatorio de la paleta pero consistente por posición
                color_index = (position[0] + position[1]) % len(rgb_colors)
                return rgb_colors[color_index] + (255,)  # Añadir alpha
        
        # Fallback: color blanco con transparencia
        return (255, 255, 255, 255)
    
    def create_shadow_effect(self, text_image: Image.Image, blur_radius: int = 3) -> Image.Image:
        """Crea un efecto de sombra para el texto"""
        # Crear máscara de alpha
        alpha = text_image.split()[3]
        blurred_alpha = alpha.filter(ImageFilter.GaussianBlur(blur_radius))
        
        # Crear imagen de sombra (negro con alpha difuminado)
        shadow = Image.new('RGBA', text_image.size, (0, 0, 0, 0))
        shadow.putalpha(blurred_alpha)
        return shadow
    
    def apply_text_effects(self, draw: ImageDraw.Draw, position: Tuple[int, int], text: str, 
                          font: ImageFont.FreeTypeFont, text_color: Tuple[int, int, int, int], 
                          anchor: str = 'mm'):
        """Aplica efectos de texto (borde, sombra) con anclaje válido"""
        # Validar anchor
        if len(anchor) != 2 or anchor[0] not in ['l', 'm', 'r'] or anchor[1] not in ['a', 'm', 'd']:
            anchor = 'mm'  # Default seguro

        # Color de borde (contrario al texto)
        border_color = (0, 0, 0, 255) if sum(text_color[:3]) > 384 else (255, 255, 255, 255)
        border_width = max(2, font.size // 20) 
        
        # Dibujar borde
        for dx in [-border_width, 0, border_width]:
            for dy in [-border_width, 0, border_width]:
                if dx != 0 or dy != 0:
                    draw.text((position[0] + dx, position[1] + dy), text, 
                             font=font, fill=border_color, anchor=anchor)
        
        # Dibujar texto principal
        draw.text(position, text, font=font, fill=text_color, anchor=anchor)
    
    def render_lyric_artistically(self, image_path: str, text: str, output_path: str = None, palette: Optional[List[str]] = None):
        """Añade texto artístico a una imagen existente con efectos avanzados"""
        if not text or not os.path.exists(image_path):
            return image_path
            
        if output_path is None:
            output_path = image_path
            
        try:
            # Abrir imagen y asegurar modo RGBA
            img = Image.open(image_path)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            width, height = img.size
            
            # Obtener ID de plantilla basado en el texto
            template_id = self.get_template_id(text)
            
            # Calcular tamaño de fuente óptimo (usamos un 70% del ancho y 15% del alto)
            max_text_width = width * 0.7
            max_text_height = height * 0.15
            font_size = self.calculate_optimal_font_size(text, max_text_width, max_text_height)
            font = self.load_font(font_size)

            # Obtener posición y código de anclaje
            position, anchor = self.get_text_position_and_anchor(template_id, width, height)
            
            # Obtener color del texto
            text_color = self.get_text_color(palette, position, img)
            
            # Crear capa para texto
            txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt_layer)
            
            # Aplicar efectos de texto
            self.apply_text_effects(draw, position, text, font, text_color, anchor)
            
            # Crear efecto de sombra
            shadow_layer = self.create_shadow_effect(txt_layer)

            # Combinar capas: fondo + sombra + texto
            final_image = Image.alpha_composite(img, shadow_layer)
            final_image = Image.alpha_composite(final_image, txt_layer)
            
            # Guardar resultado
            final_image.save(output_path)
            return output_path
            
        except Exception as e:
            print(f"Error añadiendo texto artístico a {image_path}: {e}")
            return image_path
    
    def process_image_directory(self, image_dir: str, events: List[Dict], palette: Optional[List[str]] = None):
        """Procesa todas las imágenes en un directorio basado en los eventos"""
        # Crear un mapa de texto por tiempo para búsqueda rápida
        text_map = {}
        for e in events:
            lyric = e.get('lyric', '')
            if lyric.strip():
                text_map[e['start_time']] = lyric
        
        # Procesar cada imagen en el directorio
        for filename in os.listdir(image_dir):
            if filename.endswith(('.png', '.jpg')):
                try:
                    # Extraer tiempo del nombre de archivo
                    time_str = filename.split('s')[0]
                    event_time = float(time_str)
                    
                    # Encontrar el texto más cercano en el tiempo
                    closest_time = min(text_map.keys(), key=lambda t: abs(t - event_time))
                    text = text_map[closest_time]
                    
                    # Procesar imagen
                    image_path = os.path.join(image_dir, filename)
                    self.render_lyric_artistically(image_path, text, palette=palette)
                    print(f"Texto añadido a {filename}: '{text[:20]}...'")
                except (ValueError, KeyError, OSError) as e:
                    print(f"Error procesando {filename}: {e}")
                    continue