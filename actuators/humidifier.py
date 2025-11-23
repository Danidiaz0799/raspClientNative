import RPi.GPIO as GPIO
from actuators.servo import open_gate, close_gate

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
humidifier_pin = 13
GPIO.setup(humidifier_pin, GPIO.OUT)

def control_humidifier(state):
    """Controla el humidificador y automáticamente abre/cierra la compuerta con el servo"""
    GPIO.output(humidifier_pin, GPIO.HIGH if state == 'true' else GPIO.LOW)
    
    if state == 'true':
        open_gate()
    else:
        close_gate()
