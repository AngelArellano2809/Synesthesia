
# from audio_processor.beat_detection import AudioAnalyzer

# def process_song(file_path: str):
#     # 1. Crear el analizador
#     analyzer = AudioAnalyzer()
    
#     # 2. Cargar audio y detectar tempo
#     y, tempo = analyzer.load_audio(file_path)
#     print(f"🎵 Tempo detectado: {tempo:.1f} BPM")
    
#     # 3. Detectar eventos clave
#     events = analyzer.detect_events(y)
#     print(f"⏱️ Eventos detectados: {len(events)}")
#     print("Primeros 5 eventos:", [f"{t:.2f}s" for t in events[:5]])

# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) < 2:
#         print("Uso: python demo.py [ruta_al_audio.mp3]")
#         sys.exit(1)
    
#     process_song(sys.argv[1])




# from audio_processor.event_generation import EventGenerator

# def process_song(file_path: str):
#     generator = EventGenerator()
#     analysis = generator.generate_events(file_path)
    
    # print(f"🎵 Tempo: {analysis['metadata']['tempo']:.1f} BPM")
    # print(f"⏱️ Duración: {analysis['metadata']['duration']:.1f}s")
    # print(f"✨ Eventos detectados: {analysis['metadata']['total_events']}")
    
    # print("\nPrimeros 5 eventos:")
    # for event in analysis['events'][:5]:
    #     print(f"{event['start_time']:.2f}s - {event['end_time']:.2f}s | "
    #           f"{event['type']} (Intensidad: {event['intensity']:.2f})")

# if __name__ == "__main__":
#     import sys
#     process_song(sys.argv[1])

import sys
from pathlib import Path
from audio_processor.event_generation import EventGenerator
from lyrics_handler import LyricsHandler

def main(audio_path: str):
    # 1. Procesar audio
    print("🔊 Procesando audio (esto puede tomar unos segundos)...")
    audio_events = EventGenerator().generate_events(audio_path)

    print(f"🎵 Tempo: {audio_events['metadata']['tempo']:.1f} BPM")
    print(f"⏱️ Duración: {audio_events['metadata']['duration']:.1f}s")
    print(f"✨ Eventos detectados: {audio_events['metadata']['total_events']}")
    
    print(f"Eventos:")
    for event in audio_events['events'][:3]:
        print(f"{event['start_time']:.2f}s - {event['end_time']:.2f}s | "
              f"{event['type']} (Intensidad: {event['intensity']:.2f})")
        

    # 2. Procesar letras
    print("\n📝 Buscando letras...")
    events_with_lyrics = LyricsHandler().process(audio_path, audio_events['events'])
    # print(events_with_lyrics)
    
    # 3. Mostrar resultados
    print("\n🎤 Letras sincronizadas:")
    print(f"Canción: {Path(audio_path).stem}")
    print(f"Tempo: {audio_events['metadata']['tempo']:.1f} BPM")
    print(f"Duración: {audio_events['metadata']['duration']:.2f}s")
    print("\nFragmentos sincronizados:")
    # for event in events_with_lyrics[:20]:
    #     print(f"{event['start_time']:.2f}s: {event.get('lyric')}")
    for event in events_with_lyrics[:20]:
        print(f"{event['start_time']:.2f}s \t- {event['end_time']:.2f}s \t| "
              f"{event['type']}     \t(Intensidad: {event['intensity']:.2f})\t   letra: {event.get('lyric')}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python demo.py <ruta_al_audio.mp3>")
        sys.exit(1)
    
    audio_file = Path(sys.argv[1])
    if audio_file.exists():
        main(str(audio_file))
    else:
        print(f"Error: Archivo {audio_file} no encontrado")