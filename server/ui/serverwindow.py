import sys
import os
import sqlite3
import logging
import subprocess
from datetime import datetime
from PySide6.QtWidgets import QMainWindow, QApplication, QHeaderView, QMessageBox
from PySide6.QtCore import Qt, QTimer, Signal, QProcess
from PySide6.QtGui import QColor, QBrush

from ui.ui_server_window import *

from PySide6.QtCore import Slot

#crear ventana
class ServerWindow(QMainWindow):
    # Señal para actualizar la UI desde otros hilos
    log_message = Signal(str)
    job_added = Signal(dict)
    job_updated = Signal(str, str)

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_ServerWindow()
        self.ui.setupUi(self)

        # Configuración inicial
        self.server_process = None
        self.is_running = False
        self.db_path = "synesthesia.db"

        # Configurar UI
        self.setup_ui()
        
        # Conectar señales
        self.connect_signals()
        
        # Configurar temporizador para actualizar datos
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.refresh_data)
        
        # Configurar logging
        self.setup_logging()
        
        # Estado inicial
        self.update_ui_state()

    def setup_ui(self):
        """Configura elementos iniciales de la UI"""
        # Configurar tablas
        self.ui.active_works_tableWidget.setColumnCount(4)
        self.ui.active_works_tableWidget.setHorizontalHeaderLabels(["ID", "MP3", "Preset", "Estado"])
        self.ui.active_works_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.active_works_tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.ui.active_works_tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        
        self.ui.data_base_tableWidget.setColumnCount(6)
        self.ui.data_base_tableWidget.setHorizontalHeaderLabels(["ID", "MP3 Hash", "Preset", "Estado", "Ruta", "Fecha"])
        self.ui.data_base_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.data_base_tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.ui.data_base_tableWidget.setSelectionBehavior(QTableWidget.SelectRows)

        # Configurar botones
        self.ui.start_pushButton.setEnabled(True)
        self.ui.back_pushButton.setEnabled(False)
        
        # Configurar logs
        self.ui.server_logs_textEdit.setStyleSheet("font-family: monospace;")

    def connect_signals(self):
        """Conecta todas las señales"""
        self.ui.start_pushButton.clicked.connect(self.start_server)
        self.ui.back_pushButton.clicked.connect(self.stop_server)
        self.log_message.connect(self.handle_log_message)
        self.job_added.connect(self.handle_job_added)
        self.job_updated.connect(self.handle_job_updated)

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
            self.parent.log_message.emit(msg)

    def handle_log_message(self, msg):
        """Maneja un mensaje de log recibido"""
        self.ui.server_logs_textEdit.append(msg)
        self.ui.server_logs_textEdit.verticalScrollBar().setValue(
            self.ui.server_logs_textEdit.verticalScrollBar().maximum()
        )
    
    def handle_job_added(self, job_data):
        """Maneja un nuevo trabajo añadido"""
        row_position = self.ui.active_works_tableWidget.rowCount()
        self.ui.active_works_tableWidget.insertRow(row_position)
        
        self.ui.active_works_tableWidget.setItem(row_position, 0, QTableWidgetItem(job_data["id"]))
        self.ui.active_works_tableWidget.setItem(row_position, 1, QTableWidgetItem(job_data["mp3_name"]))
        self.ui.active_works_tableWidget.setItem(row_position, 2, QTableWidgetItem(job_data["preset"]))
        
        status_item = QTableWidgetItem("En cola")
        status_item.setForeground(QBrush(QColor(200, 150, 0)))  # Naranja
        self.ui.active_works_tableWidget.setItem(row_position, 3, status_item)

    def handle_job_updated(self, job_id, status):
        """Actualiza el estado de un trabajo existente"""
        for row in range(self.ui.active_works_tableWidget.rowCount()):
            if self.ui.active_works_tableWidget.item(row, 0).text() == job_id:
                status_item = self.ui.active_works_tableWidget.item(row, 3)
                status_item.setText(status)
                
                if "procesando" in status.lower():
                    status_item.setForeground(QBrush(QColor(0, 100, 0)))  # Verde
                elif "completado" in status.lower():
                    status_item.setForeground(QBrush(QColor(0, 150, 0)))  # Verde más oscuro
                elif "error" in status.lower():
                    status_item.setForeground(QBrush(QColor(200, 0, 0)))  # Rojo
                
                return
            
    def refresh_data(self):
        """Actualiza los datos mostrados en la UI"""
        if not self.is_running:
            return
        
        try:
            # Actualizar vista de base de datos
            self.update_database_view()
            
            # Actualizar trabajos activos (si es necesario)
            # Esta parte dependerá de cómo implementes el servidor
            # Por ahora simula actualizaciones
            
        except Exception as e:
            logging.error(f"Error actualizando datos: {str(e)}")

    def update_database_view(self):
        """Actualiza la vista de la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, mp3_hash, preset, status, video_path, created_at FROM jobs ORDER BY created_at DESC LIMIT 50")
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

    def start_server(self):
        """Inicia el servidor FastAPI"""
        try:
            # Crear proceso para ejecutar el servidor
            self.server_process = QProcess()
            self.server_process.readyReadStandardOutput.connect(self.handle_stdout)
            self.server_process.readyReadStandardError.connect(self.handle_stderr)
            self.server_process.finished.connect(self.handle_finished)
            
            # Comando para ejecutar el servidor (ajusta según tu entorno)
            command = "uvicorn"
            args = ["api_server:app", "--host", "0.0.0.0", "--port", "8000"]
            
            self.server_process.start(command, args)
            
            self.is_running = True
            self.update_ui_state()
            
            logging.info("Servidor iniciado")
            logging.info(f"Endpoint: POST http://localhost:8000/create_video")
            
            # Iniciar temporizador de actualización
            self.update_timer.start(5000)  # Actualizar cada 5 segundos
            
            # Simular un nuevo trabajo para prueba
            self.simulate_new_job()
            
        except Exception as e:
            logging.error(f"No se pudo iniciar el servidor: {str(e)}")
            QMessageBox.critical(self, "Error", f"No se pudo iniciar el servidor:\n{str(e)}")

    def stop_server(self):
        """Detiene el servidor"""
        if self.server_process and self.server_process.state() == QProcess.Running:
            self.server_process.terminate()
            self.server_process.waitForFinished(2000)  # Esperar hasta 2 segundos
        
        self.is_running = False
        self.update_ui_state()
        self.update_timer.stop()
        
        logging.info("Servidor detenido")

    def handle_stdout(self):
        """Maneja la salida estándar del proceso del servidor"""
        data = self.server_process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8").strip()
        if stdout:
            logging.info(f"SERVIDOR: {stdout}")

    def handle_stderr(self):
        """Maneja la salida de error del proceso del servidor"""
        data = self.server_process.readAllStandardError()
        stderr = bytes(data).decode("utf8").strip()
        if stderr:
            logging.error(f"SERVIDOR: {stderr}")
    
    def handle_finished(self, exit_code, exit_status):
        """Maneja la finalización del proceso del servidor"""
        self.is_running = False
        self.update_ui_state()
        self.update_timer.stop()
        
        if exit_code == 0:
            logging.info("Servidor terminado correctamente")
        else:
            logging.error(f"Servidor terminado con código de error: {exit_code}")

    def update_ui_state(self):
        """Actualiza el estado de la UI según el estado del servidor"""
        self.ui.start_pushButton.setEnabled(not self.is_running)
        self.ui.back_pushButton.setEnabled(self.is_running)
        
        if self.is_running:
            self.ui.status_label.setText("Estado: En ejecución")
            self.ui.status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.ui.status_label.setText("Estado: Detenido")
            self.ui.status_label.setStyleSheet("color: red; font-weight: bold;")

    def simulate_new_job(self):
        """Simula la adición de un nuevo trabajo para propósitos de demostración"""
        if not self.is_running:
            return
        
        # Datos simulados
        job_id = f"job_{datetime.now().strftime('%H%M%S')}"
        mp3_name = "cancion_demo.mp3"
        preset = "digital_futuristic"
        
        # Emitir señal de nuevo trabajo
        self.job_added.emit({
            "id": job_id,
            "mp3_name": mp3_name,
            "preset": preset
        })
        
        # Simular progreso del trabajo
        self.simulate_job_progress(job_id)

    def simulate_job_progress(self, job_id):
        """Simula el progreso de un trabajo"""
        if not self.is_running:
            return
        
        # Cambiar estado a "Procesando"
        self.job_updated.emit(job_id, "Procesando audio")
        QTimer.singleShot(2000, lambda: self.job_updated.emit(job_id, "Generando imágenes"))
        
        # Simular finalización exitosa
        QTimer.singleShot(5000, lambda: self.job_updated.emit(job_id, "Completado"))
        
        # Simular fallo (para demostración)
        # QTimer.singleShot(5000, lambda: self.job_updated.emit(job_id, "Error en generación"))
        
        # Simular nuevo trabajo después de un tiempo
        QTimer.singleShot(10000, self.simulate_new_job)

    def closeEvent(self, event):
        """Maneja el cierre de la ventana"""
        if self.is_running:
            self.stop_server()
        
        # Asegurarse de que el proceso esté terminado
        if self.server_process and self.server_process.state() == QProcess.Running:
            self.server_process.terminate()
            self.server_process.waitForFinished(1000)

