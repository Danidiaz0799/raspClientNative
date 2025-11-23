import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin del servo (puedes cambiarlo según tu conexión física)
# IMPORTANTE: Asegúrate de que este pin esté libre y no esté siendo usado por otro dispositivo
servo_pin = 18  # GPIO 18

# Variable global para controlar el hilo PWM
servo_thread = None
servo_running = False
servo_angle = 0

def init_servo():
    """
    Inicializa el servo motor
    """
    try:
        # Verificar que GPIO esté configurado
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
        
        # Configurar el pin como salida
        GPIO.setup(servo_pin, GPIO.OUT)
        GPIO.output(servo_pin, GPIO.LOW)
        
        print(f"[SERVO] Inicializado correctamente en GPIO {servo_pin}")
        return True
    except Exception as e:
        print(f"[SERVO] Error inicializando servo: {e}")
        import traceback
        traceback.print_exc()
        return False

def pwm_servo_thread():
    """
    Hilo que genera la señal PWM para el servo
    Genera pulsos de 50Hz (20ms de período)
    """
    global servo_running, servo_angle
    
    while servo_running:
        try:
            # Convertir ángulo a ancho de pulso en milisegundos
            # Servo SG90: 0° = 1ms, 90° = 1.5ms, 180° = 2.5ms
            pulse_width_ms = 1.0 + (servo_angle / 180.0) * 1.5
            
            # Generar pulso HIGH
            GPIO.output(servo_pin, GPIO.HIGH)
            time.sleep(pulse_width_ms / 1000.0)  # Convertir ms a segundos
            
            # Generar pulso LOW (completar el período de 20ms)
            GPIO.output(servo_pin, GPIO.LOW)
            time.sleep((20.0 - pulse_width_ms) / 1000.0)
            
        except Exception as e:
            print(f"[SERVO] Error en hilo PWM: {e}")
            break

def start_pwm():
    """
    Inicia el hilo PWM para el servo
    """
    global servo_thread, servo_running
    
    if servo_thread is None or not servo_thread.is_alive():
        servo_running = True
        servo_thread = threading.Thread(target=pwm_servo_thread, daemon=True)
        servo_thread.start()
        print("[SERVO] Hilo PWM iniciado")

def stop_pwm():
    """
    Detiene el hilo PWM
    """
    global servo_running, servo_thread
    
    servo_running = False
    if servo_thread is not None:
        servo_thread.join(timeout=1.0)
        servo_thread = None
    GPIO.output(servo_pin, GPIO.LOW)
    print("[SERVO] Hilo PWM detenido")

def control_servo(angle):
    """
    Controla el servo motor SG90
    angle: ángulo en grados (0-180)
    """
    global servo_angle
    
    try:
        # Asegurar que el servo esté inicializado
        if GPIO.getmode() is None:
            if not init_servo():
                print("[SERVO] Error: No se pudo inicializar el servo")
                return
        
        # Limitar el ángulo entre 0 y 180 grados
        angle = max(0, min(180, angle))
        servo_angle = angle
        
        # Iniciar PWM si no está corriendo
        if servo_thread is None or not servo_thread.is_alive():
            start_pwm()
            # Dar tiempo para que el servo se estabilice
            time.sleep(0.3)
        
        # Calcular ancho de pulso para debug
        pulse_width_ms = 1.0 + (angle / 180.0) * 1.5
        print(f"[SERVO] Moviendo a {angle}° (pulso: {pulse_width_ms:.2f}ms)")
        
        # Esperar tiempo suficiente para que el servo se mueva
        # Los servos SG90 necesitan al menos 0.5-1 segundo para moverse completamente
        time.sleep(0.6)
        
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
    try:
        stop_pwm()
        GPIO.cleanup(servo_pin)
    except Exception as e:
        print(f"[SERVO] Error limpiando servo: {e}")

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

# Inicializar GPIO al importar el módulo (pero no iniciar PWM todavía)
try:
    init_servo()
except Exception as e:
    print(f"[SERVO] Advertencia: No se pudo inicializar el servo al importar: {e}")
    print(f"[SERVO] Se intentará inicializar cuando se use por primera vez")

