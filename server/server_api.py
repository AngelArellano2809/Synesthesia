import os
import uuid
import sqlite3
import hashlib
from pathlib import Path
from fastapi.responses import JSONResponse, FileResponse
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException
import sys
import traceback

# Añadir el directorio raíz al path para importar los módulos core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

# Configuración de directorios
UPLOAD_DIR = Path("uploads")
VIDEO_DIR = Path("videos")
DB_PATH = Path("database/synesthesia.db")

# Crear directorios si no existen
UPLOAD_DIR.mkdir(exist_ok=True)
VIDEO_DIR.mkdir(exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Inicializar base de datos
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs
                (id TEXT PRIMARY KEY, 
                 mp3_hash TEXT, 
                 preset TEXT, 
                 status TEXT, 
                 progress INTEGER, 
                 video_path TEXT, 
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

@app.get("/status")
async def status():
    return {"status": "online", "version": "1.0"}

@app.post("/create_video")
async def create_video(background_tasks: BackgroundTasks,
    mp3: UploadFile = File(...),
    preset: str = Form(...)  # Cambiado de Query a Form
):
    # Log para depuración
    print(f"Recibido MP3: {mp3.filename}")
    print(f"Recibido preset: {preset}")

    # Leer y hashear MP3
    mp3_content = await mp3.read()
    mp3_hash = hashlib.sha256(mp3_content).hexdigest()
    
    # Guardar temporalmente
    temp_path = UPLOAD_DIR / f"temp_{mp3_hash}.mp3"
    with open(temp_path, "wb") as f:
        f.write(mp3_content)
    
    # Crear job ID
    job_id = str(uuid.uuid4())
    video_path = VIDEO_DIR / f"{job_id}.mp4"
    
    # Registrar en base de datos
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO jobs (id, mp3_hash, preset, status, progress, video_path) VALUES (?, ?, ?, ?, ?, ?)", 
                  (job_id, mp3_hash, preset, "queued", 0, str(video_path)))
    conn.commit()
    conn.close()
    
    # Procesar en segundo plano
    background_tasks.add_task(process_video_background, job_id, str(temp_path), preset, str(video_path))
    
    return JSONResponse({"job_id": job_id, "status": "queued"}, status_code=202)

@app.get("/status/{job_id}")
def get_job_status(job_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT status, progress FROM jobs WHERE id=?", (job_id,))
    result = c.fetchone()
    conn.close()
    
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    
    status, progress = result
    return {"job_id": job_id, "status": status, "progress": progress}

@app.get("/video/{job_id}")
def download_video(job_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT status, video_path FROM jobs WHERE id=?", (job_id,))
    result = c.fetchone()
    conn.close()
    
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    
    status, video_path = result
    if status != "completed":
        raise HTTPException(status_code=425, detail="Video not ready yet")
    
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video file not found")
    
    return FileResponse(video_path, media_type='video/mp4', filename=f"synesthesia_{job_id}.mp4")

def process_video_background(job_id: str, mp3_path: str, preset: str, output_path: str):
    try:
        # Actualizar estado a procesando
        update_job_status(job_id, "processing", 10)

        # Importar y usar tu lógica real de generación
        try:
            from synesthesia import process_song
            
            # Creacion de video
            process_song(mp3_path, output_path, preset)
            
            # Actualizar estado a completado
            update_job_status(job_id, "completed", 50)
        except ImportError as e:
            error_msg = f"Error de importación: {str(e)}"
            update_job_status(job_id, f"failed: {error_msg}", 0)
            return
        except Exception as e:
            error_msg = f"Error en procesamiento: {str(e)}"
            update_job_status(job_id, f"failed: {error_msg}", 0)
            return
        
        # Actualizar estado a completado
        update_job_status(job_id, "completed", 100)
        
    except Exception as e:
        update_job_status(job_id, f"failed: {str(e)}", 0)
    finally:
        # Eliminar archivo temporal
        if os.path.exists(mp3_path):
            os.remove(mp3_path)

def update_job_status(job_id: str, status: str, progress: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE jobs SET status=?, progress=? WHERE id=?", 
              (status, progress, job_id))
    conn.commit()
    conn.close()