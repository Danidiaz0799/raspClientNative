import subprocess
from config import config

def connect_wifi():
    try:
        print("Verificando WiFi...")
        result = subprocess.run(['iwgetid'], capture_output=True, text=True)
        if result.returncode == 0:
            print("WiFi OK")
            return True
        else:
            print(f"WiFi Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"WiFi Exception: {e}")
        return False
