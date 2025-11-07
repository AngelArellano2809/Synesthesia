import sys
import logging
import sqlite3
import subprocess
from PySide6.QtWidgets import QMainWindow, QMessageBox, QHeaderView
from PySide6.QtCore import Qt, QTimer, QProcess
from PySide6.QtGui import QColor, QBrush
from pathlib import Path


from ui.ui_server_window import *

class ServerWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_ServerWindow()
        self.ui.setupUi(self)

        # Obtener el directorio base del proyecto (carpeta server)
        self.base_dir = Path(__file__).parent.parent
        print(self.base_dir)
        
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
        # Crear un logger
        self.logger = logging.getLogger('SynesthesiaServer')
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        
        if not self.logger.handlers:
            self.logger.addHandler(self.LogHandler(self))
        
        # Configurar logging básico para capturar mensajes de otros módulos
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s\n',
            handlers=[self.LogHandler(self)]
        )

    class LogHandler(logging.Handler):
        """Manejador de logs personalizado para enviar mensajes a la UI"""
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s\n')
            self.setFormatter(formatter)
            
        def emit(self, record):
            try:
                msg = self.format(record)
                # Filtrar mensajes de status checks muy frecuentes
                # if "GET /status/" in msg and "200 OK" in msg:
                #     return
                
                # Determinar color basado en el nivel del log
                if record.levelno >= logging.ERROR:
                    html_msg = f'<span style="color: green;">{msg}</span>'
                elif record.levelno >= logging.WARNING:
                    html_msg = f'<span style="color: orange;">{msg}</span>'
                elif "Generando imágenes:" in msg or "%" in msg or "Loading pipeline" in msg:
                    html_msg = f'<span style="color: blue;">{msg}</span>'
                else:
                    html_msg = f'<span style="color: white;">{msg}</span>'
                
                self.parent.ui.server_logs_textEdit.append(html_msg)
                
                # Auto-scroll
                scrollbar = self.parent.ui.server_logs_textEdit.verticalScrollBar()
                scrollbar.setValue(scrollbar.maximum())
                
            except Exception as e:
                print(f"Error en LogHandler: {e}")

    def start_api_server(self):
        """Inicia el servidor API en un proceso separado"""
        if self.is_running:
            return
        
        try:
            # Obtener el directorio del servidor
            project_root = str(self.base_dir)
            
            # Crear proceso
            self.api_process = QProcess()
            
            # Establecer el directorio de trabajo
            self.api_process.setWorkingDirectory(project_root)

            # Configurar variables de entorno
            env = self.api_process.processEnvironment()
            env.insert("PYTHONPATH", project_root)
            # Forzar UTF-8 en la salida
            env.insert("PYTHONIOENCODING", "utf-8")
            self.api_process.setProcessEnvironment(env)
            
            # Configurar el proceso para usar uvicorn directamente
            self.api_process.setProgram(sys.executable)
            self.api_process.setArguments([
                "-m", "uvicorn", 
                "server_api:app", 
                "--host", "0.0.0.0", 
                "--port", "8000",
                "--reload",
                "--log-level", "info"
            ])
            
            # Conectar señales para capturar salida
            self.api_process.readyReadStandardOutput.connect(self.handle_stdout)
            self.api_process.readyReadStandardError.connect(self.handle_stderr)
            self.api_process.finished.connect(self.api_finished)
            self.api_process.started.connect(self.on_api_started)
            
            # Iniciar
            self.api_process.start()
            
            self.logger.info("Iniciando servidor API...")
            
        except Exception as e:
            self.logger.error(f"No se pudo iniciar el servidor API: {str(e)}")
            QMessageBox.critical(self, "Error", f"No se pudo iniciar el servidor API:\n{str(e)}")
    
    def on_api_started(self):
        """Se llama cuando el proceso del API se inicia correctamente"""
        self.is_running = True
        self.update_ui_state()
        self.update_timer.start(3000)
        self.logger.info("✅ Servidor API iniciado correctamente")
    
    def stop_api_server(self):
        """Detiene el servidor API"""
        if self.api_process and self.api_process.state() == QProcess.Running:
            self.logger.info("Deteniendo servidor API...")
            # Intentar terminación graceful primero
            self.api_process.terminate()
            if not self.api_process.waitForFinished(3000):  # Esperar 3 segundos
                # Forzar terminación si no responde
                self.logger.warning("El servidor no respondió, forzando terminación...")
                subprocess.run(["taskkill", "/f", "/pid", str(self.api_process.processId())])
                self.api_process.waitForFinished(1000)

        self.is_running = False
        self.update_ui_state()
        self.update_timer.stop()
        self.logger.info("✅ Servidor API detenido")
    
    def handle_stdout(self):
        """Maneja la salida estándar del proceso del servidor API"""
        if self.api_process:
            data = self.api_process.readAllStandardOutput()
            try:
                # Intentar diferentes codificaciones
                stdout = bytes(data).decode("utf-8", errors="replace").strip()
                if stdout:
                    self.process_api_output(stdout, "INFO")
            except UnicodeDecodeError:
                try:
                    # Fallback a latin-1
                    stdout = bytes(data).decode("latin-1", errors="replace").strip()
                    if stdout:
                        self.process_api_output(stdout, "INFO")
                except Exception as e:
                    self.logger.error(f"Error decodificando stdout: {e}")
    
    def handle_stderr(self):
        """Maneja la salida de error del proceso del servidor API"""
        if self.api_process:
            data = self.api_process.readAllStandardError()
            try:
                stderr = bytes(data).decode("utf-8", errors="replace").strip()
                if stderr:
                    self.process_api_output(stderr, "STDERR")
            except UnicodeDecodeError:
                try:
                    stderr = bytes(data).decode("latin-1", errors="replace").strip()
                    if stderr:
                        self.process_api_output(stderr, "STDERR")
                except Exception as e:
                    self.logger.error(f"Error decodificando stderr: {e}")

    def process_api_output(self, message, source):
        """
        Procesa y categoriza la salida del API
        source: "INFO" para stdout, "STDERR" para stderr
        """
        # Filtrar mensajes de Uvicorn muy verbosos
        if "Uvicorn running on" in message:
            self.logger.info(f"🔄 {message}")
        elif "Application startup complete" in message:
            self.logger.info(f"✅ {message}")
        elif "Shutting down" in message:
            self.logger.info(f"🛑 {message}")
        
        # Mensajes de progreso de Synesthesia
        elif any(keyword in message for keyword in ["Generando imagen", "Procesando", "Cargando modelo", "progress"]):
            self.logger.info(f"📊 {message}")
        
        # Mensajes de error reales
        elif any(keyword in message.lower() for keyword in ["error", "exception", "traceback", "failed"]):
            self.logger.error(f"❌ {message}")
        
        # Requests HTTP (filtrar algunos para reducir ruido)
        elif "GET /status/" in message:
            # No mostrar todos los status checks para reducir ruido
            pass
        elif "HTTP" in message and "200" in message:
            self.logger.info(f"🌐 {message}")
        elif "HTTP" in message and "500" in message:
            self.logger.error(f"🌐 {message}")
        
        # Mensajes informativos generales
        elif source == "STDERR" and not any(keyword in message.lower() for keyword in ["error", "warning"]):
            # Muchos mensajes de Uvicorn van a stderr pero son informativos
            self.logger.info(f"ℹ️  {message}")
        else:
            # Cualquier otro mensaje
            self.logger.info(message)
    
    def api_finished(self, exit_code, exit_status):
        """Maneja la finalización del proceso del servidor API"""
        self.is_running = False
        self.update_ui_state()
        self.update_timer.stop()
        
        if exit_code == 0:
            self.logger.info("✅ Servidor API terminado correctamente")
        else:
            self.logger.error(f"❌ Servidor API terminado con código de error: {exit_code}")
    
    def refresh_data(self):
        """Actualiza los datos mostrados en la UI"""
        if not self.is_running:
            return
        
        try:
            self.update_database_view()
            self.update_active_jobs()
            
        except Exception as e:
            self.logger.error(f"Error actualizando datos: {str(e)}")
    
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
                        elif value == "queued":
                            item.setForeground(QBrush(QColor(255, 165, 0)))  # Naranja
                    
                    self.ui.data_base_tableWidget.setItem(row, col, item)
                    
        except sqlite3.Error as e:
            self.logger.error(f"Error de base de datos: {str(e)}")
    
    def update_active_jobs(self):
        """Actualiza la tabla de trabajos activos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, mp3_hash, preset, status FROM jobs WHERE status IN ('queued', 'processing') ORDER BY created_at DESC")
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
                    status_item.setForeground(QBrush(QColor(255, 165, 0)))  # Naranja
                self.ui.active_works_tableWidget.setItem(row, 3, status_item)
                
        except sqlite3.Error as e:
            self.logger.error(f"Error obteniendo trabajos activos: {str(e)}")
    
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
