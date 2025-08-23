from ui.ui_new_song import *
import ui.homewindow
from client_api import VideoProcessingThread

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
        self.selected_preset = None

        self.setup_presets()
        
        # Conexiones
        self.ui.back_pushButton.clicked.connect(self.home)
        self.ui.file_pushButton.clicked.connect(self.select_file)
        self.ui.add_pushButton.clicked.connect(self.process_song)
        self.ui.back_pushButton_2.clicked.connect(self.close)

    def setup_presets(self):
        """Configura los radio buttons de presets"""
        
        # Mapeo de nombres amigables a nombres técnicos
        self.preset_mapping = {
            "Minimal Geometric": "minimal_geometric",
            "Organic Abstract": "organic_abstract",
            "Digital Futuristic": "digital_futuristic",
            "Psychedelic Experience": "vibrant_abstract",
            "Cyberpunk Neon": "digital_minimalism",
            "Ethereal Dream": "liquid_motion"
        }
        
        # Configurar los radio buttons con nombres amigables
        self.ui.preset1_radioButton.setText("Minimal Geometric")
        self.ui.preset2_radioButton.setText("Organic Abstract")
        self.ui.preset3_radioButton.setText("Digital Futuristic")
        self.ui.preset4_radioButton.setText("Psychedelic Experience")
        self.ui.preset5_radioButton.setText("Cyberpunk Neon")
        self.ui.preset6_radioButton.setText("Ethereal Dream")
        
        # Conectar los radio buttons
        self.preset_buttons = {
            "minimal_geometric": self.ui.preset1_radioButton,
            "organic_abstract": self.ui.preset2_radioButton,
            "digital_futuristic": self.ui.preset3_radioButton,
            "vibrant_abstract": self.ui.preset4_radioButton,
            "digital_minimalism": self.ui.preset5_radioButton,
            "liquid_motion": self.ui.preset6_radioButton
        }
        
        for preset_name, button in self.preset_buttons.items():
            button.toggled.connect(self.on_preset_changed)

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

    def on_preset_changed(self, checked):
        """Maneja el cambio de selección de preset"""
        if checked:
            for preset_name, button in self.preset_buttons.items():
                if button.isChecked():
                    self.selected_preset = preset_name
                    break

    @Slot( )
    def process_song(self):
        if not self.mp3_path:
            QMessageBox.warning(self, "Error", "Selecciona un archivo primero")
            return

        # Obtener el preset seleccionado
        if not self.selected_preset:
            QMessageBox.warning(self, "Error", "Selecciona un preset primero")
            return
        
        preset = self.selected_preset
        
        # Obtener URL del servidor 
        server_url = "http://localhost:8000"  
        
        # Crear y configurar hilo
        self.processing_thread = VideoProcessingThread(
            server_url=server_url,
            mp3_path=self.mp3_path,
            preset=preset
        )
        
        # Conectar señales
        self.processing_thread.progress_updated.connect(self.update_progress)
        self.processing_thread.finished.connect(self.on_processing_finished)
        self.processing_thread.error_occurred.connect(self.on_processing_error)
        
        # Actualizar UI
        self.ui.progressBar.setRange(0, 100)
        self.ui.progressBar.setValue(0)
        self.ui.add_pushButton.setEnabled(False)
        self.ui.back_pushButton_2.setEnabled(True)
        self.ui.back_pushButton_2.clicked.connect(self.cancel_processing)
        
        # Iniciar procesamiento
        self.processing_thread.start()
    
    def update_progress(self, progress, status):
        self.ui.progressBar.setValue(progress)
        self.ui.label_status.setText(status)

    def on_processing_finished(self, video_path, success):
        if success:
            self.ui.progressBar.setValue(100)
            self.ui.label_status.setText("¡Video generado con éxito!")
            
            # Añadir a la lista de videos
            if self.parent():
                self.parent().add_new_video(video_path)
            
            QTimer.singleShot(2000, self.close)
        else:
            self.ui.label_status.setText("Error generando video")

    def on_processing_error(self, error_msg):
        QMessageBox.critical(self, "Error", error_msg)
        self.reset_ui()

    def cancel_processing(self):
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.stop()
            self.processing_thread.wait()
        self.reset_ui()

    def reset_ui(self):
        self.ui.progressBar.setValue(0)
        self.ui.label_status.setText("Listo")
        self.ui.add_pushButton.setEnabled(True)
        self.ui.back_pushButton_2.setEnabled(False)

    @Slot( )
    def home(self):
        global new
        new = ui.homewindow.HomeWindow()
        new.show()
        self.hide()