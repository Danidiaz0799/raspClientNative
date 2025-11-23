import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

servo_pin = 18
servo_thread = None
servo_running = False
servo_angle = 0

def init_servo():
    """Inicializa el servo motor"""
    try:
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
        
        GPIO.setup(servo_pin, GPIO.OUT)
        GPIO.output(servo_pin, GPIO.LOW)
        return True
    except Exception as e:
        print(f"[SERVO] Error inicializando: {e}")
        return False

def pwm_servo_thread():
    """Hilo que genera la señal PWM de 50Hz para el servo"""
    global servo_running, servo_angle
    
    period_ms = 20.0
    # Valores calibrados para servo SG90
    # 0° = 0.5ms (mínimo - compuerta cerrada)
    # 90° = 1.5ms (medio - compuerta abierta)
    # 180° = 2.5ms (máximo)
    min_pulse = 0.5
    max_pulse = 2.5
    
    while servo_running:
        try:
            # Calcular pulso basado en ángulo
            pulse_width_ms = min_pulse + (servo_angle / 180.0) * (max_pulse - min_pulse)
            pulse_width_ms = max(min_pulse, min(max_pulse, pulse_width_ms))
            
            low_time_ms = period_ms - pulse_width_ms
            
            # Generar pulso preciso
            GPIO.output(servo_pin, GPIO.HIGH)
            time.sleep(pulse_width_ms / 1000.0)
            GPIO.output(servo_pin, GPIO.LOW)
            time.sleep(low_time_ms / 1000.0)
        except Exception as e:
            print(f"[SERVO] Error en hilo PWM: {e}")
            break

def start_pwm():
    """Inicia el hilo PWM para el servo"""
    global servo_thread, servo_running
    
    if servo_thread is None or not servo_thread.is_alive():
        servo_running = True
        servo_thread = threading.Thread(target=pwm_servo_thread, daemon=True)
        servo_thread.start()
        time.sleep(0.1)

def stop_pwm():
    """Detiene el hilo PWM"""
    global servo_running, servo_thread
    
    servo_running = False
    if servo_thread is not None:
        servo_thread.join(timeout=1.0)
        servo_thread = None
    GPIO.output(servo_pin, GPIO.LOW)

def control_servo(angle):
    """Controla el servo motor SG90 (0-180 grados)"""
    global servo_angle
    
    try:
        if GPIO.getmode() is None:
            if not init_servo():
                return
        
        angle = max(0, min(180, int(angle)))
        old_angle = servo_angle
        
        # Si el ángulo no cambió y el PWM está detenido, no hacer nada
        # Esto evita movimientos innecesarios y temblores
        if old_angle == angle and (servo_thread is None or not servo_thread.is_alive()):
            return
        
        servo_angle = angle
        
        # Iniciar PWM solo si el ángulo cambió
        if old_angle != angle:
            if servo_thread is None or not servo_thread.is_alive():
                start_pwm()
                time.sleep(0.2)
            
            # Calcular tiempo basado en la distancia a mover
            distance = abs(angle - old_angle)
            move_time = 0.8 + (distance / 180.0) * 0.4  # Entre 0.8s y 1.2s
            time.sleep(move_time)
            
            # Detener PWM después de mover para evitar temblor
            # El servo mantendrá su posición mecánicamente
            stop_pwm()
    except Exception as e:
        print(f"[SERVO] Error: {e}")

def open_gate():
    """Abre la compuerta (servo a 90° - máximo para compuerta abierta)"""
    control_servo(90)

def close_gate():
    """Cierra la compuerta (servo a 0° - mínimo para compuerta cerrada)"""
    control_servo(0)

def cleanup():
    """Limpia los recursos del servo"""
    try:
        stop_pwm()
        GPIO.cleanup(servo_pin)
    except Exception:
        pass

try:
    init_servo()
except Exception:
    pass

