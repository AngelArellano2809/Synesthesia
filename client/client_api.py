import requests
import os
from pathlib import Path
from tqdm import tqdm
import hashlib

class SynesthesiaClient:
    def __init__(self, server_url="http://192.168.1.X:8000"):
        self.server_url = server_url
        self.local_storage = Path.home() / "SynesthesiaVideos"
        self.local_storage.mkdir(exist_ok=True)
    
    def create_video(self, mp3_path: str, preset: str) -> str:
        """Envía un MP3 al servidor y devuelve el job_id"""
        with open(mp3_path, "rb") as f:
            mp3_bytes = f.read()
        
        mp3_hash = hashlib.sha256(mp3_bytes).hexdigest()
        files = {"mp3": (os.path.basename(mp3_path), mp3_bytes)}
        
        response = requests.post(
            f"{self.server_url}/create_video",
            files=files,
            data={"preset": preset}
        )
        
        return response.json()["job_id"]
    
    def download_video(self, job_id: str, metadata: dict = None):
        """Descarga el video completado y guarda metadatos"""
        video_path = self.local_storage / f"{job_id}.mp4"
        metadata_path = self.local_storage / f"{job_id}.syn"
        
        # Descargar video
        response = requests.get(f"{self.server_url}/video/{job_id}", stream=True)
        total_size = int(response.headers.get("content-length", 0))
        
        with open(video_path, "wb") as f, tqdm(
            desc=video_path.name,
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                bar.update(size)
        
        # Guardar metadatos
        if metadata:
            import json
            with open(metadata_path, "w") as f:
                json.dump(metadata, f)
        
        return video_path