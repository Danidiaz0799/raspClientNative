import RPi.GPIO as GPIO
from actuators.servo import open_gate, close_gate

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
humidifier_pin = 13
GPIO.setup(humidifier_pin, GPIO.OUT)

# Estado actual del humidificador para evitar movimientos innecesarios del servo
_current_state = None

def control_humidifier(state):
    """Controla el humidificador y automáticamente abre/cierra la compuerta con el servo"""
    global _current_state
    
    # Solo mover el servo si el estado realmente cambió
    if _current_state != state:
        _current_state = state
        GPIO.output(humidifier_pin, GPIO.HIGH if state == 'true' else GPIO.LOW)
        
        if state == 'true':
            open_gate()
        else:
            close_gate()
    else:
        # Si el estado no cambió, solo actualizar el GPIO sin mover el servo
        GPIO.output(humidifier_pin, GPIO.HIGH if state == 'true' else GPIO.LOW)
