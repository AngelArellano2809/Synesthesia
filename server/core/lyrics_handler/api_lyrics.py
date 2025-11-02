#LRCGET v0.2.0 (https://github.com/tranxuanthang/lrcget)
import requests

class LyricsFetcher:
    
    def search_lyrics(self, artist, title):
        url = f"https://lrclib.net/api/search?track_name={title}&artist_name={artist}"
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json()
            if results:
                return results[0]  # primera coincidencia
        return None