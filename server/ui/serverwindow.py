import os
import sys
import logging
import sqlite3
import subprocess
from PySide6.QtWidgets import QMainWindow, QMessageBox, QHeaderView
from PySide6.QtCore import Qt, QTimer, QProcess
from PySide6.QtGui import QColor, QBrush
from pathlib import Path

from ui.ui_server_window import *

#crear ventana
class ServerWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_ServerWindow()
        self.ui.setupUi(self)

        # Obtener el directorio base del proyecto (carpeta server)
        self.base_dir = Path(__file__).parent.parent
        
        # Configuración de rutas absolutas
        self.db_path = self.base_dir / "database" / "synesthesia.db"

        # Configuración inicial
        self.api_process = None
        self.is_running = False

        # Configurar UI
        self.setup_ui()
        
        # Conectar señales
        self.ui.start_pushButton.clicked.connect(self.start_api_server)
        self.ui.back_pushButton.clicked.connect(self.stop_api_server)
        
        # Configurar temporizador para actualizar datos
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.refresh_data)

        # Estado inicial
        self.update_ui_state()
        
        # Configurar logging
        self.setup_logging()

    def setup_ui(self):
        """Configura elementos iniciales de la UI"""
        # Configurar tablas
        self.ui.data_base_tableWidget.setColumnCount(6)
        self.ui.data_base_tableWidget.setHorizontalHeaderLabels(["ID", "MP3 Hash", "Preset", "Estado", "Progreso", "Fecha"])
        self.ui.data_base_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.ui.active_works_tableWidget.setColumnCount(4)
        self.ui.active_works_tableWidget.setHorizontalHeaderLabels(["ID", "MP3", "Preset", "Estado"])
        self.ui.active_works_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)       

    def setup_logging(self):
        """Configura el sistema de logging para capturar mensajes"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[self.LogHandler(self)]
        ) 

    class LogHandler(logging.Handler):
        """Manejador de logs personalizado para enviar mensajes a la UI"""
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            
        def emit(self, record):
            msg = self.format(record)
            # Filtrar mensajes de status checks
            if "GET /status/" in msg and "200 OK" in msg:
                return 
            self.parent.ui.server_logs_textEdit.append(msg)
            self.parent.ui.server_logs_textEdit.verticalScrollBar().setValue(
                self.parent.ui.server_logs_textEdit.verticalScrollBar().maximum()
            )

    def start_api_server(self):
        """Inicia el servidor API en un proceso separado"""
        if self.is_running:
            return
        
        try:
            # Obtener el directorio del servidor
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Crear proceso
            self.api_process = QProcess()
            
            # Establecer el directorio de trabajo
            self.api_process.setWorkingDirectory(project_root)

            # Configurar variables de entorno
            env = self.api_process.processEnvironment()
            env.insert("PYTHONPATH", project_root)
            self.api_process.setProcessEnvironment(env)
            
            # Configurar el proceso para usar uvicorn directamente
            self.api_process.setProgram(sys.executable)
            self.api_process.setArguments([
                "-m", "uvicorn", 
                "server_api:app", 
                "--host", "0.0.0.0", 
                "--port", "8000",
                "--reload"
            ])
            
            # Conectar señales para capturar salida
            self.api_process.readyReadStandardOutput.connect(self.handle_stdout)
            self.api_process.readyReadStandardError.connect(self.handle_stderr)
            self.api_process.finished.connect(self.api_finished)
            
            # Iniciar
            self.api_process.start()
            
            self.is_running = True
            self.update_ui_state()
            self.update_timer.start(3000)
            
            logging.info("Servidor API iniciado")
            logging.info(f"Endpoint: POST http://localhost:8000/create_video")
            
        except Exception as e:
            logging.error(f"No se pudo iniciar el servidor API: {str(e)}")
            QMessageBox.critical(self, "Error", f"No se pudo iniciar el servidor API:\n{str(e)}")
    
    def stop_api_server(self):
        """Detiene el servidor API de manera forzosa"""
        if self.api_process and self.api_process.state() == QProcess.Running:
            subprocess.run(["taskkill", "/f", "/pid", str(self.api_process.processId())])
            self.api_process.waitForFinished(100)
        
        self.is_running = False
        self.update_ui_state()
        self.update_timer.stop()
        
        logging.info("Servidor API detenido forzosamente")
    
    def handle_stdout(self):
        """Maneja la salida estándar del proceso del servidor API"""
        data = self.api_process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8").strip()
        if stdout:
            logging.info(f"API: {stdout}")
    
    def handle_stderr(self):
        """Maneja la salida de error del proceso del servidor API"""
        if self.api_process:
            data = self.api_process.readAllStandardError()
            stderr = bytes(data).decode("utf8").strip()
            if stderr:
                # Filtrar mensajes de INFO de uvicorn
                if "INFO:" in stderr:
                    # Extraer solo el mensaje informativo
                    info_msg = stderr.split("INFO:")[-1].strip()
                    logging.info(f"API: {info_msg}")
                else:
                    logging.error(f"API ERROR: {stderr}")
                    self.ui.server_logs_textEdit.append(f'<span style="color: red;">ERROR: {stderr}</span>')
    
    def api_finished(self, exit_code, exit_status):
        """Maneja la finalización del proceso del servidor API"""
        self.is_running = False
        self.update_ui_state()
        self.update_timer.stop()
        logging.info(f"Servidor API terminado con código {exit_code}")
    
    def refresh_data(self):
        """Actualiza los datos mostrados en la UI"""
        if not self.is_running:
            return
        
        try:
            # Actualizar vista de base de datos
            self.update_database_view()
            
            # Actualizar trabajos activos
            self.update_active_jobs()
            
        except Exception as e:
            logging.error(f"Error actualizando datos: {str(e)}")
    
    def update_database_view(self):
        """Actualiza la vista de la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, mp3_hash, preset, status, progress, created_at FROM jobs ORDER BY created_at DESC LIMIT 50")
            jobs = cursor.fetchall()
            conn.close()
            
            self.ui.data_base_tableWidget.setRowCount(len(jobs))
            
            for row, job in enumerate(jobs):
                for col, value in enumerate(job):
                    item = QTableWidgetItem(str(value))
                    
                    # Colorear por estado
                    if col == 3:  # Columna de estado
                        if value == "completed":
                            item.setForeground(QBrush(QColor(0, 150, 0)))  # Verde
                        elif value == "failed":
                            item.setForeground(QBrush(QColor(200, 0, 0)))  # Rojo
                        elif value == "processing":
                            item.setForeground(QBrush(QColor(0, 100, 0)))  # Verde claro
                    
                    self.ui.data_base_tableWidget.setItem(row, col, item)
                    
        except sqlite3.Error as e:
            logging.error(f"Error de base de datos: {str(e)}")
    
    def update_active_jobs(self):
        """Actualiza la tabla de trabajos activos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, mp3_hash, preset, status FROM jobs WHERE status IN ('queued', 'processing')")
            active_jobs = cursor.fetchall()
            conn.close()
            
            self.ui.active_works_tableWidget.setRowCount(len(active_jobs))
            
            for row, job in enumerate(active_jobs):
                job_id, mp3_hash, preset, status = job
                
                # Acortar hash para visualización
                short_hash = mp3_hash[:8] + "..." if len(mp3_hash) > 10 else mp3_hash
                
                self.ui.active_works_tableWidget.setItem(row, 0, QTableWidgetItem(job_id))
                self.ui.active_works_tableWidget.setItem(row, 1, QTableWidgetItem(short_hash))
                self.ui.active_works_tableWidget.setItem(row, 2, QTableWidgetItem(preset))
                
                status_item = QTableWidgetItem(status)
                if status == "processing":
                    status_item.setForeground(QBrush(QColor(0, 100, 0)))  # Verde
                elif status == "queued":
                    status_item.setForeground(QBrush(QColor(200, 150, 0)))  # Naranja
                self.ui.active_works_tableWidget.setItem(row, 3, status_item)
                
        except sqlite3.Error as e:
            logging.error(f"Error obteniendo trabajos activos: {str(e)}")
    
    def update_ui_state(self):
        """Actualiza el estado de la UI según el estado del servidor"""
        self.ui.start_pushButton.setEnabled(not self.is_running)
        self.ui.back_pushButton.setEnabled(self.is_running)
        
        if self.is_running:
            self.ui.status_label.setText("Estado: Encendido")
            self.ui.status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.ui.status_label.setText("Estado: Detenido")
            self.ui.status_label.setStyleSheet("color: red; font-weight: bold;")
    
    def closeEvent(self, event):
        """Maneja el cierre de la ventana"""
        self.stop_api_server()
        event.accept()