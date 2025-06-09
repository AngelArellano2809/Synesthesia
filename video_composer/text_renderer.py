import os
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict
import numpy as np
from config import Config

class TextRenderer:
    def __init__(self, font_path: str = None, base_font_size: int = 40):
        self.cfg = Config.TEXT_RENDERING
        self.font_path = font_path or self.cfg['DEFAULT_FONT']
        self.base_font_size = base_font_size
        self.font_cache = {}
        
    def load_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Carga una fuente con tamaño específico (con cache)"""
        if size not in self.font_cache:
            try:
                self.font_cache[size] = ImageFont.truetype(self.font_path, size)
            except IOError:
                # Fallback a fuente básica
                self.font_cache[size] = ImageFont.load_default()
        return self.font_cache[size]
    
    def calculate_text_size(self, text: str, font_size: int) -> tuple:
        """Calcula el tamaño del texto para un tamaño de fuente dado"""
        font = self.load_font(font_size)
        # Usar una imagen temporal para medir
        temp_img = Image.new('RGB', (100, 100))
        draw = ImageDraw.Draw(temp_img)
        return draw.textbbox((0, 0), text, font=font)
    
    def calculate_optimal_font_size(self, text: str, max_width: int, max_height: int) -> int:
        """Calcula el tamaño de fuente máximo que cabe en el área designada"""
        # Empezar con el tamaño base e ir reduciendo hasta que quepa
        font_size = self.base_font_size
        while font_size > 8:
            _, _, w, h = self.calculate_text_size(text, font_size)
            if w <= max_width and h <= max_height:
                return font_size
            font_size -= 2
        return font_size
    
    def render_text_on_image(self, image_path: str, text: str, output_path: str = None):
        """Añade texto a una imagen existente"""
        if not text or not os.path.exists(image_path):
            return image_path
            
        if output_path is None:
            output_path = image_path
            
        try:
            # Abrir imagen
            img = Image.open(image_path).convert('RGBA')
            width, height = img.size
            
            # Crear capa para texto
            txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt_layer)
            
            # Calcular tamaño óptimo de fuente
            max_text_width = width * 0.8
            max_text_height = height * 0.15
            font_size = self.calculate_optimal_font_size(text, max_text_width, max_text_height)
            font = self.load_font(font_size)
            
            # Calcular posición
            _, _, text_width, text_height = self.calculate_text_size(text, font_size)
            x = (width - text_width) // 2
            y = height - text_height - self.cfg['BOTTOM_MARGIN']
            
            # Añadir fondo semitransparente
            padding = self.cfg['PADDING']
            bg_box = [
                x - padding, y - padding,
                x + text_width + padding, y + text_height + padding
            ]
            draw.rectangle(bg_box, fill=self.cfg['BACKGROUND_COLOR'])
            
            # Dibujar texto
            draw.text((x, y), text, font=font, fill=self.cfg['TEXT_COLOR'])
            
            # Combinar capas
            combined = Image.alpha_composite(img, txt_layer)
            combined.convert('RGB').save(output_path)
            return output_path
            
        except Exception as e:
            print(f"Error añadiendo texto a {image_path}: {e}")
            return image_path
    
    def process_image_directory(self, image_dir: str, events: List[Dict]):
        """Procesa todas las imágenes en un directorio basado en los eventos"""
        # Crear un mapa de texto por tiempo para búsqueda rápida
        text_map = {e['start_time']: e.get('lyric', '') for e in events}
        
        # Procesar cada imagen en el directorio
        for filename in os.listdir(image_dir):
            if filename.endswith('.png'):
                # Extraer tiempo del nombre de archivo (ej: "12.34s.png")
                try:
                    time_str = filename.split('s')[0]
                    event_time = float(time_str)
                    
                    # Encontrar el evento más cercano
                    closest_time = min(text_map.keys(), key=lambda t: abs(t - event_time))
                    text = text_map[closest_time]
                    
                    # Procesar imagen
                    image_path = os.path.join(image_dir, filename)
                    self.render_text_on_image(image_path, text)
                    print(f"Texto añadido a {filename}: '{text[:20]}...'")
                except ValueError:
                    continue