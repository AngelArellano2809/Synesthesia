from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from pathlib import Path
import uuid
import sqlite3
import hashlib
import os

app = FastAPI()
VIDEO_STORAGE = Path("./videos")

# Base de datos simple
def init_db():
    conn = sqlite3.connect('synesthesia.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs
                 (id TEXT PRIMARY KEY, mp3_hash TEXT, preset TEXT, status TEXT, video_path TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.post("/create_video")
async def create_video(mp3: UploadFile, preset: str, background_tasks: BackgroundTasks):
    # Guardar MP3 temporalmente
    mp3_bytes = await mp3.read()
    mp3_hash = hashlib.sha256(mp3_bytes).hexdigest()
    
    # Verificar si ya existe
    conn = sqlite3.connect('synesthesia.db')
    c = conn.cursor()
    c.execute("SELECT video_path FROM jobs WHERE mp3_hash=? AND preset=?", (mp3_hash, preset))
    existing = c.fetchone()
    
    if existing:
        return {"job_id": "existing", "video_path": existing[0]}
    
    # Crear nuevo trabajo
    job_id = str(uuid.uuid4())
    video_path = f"{VIDEO_STORAGE}/{job_id}.mp4"
    
    # Procesamiento en segundo plano
    background_tasks.add_task(process_video_background, mp3_bytes, preset, job_id, video_path)
    
    # Guardar en DB
    c.execute("INSERT INTO jobs VALUES (?, ?, ?, ?, ?)", 
              (job_id, mp3_hash, preset, "processing", video_path))
    conn.commit()
    conn.close()
    
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
    
    return FileResponse(video_path, media_type='video/mp4')

def process_video_background(mp3_bytes: bytes, preset: str, job_id: str, output_path: str):
    # Aquí integrarías tu demo.py existente
    from server.demo import process_audio  # Importar tu función actual
    
    # Guardar MP3 temporal
    temp_mp3 = f"temp_{job_id}.mp3"
    with open(temp_mp3, "wb") as f:
        f.write(mp3_bytes)
    
    # Procesar usando tu lógica actual
    process_audio(temp_mp3, preset, output_path)
    
    # Actualizar base de datos
    conn = sqlite3.connect('synesthesia.db')
    c = conn.cursor()
    c.execute("UPDATE jobs SET status=? WHERE id=?", ("completed", job_id))
    conn.commit()
    conn.close()
    
    # Limpiar temporal
    os.remove(temp_mp3)