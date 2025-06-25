from .api_lyrics import LyricsFetcher
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from typing import List, Dict

class LyricsHandler:
    def __init__(self):
        self.fetcher = LyricsFetcher()
    
    def process(self, audio_path: str, events: list) -> list:
        artist, title = self._get_metadata(audio_path)
        result = self.fetcher.search_lyrics(artist, title)
        if result is None:
            return events
        lyrics = self._parse_lrc_to_events(result['syncedLyrics'])
        new_events = self._assign_lyrics_to_events(events, lyrics, 0.5)
        return new_events
    
    def _get_metadata(self, audio_path: str) -> tuple:
        try:
            audio = MP3(audio_path, ID3=ID3)
            artist = audio.tags.get('TPE1', ['Unknown'])[0]
            title = audio.tags.get('TIT2', ['Unknown'])[0]
            return artist, title
        except:
            return "Unknown", "Unknown"
        
    def _parse_lrc_to_events(self, lrc_text: str) -> List[tuple[float, str]]:
        """Convierte texto LRC en lista de eventos de tiempo y texto"""
        events = []
        for line in lrc_text.split('\n'):
            if not line.startswith('[') or ']' not in line:
                continue
                
            try:
                # Dividir tiempo y texto
                time_part, text = line.split(']', 1)
                time_str = time_part[1:]  # Remover el corchete inicial
                
                # Convertir tiempo a segundos
                if ':' in time_str:
                    parts = time_str.split(':')
                    minutes = float(parts[0])
                    seconds = float(parts[1])
                    total_seconds = minutes * 60 + seconds
                    events.append((total_seconds, text.strip()))
            except Exception as e:
                print(f"Error parseando línea LRC: {line} | Error: {e}")
        
        return events

    def _assign_lyrics_to_events(self, audio_events: List[Dict], 
                           lyric_events: List[tuple[float, str]], 
                           max_gap: float = 0.5) -> List[Dict]:
        """
        Asigna letras a eventos de audio, creando nuevos eventos si es necesario
        """
        # 1. Crear lista combinada de todos los eventos
        all_events = []
        
        # 2. Primero añadimos los eventos de audio existentes
        for event in audio_events:
            all_events.append({
                'time': event['start_time'],
                'source': 'audio',
                'data': event
            })
        
        # 3. Añadir eventos de letra como puntos de referencia
        for time, text in lyric_events:
            all_events.append({
                'time': time,
                'source': 'lyric_marker',
                'text': text
            })
        
        # 4. Ordenar todos los eventos por tiempo
        all_events.sort(key=lambda x: x['time'])
        
        # 5. Fusionar eventos cercanos y asignar letras
        merged_events = []
        current_lyric = ""
        
        for i, event in enumerate(all_events):
            # Si es un marcador de letra, actualizamos la letra actual
            if event['source'] == 'lyric_marker':
                current_lyric = event['text']
                continue
                
            # Para eventos de audio, verificar si debemos fusionar con evento anterior
            if merged_events:
                prev_event = merged_events[-1]
                time_diff = event['time'] - prev_event['time']
                
                # Fusionar con evento anterior si están muy cerca
                if time_diff < max_gap:
                    prev_event['data']['end_time'] = event['data']['end_time']
                    prev_event['data']['duration'] = event['data']['end_time'] - prev_event['time']
                    # Mantener la letra más reciente
                    prev_event['data']['lyric'] = current_lyric
                    continue
            
            # Crear nuevo evento fusionado
            audio_data = event['data'].copy()
            audio_data['lyric'] = current_lyric
            merged_events.append({
                'time': event['time'],
                'data': audio_data
            })
        
        # 6. Crear nuevos eventos para letras sin evento cercano
        final_events = [e['data'] for e in merged_events]
        used_lyric_times = set()
        
        # Marcar tiempos de letra ya usados
        for event in final_events:
            if 'lyric_time' in event:
                used_lyric_times.add(event['lyric_time'])

        # Obtener todos los tiempos de inicio ordenados
        all_start_times = sorted([e['start_time'] for e in final_events])
        
        # Añadir nuevos eventos para letras no asignadas
        for time, text in lyric_events:
            if time in used_lyric_times:
                continue
                
            # Encontrar el próximo evento temporal
            next_event_time = next((t for t in all_start_times if t > time), None)
            
            # Calcular end_time basado en el próximo evento o usar duración mínima
            if next_event_time is not None:
                end_time = next_event_time
            else:
                # Si es el último evento, usar duración basada en el texto
                avg_duration = max(3.0, len(text.split()) * 0.5)  # 0.5s por palabra
                end_time = time + avg_duration
            
            # Crear nuevo evento de tipo 'lyric'
            new_event = {
                'start_time': time,
                'end_time': end_time,
                'duration': end_time - time,
                'type': 'lyric',
                'intensity': 0.5,  # Intensidad estándar
                'lyric': text
            }
            
            # Buscar posición para insertar
            insert_index = next((i for i, e in enumerate(final_events) 
                            if e['start_time'] > time), len(final_events))
            final_events.insert(insert_index, new_event)
            
            # Actualizar lista de tiempos para futuras inserciones
            all_start_times.insert(insert_index, time)
        
        return final_events