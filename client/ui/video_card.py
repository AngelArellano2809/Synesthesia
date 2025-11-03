import os
import platform
import subprocess
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from mutagen.mp4 import MP4, MP4Cover
import tempfile

class VideoCardWidget(QWidget):
    details_clicked = Signal(str)  # Solo mantenemos la señal de detalles
    
    def __init__(self, video_path, metadata, parent=None):
        super().__init__(parent)
        self.video_path = video_path
        self.metadata = metadata
        self.temp_cover_path = None 
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        # Miniatura
        self.thumbnail = QLabel()
        self.thumbnail.setFixedSize(200, 200)
        self.thumbnail.setStyleSheet("""
            background-color: #2d2d2d; 
            border-radius: 8px; 
            color: #888;
        """)
        self.thumbnail.setText("Imagen")
        self.thumbnail.setAlignment(Qt.AlignCenter)

        cover_path = self.extract_cover_from_mp4_enhanced(self.video_path)
        if cover_path and os.path.exists(cover_path):
                # Cargar la imagen
                pixmap = QPixmap(cover_path)
                if not pixmap.isNull():
                    # Escalar manteniendo relación de aspecto
                    scaled_pixmap = self.scale_pixmap_to_label(pixmap, self.thumbnail)
                    self.thumbnail.setPixmap(scaled_pixmap)
                    self.temp_cover_path = cover_path
                else:
                    # Imagen corrupta, limpiar
                    os.unlink(cover_path)
                    self.thumbnail.setText('None')
        
        # Información del video
        title = self.metadata.get('title', os.path.basename(self.video_path))
        artist = self.metadata.get('artist', 'Artista desconocido')
        album = self.metadata.get('album', 'Album desconocido')
        created_at = self.metadata.get('created_at', 'Fecha desconocida')
        preset = self.metadata.get('preset', 'Preset desconocido')
        
        self.title_label = QLabel()
        self.title_label.setText(f'\n{title}\n\n{artist}\n\n{album}\n')
        self.title_label.setStyleSheet("font-weight: bold; color: white; padding-left: 25px;")
        self.title_label.setWordWrap(True)
        
        self.artist_label = QLabel()
        self.artist_label.setText(f'\n{created_at}\n\n{preset}\n')
        self.artist_label.setStyleSheet("color: #c5c5c5; padding-left: 25px;")
        
        # Botones
        btn_layout = QHBoxLayout()
        
        # Botón de reproducción - ahora abre directamente el reproductor
        self.play_btn = QPushButton("▶ Reproducir")
        self.play_btn.setFixedSize(90, 30)
        self.play_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # Botón de detalles
        self.details_btn = QPushButton("ℹ Detalles")
        self.details_btn.setFixedSize(90, 30)
        self.details_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        btn_layout.addWidget(self.play_btn)
        btn_layout.addWidget(self.details_btn)
        btn_layout.addStretch()
        
        # Ensamblar layout
        layout.addWidget(self.thumbnail)
        layout.addWidget(self.title_label)
        layout.addWidget(self.artist_label)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # Conectar señales
        self.play_btn.clicked.connect(self.open_video_external)
        self.details_btn.clicked.connect(self.emit_details_signal)

    def open_video_external(self):
        """Abre el video con el reproductor predeterminado del sistema"""
        try:
            if not os.path.exists(self.video_path):
                QMessageBox.warning(self, "Error", f"El archivo no existe:\n{self.video_path}")
                return
            
            if platform.system() == "Windows":
                os.startfile(self.video_path)
            else:  # Linux
                subprocess.run(["xdg-open", self.video_path])
                
            print(f"Video abierto: {self.video_path}")
            
        except Exception as e:
            error_msg = f"No se pudo abrir el video:\n{str(e)}"
            print(error_msg)
            QMessageBox.critical(self, "Error", error_msg)

    def emit_details_signal(self):
        """Emite la señal para abrir los detalles"""
        self.details_clicked.emit(self.video_path)

    def extract_cover_from_mp4_enhanced(self, video_path):
        """
        Versión mejorada que maneja diferentes formatos de imagen en MP4
        """
        try:
            video = MP4(video_path)
            
            if 'covr' not in video.tags:
                return None
            
            cover_data = video.tags['covr'][0]
            
            # Determinar la extensión basada en el tipo de datos
            if hasattr(cover_data, 'imageformat'):
                if cover_data.imageformat == MP4Cover.FORMAT_JPEG:
                    extension = '.jpg'
                elif cover_data.imageformat == MP4Cover.FORMAT_PNG:
                    extension = '.png'
                else:
                    extension = '.jpg'  # Por defecto
            else:
                # Intentar detectar el formato por los bytes mágicos
                if cover_data.startswith(b'\xff\xd8\xff'):
                    extension = '.jpg'
                elif cover_data.startswith(b'\x89PNG\r\n\x1a\n'):
                    extension = '.png'
                else:
                    extension = '.jpg'  # Por defecto
            
            # Crear archivo temporal con la extensión correcta
            temp_cover = tempfile.NamedTemporaryFile(delete=False, suffix=extension)
            temp_cover.write(cover_data)
            temp_cover.close()
            return temp_cover.name
            
        except Exception as e:
            print(f" Error extrayendo portada del MP4: {e}")
            return None
        
    def scale_pixmap_to_label(self, pixmap, label):
        """Escala un QPixmap para que se ajuste a un QLabel manteniendo relación de aspecto"""
        return pixmap.scaled(
            label.width(),
            label.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        