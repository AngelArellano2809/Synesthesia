from ui.ui_new_song import *
import ui.homewindow

import os
import requests
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QFileDialog, QMessageBox
from mutagen import File
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from pathlib import Path

#from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot

#crear ventanas
class NewSongWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_NewSongWindow()
        self.ui.setupUi(self)


        # Variables
        self.mp3_path = ""
        self.server_url = "http://localhost:8000"
        self.job_id = ""
        self.timer = QTimer()
        
        # Conexiones
        self.ui.back_pushButton.clicked.connect(self.home)
        self.ui.file_pushButton.clicked.connect(self.select_file)
        self.ui.add_pushButton.clicked.connect(self.process_song)
        self.timer.timeout.connect(self.check_progress)
        self.ui.btn_cancel.clicked.connect(self.close)

    @Slot( )
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar MP3", "", "MP3 Files (*.mp3)"
        )
        
        if file_path:
            self.mp3_path = file_path
            self.display_metadata(file_path)
    
    def display_metadata(self, file_path):
        try:
            # Leer metadatos básicos
            audio = MP3(file_path, ID3=ID3)
            artist = audio.tags.get('TPE1', ['Unknown'])[0]
            title = audio.tags.get('TIT2', ['Unknown'])[0]
            album = audio.tags.get('TALB', ['Unknown'])[0]
            self.ui.label_title.setText(title)
            self.ui.label_artist.setText(artist)
            self.ui.label_album.setText(album)
            
            # Extraer portada
            if 'APIC:' in audio.tags:
                apic = audio.tags['APIC:'].data
                pixmap = QPixmap()
                pixmap.loadFromData(apic)
                self.ui.image_label.setPixmap(pixmap.scaled(200, 200))
            else:
                self.ui.image_label.clear()
                self.ui.image_label.setText("No hay portada")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron leer metadatos: {str(e)}")

    @Slot( )
    def process_song(self):
        if not self.mp3_path:
            QMessageBox.warning(self, "Error", "Selecciona un archivo primero")
            return
        
        preset = self.ui.preset_combo.currentText()
        
        try:
            # Configurar UI para procesamiento
            self.ui.progress_bar.setRange(0, 0)  # Barra indeterminada
            self.ui.label_status.setText("Enviando al servidor...")
            
            # Enviar al servidor
            with open(self.mp3_path, "rb") as f:
                response = requests.post(
                    f"{self.server_url}/create_video",
                    files={"mp3": f},
                    data={"preset": preset}
                )
            
            if response.status_code != 200:
                raise Exception(f"Error del servidor: {response.text}")
            
            response_data = response.json()
            self.job_id = response_data["job_id"]
            
            # Iniciar monitoreo
            self.ui.label_status.setText("Procesando en servidor...")
            self.timer.start(3000)  # Verificar cada 3 segundos
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fallo al procesar: {str(e)}")
            self.reset_ui()
    
    def check_progress(self):
        try:
            response = requests.get(f"{self.server_url}/video/{self.job_id}")
            
            if response.status_code == 200:
                # Video está listo
                if response.headers['Content-Type'] == 'video/mp4':
                    self.download_video(response.content)
                    return
                
                # Todavía procesando
                status_data = response.json()
                if status_data.get("status") == "completed":
                    self.download_video_by_id()
            
            elif response.status_code == 202:
                # Todavía procesando
                progress = response.json().get("progress", 0)
                self.ui.progress_bar.setValue(progress)
                self.ui.label_status.setText(f"Procesando... {progress}%")
            
            else:
                raise Exception(f"Estado inesperado: {response.status_code}")
        
        except Exception as e:
            self.timer.stop()
            QMessageBox.critical(self, "Error", f"Fallo al verificar progreso: {str(e)}")
            self.reset_ui()
    
    def download_video_by_id(self):
        try:
            response = requests.get(f"{self.server_url}/video/{self.job_id}")
            if response.status_code == 200:
                self.download_video(response.content)
            else:
                raise Exception(f"Error descargando video: {response.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.reset_ui()
    
    def download_video(self, video_data):
        try:
            # Crear directorio si no existe
            video_dir = Path.home() / "SynesthesiaVideos"
            video_dir.mkdir(exist_ok=True)
            
            # Guardar video
            video_path = video_dir / f"{self.job_id}.mp4"
            with open(video_path, "wb") as f:
                f.write(video_data)
            
            # Guardar metadatos
            metadata = {
                "title": self.ui.label_title.text(),
                "artist": self.ui.label_artist.text(),
                "album": self.ui.label_album.text(),
                "preset": self.ui.preset_combo.currentText(),
                "server_job_id": self.job_id,
                "source_file": self.mp3_path
            }
            
            metadata_path = video_dir / f"{self.job_id}.syn"
            with open(metadata_path, "w") as f:
                import json
                json.dump(metadata, f)
            
            # Notificar éxito
            self.ui.label_status.setText("¡Video generado con éxito!")
            self.ui.progress_bar.setRange(0, 100)
            self.ui.progress_bar.setValue(100)
            
            # Notificar a HomeWindow
            if self.parent():
                self.parent().add_new_video(video_path, metadata)
            
            QTimer.singleShot(2000, self.close)
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fallo al guardar: {str(e)}")
            self.reset_ui()
    
    def reset_ui(self):
        self.timer.stop()
        self.ui.progress_bar.setRange(0, 100)
        self.ui.progress_bar.setValue(0)
        self.ui.label_status.setText("Listo")

    @Slot( )
    def home(self):
        global new
        new = ui.homewindow.HomeWindow()
        new.show()
        self.hide()