import os
import platform
import subprocess
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap

class VideoCardWidget(QWidget):
    details_clicked = Signal(str)  # Solo mantenemos la señal de detalles
    
    def __init__(self, video_path, metadata, parent=None):
        super().__init__(parent)
        self.video_path = video_path
        self.metadata = metadata
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        # Miniatura
        self.thumbnail = QLabel()
        self.thumbnail.setFixedSize(200, 150)
        self.thumbnail.setStyleSheet("""
            background-color: #2d2d2d; 
            border-radius: 8px; 
            color: #888;
        """)
        self.thumbnail.setText("Video")
        self.thumbnail.setAlignment(Qt.AlignCenter)
        
        # Información del video
        title = self.metadata.get('title', os.path.basename(self.video_path))
        artist = self.metadata.get('artist', 'Artista desconocido')
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: bold; color: white;")
        self.title_label.setWordWrap(True)
        
        self.artist_label = QLabel(artist)
        self.artist_label.setStyleSheet("color: #aaa;")
        
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