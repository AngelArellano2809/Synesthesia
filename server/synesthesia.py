from server.core.audio_processor.event_generation import EventGenerator
from server.core.lyrics_handler import LyricsHandler
from server.core.album_processor import AlbumProcessor
from server.core.image_generator import ImageGenerator
from server.core.video_composer.text_renderer import ArtisticTextRenderer
from server.core.video_composer.video_export import VideoExporter
import os

def process_song(file_path: str, output_dir: str, style_preset="minimal_geometric"):
    # 1. Procesamiento de audio
    print(" Procesando audio (esto puede tomar unos segundos)...")
    audio_analysis = EventGenerator().generate_events(file_path)
    print(f" eventos encontrados: {len(audio_analysis["events"])}")
    
    # 2. Procesamiento de letras
    print("\n Buscando letras...")
    events_with_lyrics = LyricsHandler().process(file_path, 
                                                 audio_analysis["events"])
    print(f" eventos mas letra: {len(events_with_lyrics)}")
    
    # 3. Procesamiento de portada del álbum
    album_processor = AlbumProcessor(n_colors=5)
    print("\n Buscando colores...")
    color_palette = album_processor.process_album(file_path)
    print(f" colores encontrados: {color_palette}")
    
    # 4. Crear directorio para imágenes
    image_dir = os.path.join(output_dir, "images")
    os.makedirs(image_dir, exist_ok=True)
    
    # 5. Generar imágenes
    print("\n Generando imagenes...")
    image_generator = ImageGenerator()
    image_generator.generate_images(
        events_with_lyrics,
        output_dir=image_dir,
        style_preset=style_preset,
        color_palette=color_palette
    )

    # 6. Añadir texto a las imágenes
    print("\n Agregando letra a imagenes...")
    if events_with_lyrics:
        text_renderer = ArtisticTextRenderer()
        text_renderer.process_image_directory(image_dir, events_with_lyrics,color_palette)

    # 7. Crear video final
    print("\n Exportando video...")
    video_exporter = VideoExporter()
    
    # Preparar ruta de salida
    # song_name = os.path.splitext(os.path.basename(file_path))[0]
    output_video = os.path.join(output_dir, "video.mp4")
    
    # Crear video
    video_exporter.create_video(image_dir, file_path, events_with_lyrics, output_video)
    
    print(" Proceso completado exitosamente!")
    print(f" Video exportado a: {output_video}")
    return output_video
