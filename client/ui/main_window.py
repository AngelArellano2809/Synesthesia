from PySide6.QtWidgets import QFileDialog, QMessageBox
from ..client_api import SynesthesiaClient
import os

class MainWindowExtension:
    def __init__(self, window):
        self.window = window
        self.client = SynesthesiaClient()
        
        # Conectar botones existentes
        self.window.btn_process_remote.clicked.connect(self.process_remote)
        self.window.btn_refresh.clicked.connect(self.load_local_playlist)
    
    def process_remote(self):
        mp3_path, _ = QFileDialog.getOpenFileName(
            self.window, "Seleccionar MP3", "", "Audio Files (*.mp3)"
        )
        
        if not mp3_path:
            return
        
        preset = self.window.preset_combo.currentText()
        
        try:
            job_id = self.client.create_video(mp3_path, preset)
            self.monitor_job(job_id, os.path.basename(mp3_path), preset)
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"Error al procesar: {str(e)}")
    
    def monitor_job(self, job_id, filename, preset):
        # Implementar monitoreo con QTimer y actualizar UI
        # Usar client.download_video cuando esté completo
        pass
    
    def load_local_playlist(self):
        # Cargar videos locales con sus metadatos
        for video in self.local_storage.glob("*.mp4"):
            metadata_path = video.with_suffix(".syn")
            if metadata_path.exists():
                # Leer y mostrar metadatos
                pass
            else:
                # Mostrar información básica del archivo
                pass