import subprocess
from config import config

def connect_wifi():
    try:
        result = subprocess.run(['iwgetid'], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        return False
