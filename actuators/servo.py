import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin del servo (puedes cambiarlo según tu conexión física)
# IMPORTANTE: Asegúrate de que este pin esté libre y no esté siendo usado por otro dispositivo
# Pines PWM hardware en Raspberry Pi: GPIO 12, 13, 18, 19
# También puedes usar cualquier otro pin GPIO para PWM software
servo_pin = 18  # GPIO 18 (pin PWM hardware, pero funciona con PWM software también)

# Variable global para el objeto PWM
servo_pwm = None

def init_servo():
    """
    Inicializa el servo motor
    """
    global servo_pwm
    try:
        # Verificar que GPIO esté configurado
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
        
        # Configurar el pin como salida
        GPIO.setup(servo_pin, GPIO.OUT)
        
        # Crear objeto PWM con frecuencia de 50Hz (estándar para servos SG90)
        servo_pwm = GPIO.PWM(servo_pin, 50)
        
        # Iniciar PWM con duty cycle 0 (servo en posición inicial)
        servo_pwm.start(0)
        
        # Pequeña pausa para estabilizar
        time.sleep(0.2)
        
        # Mover a posición inicial (0 grados) para asegurar que esté en posición conocida
        servo_pwm.ChangeDutyCycle(2.5)
        time.sleep(0.3)
        
        print(f"[SERVO] Inicializado correctamente en GPIO {servo_pin}")
        return True
    except Exception as e:
        print(f"[SERVO] Error inicializando servo: {e}")
        import traceback
        traceback.print_exc()
        return False

def control_servo(angle):
    """
    Controla el servo motor SG90
    angle: ángulo en grados (0-180)
    """
    global servo_pwm
    
    try:
        # Asegurar que el servo esté inicializado
        if servo_pwm is None:
            print("Inicializando servo...")
            if not init_servo():
                print("Error: No se pudo inicializar el servo")
                return
        
        # Convertir ángulo a duty cycle
        # Servo SG90 típicamente:
        # 0° = 2.5% duty cycle (1ms de pulso en 20ms)
        # 90° = 7.5% duty cycle (1.5ms de pulso en 20ms)
        # 180° = 12.5% duty cycle (2.5ms de pulso en 20ms)
        # Fórmula: duty_cycle = 2.5 + (angle / 180) * 10
        duty_cycle = 2.5 + (angle / 180.0) * 10.0
        
        # Limitar el duty cycle entre 2.5% y 12.5%
        duty_cycle = max(2.5, min(12.5, duty_cycle))
        
        print(f"[SERVO] Moviendo a {angle}° (duty cycle: {duty_cycle:.2f}%)")
        
        # Aplicar el duty cycle
        servo_pwm.ChangeDutyCycle(duty_cycle)
        
        # Esperar tiempo suficiente para que el servo se mueva
        # Los servos SG90 necesitan al menos 0.5-1 segundo para moverse completamente
        time.sleep(0.8)
        
        # Mantener el duty cycle activo para que el servo mantenga la posición
        # NO poner a 0, ya que algunos servos necesitan la señal constante
        
        print(f"[SERVO] Posición establecida en {angle}°")
        
    except Exception as e:
        print(f"[SERVO] Error controlando servo: {e}")
        import traceback
        traceback.print_exc()

def open_gate():
    """
    Abre la compuerta (mueve el servo a 90 grados)
    """
    print("[SERVO] Abriendo compuerta...")
    control_servo(90)
    print("[SERVO] Compuerta abierta (servo en 90°)")

def close_gate():
    """
    Cierra la compuerta (mueve el servo a 0 grados - posición inicial)
    """
    print("[SERVO] Cerrando compuerta...")
    control_servo(0)
    print("[SERVO] Compuerta cerrada (servo en 0°)")

def cleanup():
    """
    Limpia los recursos del servo
    """
    global servo_pwm
    try:
        if servo_pwm is not None:
            servo_pwm.stop()
            servo_pwm = None
        GPIO.cleanup(servo_pin)
    except Exception as e:
        print(f"Error limpiando servo: {e}")

def test_servo():
    """
    Función de prueba para verificar que el servo funciona
    Mueve el servo de 0° a 90° y vuelve a 0°
    """
    print("[SERVO] Iniciando prueba del servo...")
    print(f"[SERVO] Pin GPIO: {servo_pin}")
    
    try:
        # Mover a 0 grados
        print("[SERVO] Moviendo a 0°...")
        control_servo(0)
        time.sleep(1)
        
        # Mover a 90 grados
        print("[SERVO] Moviendo a 90°...")
        control_servo(90)
        time.sleep(1)
        
        # Volver a 0 grados
        print("[SERVO] Volviendo a 0°...")
        control_servo(0)
        time.sleep(1)
        
        print("[SERVO] Prueba completada")
    except Exception as e:
        print(f"[SERVO] Error en la prueba: {e}")
        import traceback
        traceback.print_exc()

# Inicializar el servo al importar el módulo
try:
    init_servo()
except Exception as e:
    print(f"[SERVO] Advertencia: No se pudo inicializar el servo al importar: {e}")
    print(f"[SERVO] Se intentará inicializar cuando se use por primera vez")

