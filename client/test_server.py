# Prueba de conexión simple
import requests
from config import ClientConfig

try:
    response = requests.get(f"{ClientConfig.SERVER_URL}/status", timeout=5)
    if response.status_code == 200:
        print("✓ Conexión exitosa con el servidor")
    else:
        print("✗ El servidor respondió con error")
except Exception as e:
    print(f"✗ No se pudo conectar: {e}")