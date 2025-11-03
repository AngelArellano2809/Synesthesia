from ui.ui_details import Ui_DetailsWindow
import ui.homewindow
from PySide6.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout, QLabel, QWidget
import json
from pathlib import Path
from PySide6.QtCore import Slot
import os
import platform
import subprocess
from mutagen.mp4 import MP4, MP4Cover
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import tempfile

class DetailsWindow(QMainWindow):
    def __init__(self, video_path):
        QMainWindow.__init__(self)
        
        self.ui = Ui_DetailsWindow()
        self.video_path = video_path
        self.metadata = self.load_metadata()
        self.temp_cover_path = None 
        
        self.ui.setupUi(self)
        
        # Llenar los con datos
        self.populate_details_frame()
        self.populate_versions_frame()

        # Cargar y mostrar la portada del video
        self.load_video_cover()

        # Conectar botones
        self.ui.back_pushButton.clicked.connect(self.home)
        self.ui.play_pushButton.clicked.connect(self.play_video_external)

    def load_metadata(self):
        """Carga los metadatos del archivo .syn"""
        metadata_path = Path(self.video_path).with_suffix('.syn')
        if metadata_path.exists():
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                return {}

    def populate_details_frame(self):
        """Llena el details_frame con información básica"""
        # Crear layout si no existe
        if not self.ui.details_frame.layout():
            layout = QVBoxLayout(self.ui.details_frame)
            layout.setSpacing(8)
        else:
            layout = self.ui.details_frame.layout()
            # Limpiar layout existente
            for i in reversed(range(layout.count())): 
                layout.itemAt(i).widget().setParent(None)
        
        # Campos de metadatos principales
        metadata_fields = [
            ("Título", self.metadata.get('title', 'Desconocido')),
            ("Artista", self.metadata.get('artist', 'Artista desconocido')),
            ("Álbum", self.metadata.get('album', 'Álbum desconocido')),
            ("Preset", self.metadata.get('preset', 'Desconocido')),
            ("Numero de Eventos", self.metadata.get('events_count', 'Desconocido')),
            ("Colores", self.metadata.get('color_palette', 'Desconocido')),
        ]
        
        for field_name, field_value in metadata_fields:
            field_widget = self.create_field_widget(field_name, field_value)
            layout.addWidget(field_widget)
        
        layout.addStretch()

    def populate_versions_frame(self):
        """Llena el versions_frame con información adicional"""
        # Crear layout si no existe
        if not self.ui.versions_frame.layout():
            layout = QVBoxLayout(self.ui.versions_frame)
            layout.setSpacing(8)
        else:
            layout = self.ui.versions_frame.layout()
            # Limpiar layout existente
            for i in reversed(range(layout.count())): 
                layout.itemAt(i).widget().setParent(None)
        
        # Información adicional
        duration = self.metadata.get('duration', 'N/A')
        created_at = self.metadata.get('created_at', 'N/A')
        file_size = self.get_file_size()
        
        additional_fields = [
            ("Duración", f"{duration} segundos" if duration != 'N/A' else 'N/A'),
            ("Fecha de creación", created_at),
            ("Tamaño del archivo", file_size),
            ("Nombre del archivo", os.path.basename(self.video_path)),
        ]
        
        for field_name, field_value in additional_fields:
            field_widget = self.create_field_widget(field_name, field_value)
            layout.addWidget(field_widget)
        
        layout.addStretch()

    def create_field_widget(self, field_name, field_value):
        """Crea un widget para mostrar un campo de metadatos"""
        container = QWidget()
        container.setStyleSheet("""
            background-color: rgba(255, 0, 0, 0);
            border-radius: 50px;
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        # Etiqueta del nombre del campo
        name_label = QLabel(field_name)
        name_label.setStyleSheet("""
            font-weight: bold; 
            color: black; 
            font-size: 16px;
            margin-bottom: 2px;
            padding-left: 30px;
        """)
        
        # Etiqueta del valor del campo
        value_label = QLabel(str(field_value))
        value_label.setStyleSheet("""
            color: white; 
            font-size: 18px;
            margin-top: 2px;
            padding-left: 30px;
        """)
        value_label.setWordWrap(True)
        
        container_layout.addWidget(name_label)
        container_layout.addWidget(value_label)
        
        return container

    def get_file_size(self):
        """Obtiene el tamaño del archivo de video en formato legible"""
        try:
            size_bytes = os.path.getsize(self.video_path)
            # Convertir a MB o KB
            if size_bytes >= 1024 * 1024:
                return f"{size_bytes / (1024 * 1024):.1f} MB"
            elif size_bytes >= 1024:
                return f"{size_bytes / 1024:.1f} KB"
            else:
                return f"{size_bytes} bytes"
        except:
            return "N/A"

    def play_video_external(self):
        """Abre el video con el reproductor predeterminado del sistema"""
        try:
            if not os.path.exists(self.video_path):
                QMessageBox.warning(self, "Error", "El archivo de video no existe")
                return
            
            if platform.system() == "Windows":
                os.startfile(self.video_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", self.video_path])
            else:  # Linux
                subprocess.run(["xdg-open", self.video_path])
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir el video:\n{str(e)}")

    @Slot( )
    def home(self):
        global new
        new = ui.homewindow.HomeWindow()
        new.show()
        self.hide()

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
        
    def load_video_cover(self):
        """Carga y muestra la portada del video MP4 en image_label"""
        try:
            # Intentar extraer portada del MP4 usando mutagen
            cover_path = self.extract_cover_from_mp4_enhanced(self.video_path)
            
            if cover_path and os.path.exists(cover_path):
                # Cargar la imagen
                pixmap = QPixmap(cover_path)
                if not pixmap.isNull():
                    # Escalar manteniendo relación de aspecto
                    scaled_pixmap = self.scale_pixmap_to_label(pixmap, self.ui.image_label)
                    self.ui.image_label.setPixmap(scaled_pixmap)
                    self.temp_cover_path = cover_path
                else:
                    # Imagen corrupta, limpiar
                    os.unlink(cover_path)
                    self.ui.image_label.setText('None')
            else:
                # Si no hay portada en MP4, intentar con ffmpeg como fallback
                self.extract_cover_with_ffmpeg_fallback()
                
        except Exception as e:
            print(f"Error cargando portada del MP4: {e}")
            self.extract_cover_with_ffmpeg_fallback()
    
    def extract_cover_with_ffmpeg_fallback(self):
        """Fallback usando ffmpeg si mutagen no funciona"""
        try:
            cover_path = self.extract_cover_from_mp4_enhanced(self.video_path)  # Tu función anterior con ffmpeg
            if cover_path and os.path.exists(cover_path):
                pixmap = QPixmap(cover_path)
                if not pixmap.isNull():
                    scaled_pixmap = self.scale_pixmap_to_label(pixmap, self.ui.image_label)
                    self.ui.image_label.setPixmap(scaled_pixmap)
                    self.temp_cover_path = cover_path
                else:
                    os.unlink(cover_path)
                    self.ui.image_label.setText('None')
            else:
                self.ui.image_label.setText('None')
        except Exception as e:
            print(f"Error en fallback ffmpeg: {e}")
            self.ui.image_label.setText('None')
    
    def scale_pixmap_to_label(self, pixmap, label):
        """Escala un QPixmap para que se ajuste a un QLabel manteniendo relación de aspecto"""
        return pixmap.scaled(
            label.width(),
            label.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
    
    def closeEvent(self, event):
        """Limpia los archivos temporales al cerrar la ventana"""
        if self.temp_cover_path and os.path.exists(self.temp_cover_path):
            try:
                os.unlink(self.temp_cover_path)
            except Exception as e:
                print(f"⚠ Error eliminando archivo temporal: {e}")
        event.accept()
