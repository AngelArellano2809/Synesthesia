from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
import sqlite3
import uuid
import hashlib
import os
import logging

app = FastAPI()
UPLOAD_DIR = "uploads"
VIDEO_DIR = "videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Inicializar base de datos
def init_db():
    conn = sqlite3.connect('synesthesia.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs
                 (id TEXT PRIMARY KEY, mp3_hash TEXT, preset TEXT, status TEXT, 
                 video_path TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

@app.post("/create_video")
async def create_video(mp3: UploadFile, preset: str, background_tasks: BackgroundTasks):
    # Leer contenido del MP3
    mp3_content = await mp3.read()
    mp3_hash = hashlib.sha256(mp3_content).hexdigest()
    mp3_name = mp3.filename
    
    # Guardar temporalmente
    temp_path = os.path.join(UPLOAD_DIR, f"temp_{mp3_hash}.mp3")
    with open(temp_path, "wb") as f:
        f.write(mp3_content)
    
    # Crear trabajo
    job_id = str(uuid.uuid4())
    video_path = os.path.join(VIDEO_DIR, f"{job_id}.mp4")
    
    # Procesar en segundo plano
    background_tasks.add_task(process_video, job_id, temp_path, preset, video_path, mp3_name)
    
    # Guardar en DB
    conn = sqlite3.connect('synesthesia.db')
    c = conn.cursor()
    c.execute("INSERT INTO jobs (id, mp3_hash, preset, status, video_path) VALUES (?, ?, ?, ?, ?)", 
              (job_id, mp3_hash, preset, "processing", video_path))
    conn.commit()
    conn.close()
    
    logging.info(f"Nuevo trabajo creado: ID={job_id}, MP3={mp3_name}, Preset={preset}")
    
    return {"job_id": job_id, "status": "processing"}

@app.get("/video/{job_id}")
def get_video(job_id: str):
    conn = sqlite3.connect('synesthesia.db')
    c = conn.cursor()
    c.execute("SELECT video_path, status FROM jobs WHERE id=?", (job_id,))
    result = c.fetchone()
    
    if not result:
        return {"error": "Job not found"}
    
    video_path, status = result
    if status != "completed":
        return {"status": status}
    
    return FileResponse(video_path)

def process_video(job_id: str, mp3_path: str, preset: str, output_path: str, mp3_name: str):
    """Función de procesamiento simulada"""
    try:
        # Aquí iría tu lógica real de Synesthesia
        logging.info(f"Procesando trabajo {job_id} ({mp3_name}) con preset {preset}")
        
        # Simular procesamiento
        import time
        time.sleep(2)  # Fase 1: Procesamiento de audio
        logging.info(f"Trabajo {job_id}: Audio procesado")
        time.sleep(3)  # Fase 2: Generación de imágenes
        logging.info(f"Trabajo {job_id}: Imágenes generadas")
        time.sleep(2)  # Fase 3: Composición de video
        logging.info(f"Trabajo {job_id}: Video compuesto")
        
        # Actualizar estado
        conn = sqlite3.connect('synesthesia.db')
        c = conn.cursor()
        c.execute("UPDATE jobs SET status=? WHERE id=?", ("completed", job_id))
        conn.commit()
        conn.close()
        
        logging.info(f"Trabajo {job_id} completado con éxito")
        
    except Exception as e:
        logging.error(f"Error procesando trabajo {job_id}: {str(e)}")
        
        # Actualizar estado a fallido
        conn = sqlite3.connect('synesthesia.db')
        c = conn.cursor()
        c.execute("UPDATE jobs SET status=? WHERE id=?", ("failed", job_id))
        conn.commit()
        conn.close()
        
    finally:
        # Limpiar archivo temporal
        if os.path.exists(mp3_path):
            os.remove(mp3_path)

@app.get("/status")
def server_status():
    return {"status": "online", "version": "1.0"}