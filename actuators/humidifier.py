import RPi.GPIO as GPIO
from actuators.servo import open_gate, close_gate

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
humidifier_pin = 13
GPIO.setup(humidifier_pin, GPIO.OUT)

def control_humidifier(state):
    """
    Controla el humidificador y automáticamente abre/cierra la compuerta con el servo
    state: 'true' para encender, 'false' para apagar
    """
    # Controlar el humidificador
    GPIO.output(humidifier_pin, GPIO.HIGH if state == 'true' else GPIO.LOW)
    
    # Controlar el servo automáticamente
    if state == 'true':
        # Humidificador encendido: abrir compuerta (servo a 90°)
        open_gate()
        print("Humidificador encendido - Compuerta abierta")
    else:
        # Humidificador apagado: cerrar compuerta (servo a 0°)
        close_gate()
        print("Humidificador apagado - Compuerta cerrada")
