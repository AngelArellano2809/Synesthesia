
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




from audio_processor.event_generation import EventGenerator

def process_song(file_path: str):
    generator = EventGenerator()
    analysis = generator.generate_events(file_path)
    
    print(f"🎵 Tempo: {analysis['metadata']['tempo']:.1f} BPM")
    print(f"⏱️ Duración: {analysis['metadata']['duration']:.1f}s")
    print(f"✨ Eventos detectados: {analysis['metadata']['total_events']}")
    
    print("\nPrimeros 5 eventos:")
    for event in analysis['events'][:5]:
        print(f"{event['start_time']:.2f}s - {event['end_time']:.2f}s | "
              f"{event['type']} (Intensidad: {event['intensity']:.2f})")

if __name__ == "__main__":
    import sys
    process_song(sys.argv[1])