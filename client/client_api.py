import requests
from pathlib import Path
from PySide6.QtCore import QThread, Signal
import time
from config import ClientConfig
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
import json
import os

class VideoProcessingThread(QThread):
    progress_updated = Signal(int, str)  # progress, status
    finished = Signal(str, bool)  # video_path, success
    error_occurred = Signal(str)

    def __init__(self, mp3_path, preset, parent=None, server_url=None,):
        super().__init__(parent)
        self.server_url = server_url or ClientConfig.SERVER_URL
        self.mp3_path = mp3_path
        self.preset = preset
        self.job_id = None
        self.running = True

    def run(self):
        try:            
            # Subir MP3 y crear trabajo
            with open(self.mp3_path, 'rb') as f:
                files = {'mp3': f}
                data = {'preset': self.preset}
                
                response = requests.post(
                    f"{self.server_url}/create_video",
                    files=files,
                    data=data
                )
            if response.status_code == 200:
                # El video ya existe, podemos descargarlo inmediatamente
                response_data = response.json()
                self.job_id = response_data['job_id']
                
                print(f" Video ya existe en el servidor, job_id: {self.job_id}")
                self.progress_updated.emit(100, "Video ya procesado anteriormente")
                
                # Descargar directamente
                video_path = self.download_video_and_metadata()
                self.finished.emit(video_path, True)
                return
            
            elif response.status_code == 202:
                # Nuevo MP3            
                response_data = response.json()
                self.job_id = response_data['job_id']
                self.progress_updated.emit(0, "En cola")
                
                # Monitorear progreso
                while self.running:
                    status_response = requests.get(f"{self.server_url}/status/{self.job_id}")
                    
                    if status_response.status_code != 200:
                        self.error_occurred.emit(f"Error obteniendo estado: {status_response.text}")
                        return
                    
                    status_data = status_response.json()
                    status = status_data['status']
                    progress = status_data['progress']
                    
                    self.progress_updated.emit(progress, status)
                    
                    if status == "completed":
                        break
                    elif "failed" in status:
                        self.error_occurred.emit(f"Error en el servidor: {status}")
                        return
                    
                    time.sleep(50) 

                # Descargar video y metadatos
                video_path = self.download_video_and_metadata()
                self.finished.emit(video_path, True)

            else:
                # Error
                self.error_occurred.emit(f"Error del servidor: {response.text}")
                return  
            
        except Exception as e:
            self.error_occurred.emit(f"Error inesperado: {str(e)}")

    def download_video_and_metadata(self):
        """Descarga el video y metadatos para el job_id actual"""
        #Obtener Metadatos
        audio = MP3(self.mp3_path, ID3=ID3)
        title = audio.tags.get('TIT2', ['Unknown'])[0]

        video_dir = Path("client/SynesthesiaVideos")
        video_dir.mkdir(parents=True, exist_ok=True)
        video_path = video_dir / f"{title}_Synesthesia.mp4"
        metadata_path = video_dir / f"{title}_Synesthesia.syn"
        
        # Descargar video
        self.progress_updated.emit(0, "Iniciando descarga de video...")
        video_response = requests.get(f"{self.server_url}/video/{self.job_id}", stream=True)
        
        if video_response.status_code != 200:
            self.error_occurred.emit(f"Error descargando video: {video_response.status_code}")
            return
        
        total_size = int(video_response.headers.get("content-length", 0))
        downloaded_size = 0
        
        with open(video_path, 'wb') as f:
            for chunk in video_response.iter_content(chunk_size=8192):
                if not self.running:
                    return  # Cancelar si se detuvo
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    # Opcional: emitir progreso de descarga 
                    if total_size > 0:
                        download_progress = int((downloaded_size / total_size) * 100)
                        self.progress_updated.emit(download_progress, "Descargando video...")
        
        # Descargar metadatos
        self.progress_updated.emit(90, "Descargando metadatos...")
        metadata_response = requests.get(f"{self.server_url}/metadata/{self.job_id}")

        if metadata_response.status_code != 200:
            self.error_occurred.emit(f"Error descargando video: {metadata_response.status_code}")
            return
        
        with open(metadata_path, 'wb') as f:
            f.write(metadata_response.content)
        
        self.progress_updated.emit(100, "Video Descargado!")
        return str(video_path)

    def stop(self):
        self.running = False