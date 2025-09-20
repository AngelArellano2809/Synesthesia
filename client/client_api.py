import requests
from pathlib import Path
from PySide6.QtCore import QThread, Signal
import time

class VideoProcessingThread(QThread):
    progress_updated = Signal(int, str)  # progress, status
    finished = Signal(str, bool)  # video_path, success
    error_occurred = Signal(str)

    def __init__(self, server_url, mp3_path, preset, parent=None):
        super().__init__(parent)
        self.server_url = server_url
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
            
            if response.status_code != 202:
                self.error_occurred.emit(f"Error del servidor: {response.text}")
                return
            
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
                
                time.sleep(50)  # Esperar antes de la próxima verificación
            
            # Descargar video
            video_response = requests.get(f"{self.server_url}/video/{self.job_id}", stream=True)
            
            if video_response.status_code != 200:
                self.error_occurred.emit(f"Error descargando video: {video_response.status_code}")
                return
            
            # Guardar video localmente
            video_dir = Path.home() / "SynesthesiaVideos"
            video_dir.mkdir(exist_ok=True)
            video_path = video_dir / f"synesthesia_{self.job_id}.mp4"
            
            with open(video_path, 'wb') as f:
                for chunk in video_response.iter_content(chunk_size=8192):
                    if not self.running:
                        return  # Cancelar si se detuvo
                    f.write(chunk)
            
            self.finished.emit(str(video_path), True)
            
        except Exception as e:
            self.error_occurred.emit(f"Error inesperado: {str(e)}")

    def stop(self):
        self.running = False