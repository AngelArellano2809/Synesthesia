from .api_lyrics import LyricsFetcher
from mutagen.id3 import ID3
from mutagen.mp3 import MP3

class LyricsHandler:
    def __init__(self):
        self.fetcher = LyricsFetcher()
    
    def process(self, audio_path: str, events: list) -> list:
        artist, title = self._get_metadata(audio_path)
        print(f'{artist}  /  {title}')
        result = self.fetcher.search_lyrics(artist, title)
        print(result['syncedLyrics'])

        return result['syncedLyrics']
        # return self._assign_to_events(events, result['syncedLyrics'])
    
    def _get_metadata(self, audio_path: str) -> tuple:
        try:
            audio = MP3(audio_path, ID3=ID3)
            artist = audio.tags.get('TPE1', ['Unknown'])[0]
            title = audio.tags.get('TIT2', ['Unknown'])[0]
            return artist, title
        except:
            return "Unknown", "Unknown"

    
    def _assign_to_events(self, events: list, lyrics: list) -> list:
    
        lyric_ptr = 0
        for event in events:
            while (lyric_ptr < len(lyrics)-1 and 
                   lyrics[lyric_ptr+1]['time'] <= event['start_time']):
                lyric_ptr += 1
            event['lyric'] = lyrics[lyric_ptr]['text']
        return events