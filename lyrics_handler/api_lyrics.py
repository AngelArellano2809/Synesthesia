import requests
from typing import Optional
import re
from config import Config

class LyricsFetcher:
    def __init__(self):
        self.headers = {
            'Authorization': f"Bearer {Config.GENIUS['ACCESS_TOKEN']}",
            'User-Agent': 'Synesthesia-App/1.0'
        }
    
    def get_lyrics(self, artist: str, title: str) -> Optional[str]:
        """Obtiene letras usando solo la API oficial de Genius"""
        try:
            # 1. Buscar ID de la canción
            search_url = "https://api.genius.com/search"
            params = {'q': f"{artist} {title}"}
            search_res = requests.get(
                search_url,
                headers=self.headers,
                params=params,
                timeout=Config.GENIUS['TIMEOUT']
            ).json()
            
            # 2. Extraer letras directamente del campo 'lyrics_state'
            song_data = search_res['response']['hits'][0]['result']
            if song_data.get('lyrics_state') == 'complete':
                lyrics_api_url = f"https://api.genius.com/songs/{song_data['id']}/lyrics"
                lyrics_res = requests.get(
                    lyrics_api_url,
                    headers=self.headers,
                    timeout=Config.GENIUS['TIMEOUT']
                ).json()
                
                return self._clean_lyrics(lyrics_res['response']['lyrics']['plain'])
            
            return None
            
        except Exception as e:
            print(f"Error Genius API: {str(e)}")
            return None
    
    def _clean_lyrics(self, lyrics: str) -> str:
        """Limpia formato básico manteniendo estructura"""
        lyrics = re.sub(r'\n{3,}', '\n\n', lyrics)  # Compacta múltiples saltos
        lyrics = re.sub(r'\[.*\]', '', lyrics)  # Elimina anotaciones entre corchetes
        return lyrics.strip()