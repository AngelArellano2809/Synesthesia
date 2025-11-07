import os
import uuid
import sqlite3
import hashlib
from pathlib import Path
from fastapi.responses import JSONResponse, FileResponse
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException
import sys
import uvicorn
import logging

# Añadir el directorio raíz al path para importar los módulos core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

logger = logging.getLogger('SynesthesiaServer')
logger.setLevel(logging.INFO)

# Configuración de rutas absolutas
BASE_DIR = Path(__file__).parent
VIDEO_DIR = BASE_DIR / "videos"
UPLOAD_DIR = BASE_DIR / "uploads"
DB_PATH = BASE_DIR / "database" / "synesthesia.db"

# Crear directorios si no existen
VIDEO_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)
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
async def create_video(
    background_tasks: BackgroundTasks,
    mp3: UploadFile = File(...),
    preset: str = Form(...) 
):
    # Log para depuración
    print(f"Recibido MP3: {mp3.filename}")
    print(f"Recibido preset: {preset}")

    # Leer y hashear MP3
    mp3_content = await mp3.read()
    mp3_hash = hashlib.sha256(mp3_content).hexdigest()

    # VERIFICAR SI YA EXISTE EN LA BASE DE DATOS
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Buscar trabajos completados con el mismo hash y preset
    c.execute("""
        SELECT id, status, video_path 
        FROM jobs 
        WHERE mp3_hash = ? AND preset = ? AND status = 'completed'
        ORDER BY created_at DESC 
        LIMIT 1
    """, (mp3_hash, preset))
    
    existing_job = c.fetchone()

    if existing_job:
        # El video ya existe
        _job_id, _status, _video_path = existing_job
        # Verificar que el archivo de video todavía existe
        video_file = VIDEO_DIR / _job_id / "video.mp4"
        syn_file = VIDEO_DIR / _job_id / "video.syn"
        
        if video_file.exists() and syn_file.exists():
            conn.close()
            
            print(f" Trabajo existente encontrado para MP3 hash: {mp3_hash[:16]}... con preset: {preset}")
            print(f"   Job ID existente: {_job_id}")
            
            return JSONResponse({
                "job_id": _job_id, 
                "status": "already_exists"
            }, status_code=200)
        else:
            # Si los archivos no existen, marcar como fallido y continuar con la creación de un nuevo trabajo
            update_job_status(_job_id, "not_found", 4)

    # Guardar temporalmente
    temp_path = UPLOAD_DIR / f"temp_{mp3_hash}.mp3"
    with open(temp_path, "wb") as f:
        f.write(mp3_content)

    # Cerrar la conexión de la verificación
    conn.close()
        
    # Crear job ID
    job_id = str(uuid.uuid4())
    video_path = VIDEO_DIR / job_id
    video_path.mkdir(parents=True, exist_ok=True)
    video_dir_path = str(video_path)
    
    # Registrar en base de datos
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO jobs (id, mp3_hash, preset, status, progress, video_path) VALUES (?, ?, ?, ?, ?, ?)", 
                  (job_id, mp3_hash, preset, "queued", 0, str(video_dir_path)))
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
    # conn = sqlite3.connect(DB_PATH)
    # c = conn.cursor()
    # c.execute("SELECT status FROM jobs WHERE id=?", (job_id,))
    # result = c.fetchone()
    # conn.close()
    
    # if not result:
    #     raise HTTPException(status_code=404, detail="Job not found")
    
    # status, video_dir  = result
    # if status != "completed":
    #     raise HTTPException(status_code=425, detail="Video not ready yet")
    
    video_file_path = VIDEO_DIR / job_id / "video.mp4"
    print(video_file_path)

    return FileResponse(str(video_file_path), media_type='video/mp4', filename=f"synesthesia_{job_id}.mp4")

@app.get("/metadata/{job_id}")
async def download_metadata(job_id: str):
    # conn = sqlite3.connect(DB_PATH)
    # c = conn.cursor()
    # c.execute("SELECT status, video_path FROM jobs WHERE id=?", (job_id,))
    # result = c.fetchone()
    # conn.close()
    
    # if not result:
    #     raise HTTPException(status_code=404, detail="Job not found")
    
    # status, video_dir = result
    # if status != "completed":
    #     raise HTTPException(status_code=425, detail="Metadata not ready yet")
    
    metadata_file_path = VIDEO_DIR / job_id / "video.syn"
    print(metadata_file_path)
    
    return FileResponse(str(metadata_file_path), media_type='application/json', filename=f"synesthesia_{job_id}.syn")

def process_video_background(job_id: str, mp3_path: str, preset: str, output_path: str):
    try:
        # Actualizar estado a procesando
        update_job_status(job_id, "processing", 10)

        try:
            from synesthesia import process_song
            
            # Creacion de video
            process_song(mp3_path, output_path, preset)
            
            # Actualizar estado a completado
            update_job_status(job_id, "completed", 90)
        except ImportError as e:
            error_msg = f"Error de importación: {str(e)}"
            update_job_status(job_id, f"failed: {error_msg}", 1)
            return
        except Exception as e:
            error_msg = f"Error en procesamiento: {str(e)}"
            update_job_status(job_id, f"failed: {error_msg}", 2)
            return
        
        # Actualizar estado a completado
        update_job_status(job_id, "completed", 100)
        
    except Exception as e:
        update_job_status(job_id, f"failed: {str(e)}", 3)
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)