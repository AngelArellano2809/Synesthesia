import os
import re
from typing import List
from moviepy import *
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from config import Config

class VideoExporter:
    def __init__(self, fps: int = None):
        self.cfg = Config.VIDEO
        self.fps = fps or self.cfg['FPS']
    
    def create_video(self, image_dir: str, audio_path: str, events: List[dict], output_path: str):
        """
        Crea un video a partir de imágenes y audio, sincronizado con eventos
        
        Args:
            image_dir: Directorio con imágenes generadas
            audio_path: Ruta al archivo de audio original
            events: Lista de eventos con tiempos
            output_path: Ruta de salida para el video
        """
        # 1. Preparar lista de imágenes con duraciones
        clips = self.prepare_clips(image_dir, events)
        
        # 2. Crear clip de video
        video_clip = ImageSequenceClip(
            [clip['path'] for clip in clips],
            durations=[clip['duration'] for clip in clips],
            fps=self.fps
        )
        
        # 3. Añadir audio
        audio_clip = AudioFileClip(audio_path)
        final_clip = video_clip.with_audio(audio_clip)
        
        # 4. Exportar video
        print(f"Exportando video a {output_path}...")
        final_clip.write_videofile(
            output_path,
            fps=self.fps,
            audio_codec='aac',
            # verbose=False,
            logger=None
        )
        return output_path

    def prepare_clips(self, image_dir: str, events: List[dict]) -> List[dict]:
        """Prepara la lista de clips con sus rutas y duraciones"""
        # Obtener todas las imágenes del directorio
        image_files = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg'))]
        
        # Crear un diccionario de tiempo -> ruta de imagen
        image_map = {}
        for filename in image_files:
            try:
                # Extraer tiempo del nombre de archivo (ej: "12.34s.png")
                time_str = re.search(r'^([\d.]+)s', filename).group(1)
                time_val = float(time_str)
                image_map[time_val] = os.path.join(image_dir, filename)
            except (ValueError, AttributeError):
                continue
        
        # Si no encontramos imágenes, usar una imagen negra
        if not image_map:
            print("⚠ No se encontraron imágenes. Usando fondo negro.")
            black_image = self.create_black_image(1920, 1080)
            return [{'path': black_image, 'duration': 10.0}]
        
        # Preparar clips ordenados por tiempo
        clips = []
        event_times = sorted(image_map.keys())
        
        # Para cada evento, calcular la duración de la imagen
        for i in range(len(event_times)):
            start_time = event_times[i]
            end_time = event_times[i + 1] if i < len(event_times) - 1 else start_time + 5.0
            duration = end_time - start_time
            
            clips.append({
                'path': image_map[start_time],
                'duration': duration,
                'start_time': start_time
            })
        
        return clips
    
    def create_black_image(self, width: int, height: int) -> str:
        """Crea una imagen negra temporal para usar cuando no hay imágenes"""
        from PIL import Image
        temp_path = os.path.join(os.getcwd(), "black_background.png")
        if os.path.exists(temp_path):
            return temp_path
            
        img = Image.new('RGB', (width, height), color='black')
        img.save(temp_path)
        return temp_path

    def add_transitions(self, clips: List[dict], transition_duration: float = 0.5) -> List[dict]:
        """Añade transiciones entre clips (opcional)"""
        # Esta implementación es conceptual - MoviePy no soporta transiciones nativas fácilmente
        # En una implementación real, usaríamos composición con superposiciones
        print("⚠ Las transiciones avanzadas requieren implementación adicional")
        return clips