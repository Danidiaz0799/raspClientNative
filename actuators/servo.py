import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin del servo (puedes cambiarlo según tu conexión física)
servo_pin = 18  # GPIO 18 (pin PWM hardware, pero funciona con PWM software también)

# Configurar el pin como salida
GPIO.setup(servo_pin, GPIO.OUT)

# Crear objeto PWM con frecuencia de 50Hz (estándar para servos)
servo_pwm = GPIO.PWM(servo_pin, 50)

# Iniciar PWM con duty cycle 0 (servo en posición inicial)
servo_pwm.start(0)

def control_servo(angle):
    """
    Controla el servo motor SG90
    angle: ángulo en grados (0-180)
    """
    try:
        # Convertir ángulo a duty cycle
        # Servo SG90: 0° = 2.5% duty cycle, 90° = 7.5% duty cycle, 180° = 12.5% duty cycle
        # Fórmula: duty_cycle = 2.5 + (angle / 180) * 10
        duty_cycle = 2.5 + (angle / 180.0) * 10.0
        
        # Limitar el duty cycle entre 2.5% y 12.5%
        duty_cycle = max(2.5, min(12.5, duty_cycle))
        
        # Aplicar el duty cycle
        servo_pwm.ChangeDutyCycle(duty_cycle)
        
        # Esperar un momento para que el servo se mueva
        time.sleep(0.3)
        
        # Detener el pulso (opcional, pero ayuda a estabilizar)
        servo_pwm.ChangeDutyCycle(0)
        
    except Exception as e:
        print(f"Error controlando servo: {e}")

def open_gate():
    """
    Abre la compuerta (mueve el servo a 90 grados)
    """
    control_servo(90)
    print("Compuerta abierta (servo en 90°)")

def close_gate():
    """
    Cierra la compuerta (mueve el servo a 0 grados - posición inicial)
    """
    control_servo(0)
    print("Compuerta cerrada (servo en 0°)")

def cleanup():
    """
    Limpia los recursos del servo
    """
    try:
        servo_pwm.stop()
        GPIO.cleanup(servo_pin)
    except Exception as e:
        print(f"Error limpiando servo: {e}")

