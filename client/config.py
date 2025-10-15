import os

class ClientConfig:
    # URL del servidor - CAMBIA ESTA IP POR LA DE TU SERVIDOR
    
    SERVER_URL = "http://192.168.1.100:8000"  # ← IP de Server
    
    # Directorio local para guardar videos
    LOCAL_VIDEO_DIR = os.path.join(os.path.expanduser("~"), "SynesthesiaVideos")
    
    # Tiempo de espera para conexiones (segundos)
    TIMEOUT = 30
    
    # Intentos de reconexión
    MAX_RETRIES = 3