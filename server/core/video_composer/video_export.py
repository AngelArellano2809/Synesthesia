import os
import re
from typing import List
from moviepy import *
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from server.core.config import Config

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
        
        # # 2. Crear clip de video
        # video_clip = ImageSequenceClip(
        #     [clip['path'] for clip in clips],
        #     durations=[clip['duration'] for clip in clips],
        #     fps=self.fps
        # )

        # 2. Crear clip de video compuesto
        video_clips = []
        last_end = 0
        
        # Crear clips con duraciones exactas basadas en eventos
        for clip in clips:
            # Añadir espacio negro si hay un gap entre clips
            if clip['start_time'] > last_end:
                gap_duration = clip['start_time'] - last_end
                gap_clip = self.create_black_clip(gap_duration)
                video_clips.append(gap_clip)
            
            # Crear clip de imagen
            img_clip = ImageClip(clip['path'], duration=clip['duration'])
            video_clips.append(img_clip)
            last_end = clip['start_time'] + clip['duration']
        
        # Combinar todos los clips
        final_video = concatenate_videoclips(video_clips, method="compose")
        
        # 3. Añadir audio
        audio_clip = AudioFileClip(audio_path)
        final_clip = final_video.with_audio(audio_clip)
        
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
            return []
        
        # Preparar clips ordenados por tiempo
        clips = []
        sorted_times = sorted(image_map.keys())
        
        # # Para cada evento, calcular la duración de la imagen
        # for i in range(len(event_times)):
        #     start_time = event_times[i]
        #     end_time = event_times[i + 1] if i < len(event_times) - 1 else start_time + 5.0
        #     duration = end_time - start_time
            
        #     clips.append({
        #         'path': image_map[start_time],
        #         'duration': duration,
        #         'start_time': start_time
        #     })
        
        # return clips

        # Para cada tiempo de imagen, encontrar el evento correspondiente
        for i, time_val in enumerate(sorted_times):
            # Encontrar el evento que coincide con este tiempo
            matching_event = next((e for e in events if abs(e['start_time'] - time_val) < 0.1), None)
            
            if matching_event:
                # Calcular duración hasta el próximo evento
                if i < len(sorted_times) - 1:
                    next_time = sorted_times[i + 1]
                    duration = next_time - time_val
                else:
                    # Para la última imagen, usar la duración restante
                    duration = events[-1]['end_time'] - time_val
                    if duration <= 0:
                        duration = 5.0  # Duración por defecto
                
                clips.append({
                    'path': image_map[time_val],
                    'start_time': time_val,
                    'duration': duration,
                    'event': matching_event
                })
        
        return clips

    def add_transitions(self, clips: List[dict], transition_duration: float = 0.5) -> List[dict]:
        """Añade transiciones entre clips (opcional)"""
        # Esta implementación es conceptual - MoviePy no soporta transiciones nativas fácilmente
        # En una implementación real, usaríamos composición con superposiciones
        print("⚠ Las transiciones avanzadas requieren implementación adicional")
        return clips