from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget
import sqlite3

class ServerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Synesthesia Server")
        self.setGeometry(100, 100, 800, 600)
        
        self.job_list = QListWidget()
        
        layout = QVBoxLayout()
        layout.addWidget(self.job_list)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.update_job_list()
        self.timer = self.startTimer(5000)  # Actualizar cada 5 segundos
    
    def update_job_list(self):
        self.job_list.clear()
        conn = sqlite3.connect('synesthesia.db')
        c = conn.cursor()
        c.execute("SELECT id, mp3_hash, preset, status FROM jobs ORDER BY rowid DESC LIMIT 50")
        
        for job in c.fetchall():
            job_id, mp3_hash, preset, status = job
            self.job_list.addItem(f"{status.upper()} | {preset} | {mp3_hash[:8]}... | {job_id}")
        
        conn.close()
    
    def timerEvent(self, event):
        self.update_job_list()