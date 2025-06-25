###DEMO PARA PROBAR MODULOS PREVIOS A GENERACION DE IMAGENES###
# import sys
# from pathlib import Path
# from audio_processor.event_generation import EventGenerator
# from lyrics_handler import LyricsHandler
# from album_processor import AlbumProcessor

# def main(audio_path: str):
#     # 1. Procesar audio
#     print("🔊 Procesando audio (esto puede tomar unos segundos)...")
#     audio_events = EventGenerator().generate_events(audio_path)

#     print(f"🎵 Tempo: {audio_events['metadata']['tempo']:.1f} BPM")
#     print(f"⏱️ Duración: {audio_events['metadata']['duration']:.1f}s")
#     print(f"✨ Eventos detectados: {audio_events['metadata']['total_events']}")
        
#     # 2. Procesar letras
#     print("\n📝 Buscando letras...")
#     events_with_lyrics = LyricsHandler().process(audio_path, audio_events['events'])
    
#     # 3. Mostrar resultados
#     print("\n🎤 Letras sincronizadas:")
#     print(f"Canción: {Path(audio_path).stem}")
#     print(f"Tempo: {audio_events['metadata']['tempo']:.1f} BPM")
#     print(f"Duración: {audio_events['metadata']['duration']:.2f}s")
#     print("\nFragmentos sincronizados:")
#     for event in events_with_lyrics[:7]:
#         print(f"{event['start_time']:.2f}s \t- {event['end_time']:.2f}s \t| "
#               f"{event['type']}     \t(Intensidad: {event['intensity']:.2f})\t   letra: {event.get('lyric')}")
    
#     #4. Procesar portada del álbum
#     album_processor = AlbumProcessor(n_colors=5)
#     color_palette = album_processor.process_album(audio_path)
    
#     if color_palette:
#         print("\n🎨 Paleta de colores extraída:")
#         print(f"HEX: {color_palette['hex_colors']}")
#         # print(f"RGB: {color_palette['rgb_colors']}")
#         print(f"Descripción para prompt: {color_palette['prompt_description']}")
#     else:
#         print("\n⚠ No se encontró portada en los metadatos")
            

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Uso: python demo.py <ruta_al_audio.mp3>")
#         sys.exit(1)
    
#     audio_file = Path(sys.argv[1])
#     if audio_file.exists():
#         main(str(audio_file))
#     else:
#         print(f"Error: Archivo {audio_file} no encontrado")

import sys
from audio_processor.event_generation import EventGenerator
from lyrics_handler import LyricsHandler
from album_processor import AlbumProcessor
from image_generator import ImageGenerator
from video_composer.text_renderer import ArtisticTextRenderer
from video_composer.video_export import VideoExporter
import os

def process_song(file_path: str, output_dir: str, style_preset="minimal_geometric"):
    # 1. Procesamiento de audio
    print("🔊 Procesando audio (esto puede tomar unos segundos)...")
    audio_analysis = EventGenerator().generate_events(file_path)
    print(f"🔊 eventos encontrados: {len(audio_analysis["events"])}")
    
    # 2. Procesamiento de letras
    print("\n📝 Buscando letras...")
    events_with_lyrics = LyricsHandler().process(file_path, 
                                                 audio_analysis["events"])
    print(f"📝 eventos mas letra: {len(events_with_lyrics)}")
    
    # 3. Procesamiento de portada del álbum
    album_processor = AlbumProcessor(n_colors=5)
    print("\n💿 Buscando colores...")
    color_palette = album_processor.process_album(file_path)
    print(f"💿 colores encontrados: {color_palette}")
    
    # 4. Crear directorio para imágenes
    image_dir = os.path.join(output_dir, "images")
    os.makedirs(image_dir, exist_ok=True)
    
    # 5. Generar imágenes
    print("\n📸 Generando imagenes...")
    image_generator = ImageGenerator()
    image_generator.generate_images(
        events_with_lyrics,
        output_dir=image_dir,
        style_preset=style_preset,
        color_palette=color_palette
    )

    # 6. Añadir texto a las imágenes
    print("\n💬 Agregando letra a imagenes...")
    if events_with_lyrics:
        text_renderer = ArtisticTextRenderer()
        text_renderer.process_image_directory(image_dir, events_with_lyrics,color_palette)

    # 7. Crear video final
    print("\n🎥 Exportando video...")
    video_exporter = VideoExporter()
    
    # Preparar ruta de salida
    song_name = os.path.splitext(os.path.basename(file_path))[0]
    output_video = os.path.join(output_dir, f"{song_name}_video.mp4")
    
    # Crear video
    video_exporter.create_video(image_dir, file_path, events_with_lyrics, output_video)
    
    print("✅ Proceso completado exitosamente!")
    print(f"🎬 Video exportado a: {output_video}")
    return output_video

    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python demo.py <ruta_al_mp3> [estilo]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    style = sys.argv[2] if len(sys.argv) > 2 else "minimal_geometric"
    output_dir = os.path.splitext(os.path.basename(file_path))[0]
    
    result = process_song(file_path, output_dir, style)
    # print(f"Total eventos procesados: {len(result['audio_events'])}")