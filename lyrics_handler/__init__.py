from .hybrid_sync import HybridLyricsSyncer
from .api_lyrics import LyricsFetcher
from typing import List, Dict

class LyricsHandler:
    def __init__(self):
        self.fetcher = LyricsFetcher()
        self.syncer = HybridLyricsSyncer(model_size="base")  # "tiny", "base", "small"
    
    def process(self, audio_path: str, events: List[Dict]) -> List[Dict]:
        # 1. Obtener letras de referencia
        artist, title = self._get_metadata(audio_path)
        lyrics = self.fetcher.get_lyrics(artist, title)
        
        if not lyrics:
            return events  # No hacer nada si no hay letras
            
        # 2. Sincronizar con audio
        timed_lyrics = self.syncer.sync_lyrics(audio_path, lyrics)
        
        # 3. Asignar a eventos existentes
        return self._assign_to_events(events, timed_lyrics)
    
    def _assign_to_events(self, events, lyrics):
        lyric_idx = 0
        for event in events:
            while (lyric_idx < len(lyrics)-1 and 
                   lyrics[lyric_idx+1]['time'] <= event['start_time']):
                lyric_idx += 1
            event['lyric'] = lyrics[lyric_idx]['text']
        return events