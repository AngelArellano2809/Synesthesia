from ui.ui_home import *
import ui.newsongwindow
import ui.detailswindow
import ui.video_card
import json
import os
from pathlib import Path
from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QGridLayout, QMessageBox
from PySide6.QtCore import Qt


#from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot

#crear ventanas
class HomeWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        
        self.ui = Ui_HomeWindow()
        self.ui.setupUi(self)

        base_dir = Path(__file__).parent.parent
        self.video_dir = base_dir / "SynesthesiaVideos"

        # Conectar señales existentes
        self.ui.add_pushButton.clicked.connect(self.newSong)
        self.ui.playlist_pushButton.clicked.connect(self.open_random_video)

        # Cargar videos al iniciar
        self.load_local_videos()

    def load_local_videos(self):
        """Carga todos los videos locales en el QScrollArea"""        
        if not self.video_dir.exists():
            self.ui.search_lineEdit.setText("No hay videos descargados")
            return
        
        # Limpiar el scroll area actual
        self.clear_scroll_area()
        
        # Crear widget contenedor para el scroll
        scroll_content = QWidget()
        self.videos_layout = QGridLayout(scroll_content)
        self.videos_layout.setSpacing(15)
        
        # Buscar archivos de video
        video_files = list(self.video_dir.glob("*.mp4"))
        
        # Crear una card para cada video
        row, col = 0, 0
        max_cols = 2  # Máximo de columnas
        
        for video_file in video_files:
            # Cargar metadatos
            metadata_path = video_file.with_suffix('.syn')
            metadata = self.load_metadata(metadata_path)
            
            if metadata_path.exists():
                try:
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                except Exception as e:
                    print(f"Error cargando metadatos {metadata_path}: {e}")
            
            # Crear card de video
            card = ui.video_card.VideoCardWidget(str(video_file), metadata)
            card.details_clicked.connect(self.show_video_details)
            
            # Añadir al grid
            self.videos_layout.addWidget(card, row, col)
            
            # Actualizar posición
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Configurar el scroll area
        self.ui.scrollArea.setWidget(scroll_content)
        self.ui.scrollArea.setWidgetResizable(True)

    def open_random_video(self):
        """Abre un video aleatorio con el reproductor externo"""
        video_files = list(self.video_dir.glob("*.mp4"))
        
        if video_files:
            import random
            random_video = random.choice(video_files)
            self.open_video_external(str(random_video))
        else:
            self.ui.label_status.setText("No hay videos para reproducir")

    def open_video_external(self, video_path):
        """Función auxiliar para abrir video externamente"""
        try:
            if not os.path.exists(video_path):
                QMessageBox.warning(self, "Error", "El archivo de video no existe")
                return
            
            import platform
            import subprocess
            
            if platform.system() == "Windows":
                os.startfile(video_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", video_path])
            else:  # Linux
                subprocess.run(["xdg-open", video_path])
                
            print(f"Video abierto: {video_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir el video:\n{str(e)}")

    def show_video_details(self, video_path):
        """Abre DetailsWindow con los detalles del video"""
        self.details_window = ui.detailswindow.DetailsWindow(video_path)
        self.details_window.show()
        self.hide()

    def clear_scroll_area(self):
        """Limpia el contenido actual del scroll area"""
        if self.ui.scrollArea.widget():
            old_widget = self.ui.scrollArea.takeWidget()
            if old_widget:
                old_widget.deleteLater()

    def load_metadata(self, metadata_path):
        """Carga metadatos desde archivo .syn"""
        metadata = {}
        if metadata_path.exists():
            try:
                import json
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            except Exception as e:
                print(f"Error cargando metadatos {metadata_path}: {e}")
        return metadata

    @Slot( )
    def newSong(self):
        global new
        new = ui.newsongwindow.NewSongWindow()
        new.show()
        self.hide()

