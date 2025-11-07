from server.core.audio_processor.event_generation import EventGenerator
from server.core.lyrics_handler import LyricsHandler
from server.core.album_processor import AlbumProcessor
from server.core.image_generator import ImageGenerator
from server.core.video_composer.text_renderer import ArtisticTextRenderer
from server.core.video_composer.video_export import VideoExporter
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import json
import os
import tempfile
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import logging


def extract_audio_metadata(mp3_path):
    """
    Extrae metadatos básicos del archivo MP3 usando el mismo método que en lyrics_handler
    """
    try:
        audio = MP3(mp3_path, ID3=ID3)
        metadata = {}
        
        # Extraer título - usando el mismo método que en _get_metadata
        title_tag = audio.tags.get('TIT2')
        if title_tag:
            metadata['title'] = str(title_tag.text[0])
        else:
            metadata['title'] = Path(mp3_path).stem
        
        # Extraer artista
        artist_tag = audio.tags.get('TPE1')
        if artist_tag:
            metadata['artist'] = str(artist_tag.text[0])
        else:
            metadata['artist'] = 'Unknown Artist'
        
        # Extraer álbum
        album_tag = audio.tags.get('TALB')
        if album_tag:
            metadata['album'] = str(album_tag.text[0])
        else:
            metadata['album'] = 'Unknown Album'
        
        # Duración
        metadata['duration'] = audio.info.length
        
        print(f" Metadatos extraídos: {metadata['title']} - {metadata['artist']}\n")
        return metadata
        
    except Exception as e:
        print(f" Error extrayendo metadatos: {e}\n")
        return {
            'title': Path(mp3_path).stem,
            'artist': 'Unknown Artist',
            'album': 'Unknown Album',
            'duration': 0
        }

def extract_album_cover(mp3_path):
    """
    Extrae la portada del álbum de un archivo MP3 usando el mismo método que en AlbumProcessor
    """
    try:
        audio = MP3(mp3_path, ID3=ID3)
        
        # Buscar todas las imágenes (puede haber varias)
        images = []
        for tag in audio.tags.values():
            if isinstance(tag, APIC):
                images.append(tag)
        
        if not images:
            print("ℹ No se encontraron imágenes en los metadatos del MP3\n")
            return None
            
        # Seleccionar la imagen de mayor tamaño (asumimos que es la portada)
        largest_image = max(images, key=lambda img: len(img.data))
        
        # Determinar extensión basada en el MIME type
        if largest_image.mime == 'image/jpeg':
            ext = 'jpg'
        elif largest_image.mime == 'image/png':
            ext = 'png'
        else:
            ext = 'jpg'  # fallback
        
        # Crear archivo temporal
        temp_cover = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{ext}')
        temp_cover.write(largest_image.data)
        temp_cover.close()
        
        print(f" Portada extraída y guardada en: {temp_cover.name}\n")
        return temp_cover.name
        
    except Exception as e:
        print(f" No se pudo extraer portada: {e}\n")
        return None

def inject_video_metadata(video_path, metadata, cover_path=None):
    """
    Inyecta metadatos y portada del álbum en el archivo de video usando ffmpeg
    """
    try:
        # Crear archivo temporal para el output
        temp_path = str(Path(video_path).with_suffix('.temp.mp4'))
        
        # Construir comando base de ffmpeg
        cmd = [
            'ffmpeg',
            '-i', video_path,  # Input video
        ]
        
        # Agregar portada si está disponible
        if cover_path and os.path.exists(cover_path):
            cmd.extend(['-i', cover_path])  # Input imagen de portada
            print(f" Portada encontrada, agregando al video: {cover_path}\n")
        
        # Agregar metadatos
        cmd.extend([
            '-map', '0',  # Usar todos los streams del video original
            '-c', 'copy',  # Copiar sin re-encoding para mantener calidad
            '-metadata', f'title={metadata.get("title", "Synesthesia Video")}',
            '-metadata', f'artist={metadata.get("artist", "Unknown Artist")}',
            '-metadata', f'album={metadata.get("album", "Unknown Album")}',
            '-metadata', f'comment=Generated with Synesthesia | Preset: {metadata.get("preset", "unknown")}',
            '-metadata', f'creation_time={datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}',
        ])
        
        # Si hay portada, agregarla como stream de imagen
        if cover_path and os.path.exists(cover_path):
            cmd.extend([
                '-map', '1',  # Usar la imagen como segundo stream
                '-disposition:v:1', 'attached_pic',  # Marcar como portada adjunta
            ])
        
        cmd.append(temp_path)
        
        # Ejecutar ffmpeg
        print(f" Ejecutando comando ffmpeg para inyectar metadatos...\n")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # Reemplazar archivo original con el que tiene metadatos
            os.replace(temp_path, video_path)
            print(f" Metadatos y portada inyectados exitosamente en: {video_path}\n")
            return True
        else:
            print(f" Error inyectando metadatos: {result.stderr}\n")
            # Limpiar archivo temporal en caso de error
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            return False
            
    except subprocess.TimeoutExpired:
        print(" Timeout inyectando metadatos\n")
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        return False
    except Exception as e:
        print(f" Excepción inyectando metadatos: {e}\n")
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        return False
    
def verify_video_metadata(video_path):
    """
    Verifica los metadatos de un video usando ffprobe
    """
    try:
        cmd = [
            'ffprobe', 
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            metadata = json.loads(result.stdout)
            format_info = metadata.get('format', {})
            tags = format_info.get('tags', {})
            
            print(" Verificación de metadatos del video:\n")
            print(f"    Título: {tags.get('title', 'N/A')}\n")
            print(f"    Artista: {tags.get('artist', 'N/A')}\n")
            print(f"    Álbum: {tags.get('album', 'N/A')}\n")
            
            # Verificar si hay stream de imagen (portada)
            streams = metadata.get('streams', [])
            has_cover = any(
                stream.get('disposition', {}).get('attached_pic', 0) == 1 
                for stream in streams
            )
            print(f"  Portada incluida: {'' if has_cover else ''}\n")
            
            return True
        else:
            print(" No se pudieron verificar los metadatos\n")
            return False
            
    except Exception as e:
        print(f" Error verificando metadatos: {e}\n")
        return False
    
def save_updated_metadata(video_path, metadata):
    """
    Guarda los metadatos actualizados en el archivo .syn
    """
    try:
        syn_path = Path(video_path).with_suffix('.syn')
        
        # Si ya existe un archivo .syn, cargarlo y actualizarlo
        existing_metadata = {}
        if syn_path.exists():
            try:
                with open(syn_path, 'r', encoding='utf-8') as f:
                    existing_metadata = json.load(f)
            except:
                pass
        
        # Combinar con los nuevos metadatos
        updated_metadata = {**existing_metadata, **metadata}
        
        # Guardar el archivo actualizado
        with open(syn_path, 'w', encoding='utf-8') as f:
            json.dump(updated_metadata, f, indent=2, ensure_ascii=False)
        
        print(f" Metadatos actualizados en: {syn_path}\n")
        return True
        
    except Exception as e:
        print(f" Error guardando metadatos actualizados: {e}\n")
        return False

def process_song(file_path: str, output_dir: str, style_preset="minimal_geometric"):
    logger = logging.getLogger(__name__)
    # 0. Extraer metadatos y portada ANTES de procesar
    print(" Extrayendo metadatos y portada del audio...\n")
    audio_metadata = extract_audio_metadata(file_path)
    cover_path = extract_album_cover(file_path)
    
    print(f"   Título: {audio_metadata.get('title', 'N/A')}\n")
    print(f"   Artista: {audio_metadata.get('artist', 'N/A')}\n")
    print(f"   Álbum: {audio_metadata.get('album', 'N/A')}\n")
    print(f"   Duración: {audio_metadata.get('duration', 0):.2f} segundos\n")
    print(f"   Portada: {' Encontrada' if cover_path else ' No encontrada'}\n")

    # 1. Procesamiento de audio
    print(" Procesando audio (esto puede tomar unos segundos)...\n")
    audio_analysis = EventGenerator().generate_events(file_path)
    print(f" eventos encontrados: {len(audio_analysis["events"])}\n")
    
    # 2. Procesamiento de letras
    print("\n Buscando letras...\n")
    events_with_lyrics = LyricsHandler().process(file_path, 
                                                 audio_analysis["events"])
    print(f" eventos mas letra: {len(events_with_lyrics)}\n")
    
    # 3. Procesamiento de portada del álbum
    album_processor = AlbumProcessor(n_colors=5)
    print("\n Buscando colores...\n")
    color_palette = album_processor.process_album(file_path)
    print(f" colores encontrados: {color_palette}\n")
    
    # 4. Crear directorio para imágenes
    image_dir = os.path.join(output_dir, "images")
    os.makedirs(image_dir, exist_ok=True)
    
    # 5. Generar imágenes
    print("\n Generando imagenes...\n")
    image_generator = ImageGenerator()
    image_generator.generate_images(
        events_with_lyrics,
        output_dir=image_dir,
        style_preset=style_preset,
        color_palette=color_palette
    )

    # 6. Añadir texto a las imágenes
    print("\n Agregando letra a imagenes...\n")
    if events_with_lyrics:
        text_renderer = ArtisticTextRenderer()
        text_renderer.process_image_directory(image_dir, events_with_lyrics,color_palette)

    # 7. Crear video final
    print("\n Exportando video...\n")
    video_exporter = VideoExporter()
    
    # Preparar ruta de salida
    output_video = os.path.join(output_dir, "video.mp4")
    
    # Crear video
    video_exporter.create_video(image_dir, file_path, events_with_lyrics, output_video)

    # 8. INYECTAR METADATOS Y PORTADA + ACTUALIZAR ARCHIVO .SYN
    print("\n📋 Inyectando metadatos y portada en el video...\n")

    # Combinar metadatos COMPLETOS para el archivo .syn
    final_metadata = {
        'title': audio_metadata.get('title', 'Unknown'),
        'artist': audio_metadata.get('artist', 'Unknown Artist'),
        'album': audio_metadata.get('album', 'Unknown Album'),
        'duration': audio_metadata.get('duration', 0),
        'preset': style_preset,
        'events_count': len(events_with_lyrics),
        'color_palette': color_palette.get('hex_colors', []) if color_palette else [],
        'created_at': datetime.now().isoformat(),
        'has_cover': cover_path is not None
    }

    # Inyectar metadatos en el video (para reproductores externos)
    video_success = inject_video_metadata(output_video, final_metadata, cover_path)

    # Guardar metadatos en archivo .syn (para tu interfaz)
    metadata_success = save_updated_metadata(output_video, final_metadata)

    # Limpiar archivo temporal de portada
    if cover_path and os.path.exists(cover_path):
        try:
            os.unlink(cover_path)
            print(" Archivo temporal de portada eliminado\n")
        except:
            pass

    if video_success and metadata_success:
        print(" Metadatos agregados al video Y al archivo .syn\n")
    else:
        print("⚠ Algunos metadatos no se pudieron guardar completamente\n")

    return output_video