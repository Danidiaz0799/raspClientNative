import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

motor_pin = 6
servo_thread = None
servo_running = False
servo_angle = 0
_current_state = None

def init_servo():
    try:
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
        
        GPIO.setup(motor_pin, GPIO.OUT)
        GPIO.output(motor_pin, GPIO.LOW)
        return True
    except Exception as e:
        print(f"[MOTOR] Error inicializando servo: {e}")
        return False

def pwm_servo_thread():
    global servo_running, servo_angle
    
    period_ms = 20.0
    min_pulse = 0.5
    max_pulse = 2.5
    
    while servo_running:
        try:
            pulse_width_ms = min_pulse + (servo_angle / 180.0) * (max_pulse - min_pulse)
            pulse_width_ms = max(min_pulse, min(max_pulse, pulse_width_ms))
            
            low_time_ms = period_ms - pulse_width_ms
            
            GPIO.output(motor_pin, GPIO.HIGH)
            time.sleep(pulse_width_ms / 1000.0)
            GPIO.output(motor_pin, GPIO.LOW)
            time.sleep(low_time_ms / 1000.0)
        except Exception as e:
            print(f"[MOTOR] Error en hilo PWM: {e}")
            break

def start_pwm():
    global servo_thread, servo_running
    
    if servo_thread is None or not servo_thread.is_alive():
        servo_running = True
        servo_thread = threading.Thread(target=pwm_servo_thread, daemon=True)
        servo_thread.start()
        time.sleep(0.1)

def stop_pwm():
    global servo_running, servo_thread
    
    servo_running = False
    if servo_thread is not None:
        servo_thread.join(timeout=1.0)
        servo_thread = None
    GPIO.output(motor_pin, GPIO.LOW)

def control_servo(angle):
    global servo_angle
    
    try:
        if GPIO.getmode() is None:
            if not init_servo():
                return
        
        angle = max(0, min(180, int(angle)))
        old_angle = servo_angle
        
        if old_angle == angle and (servo_thread is None or not servo_thread.is_alive()):
            return
        
        servo_angle = angle
        
        if old_angle != angle:
            if servo_thread is None or not servo_thread.is_alive():
                start_pwm()
                time.sleep(0.2)
            
            distance = abs(angle - old_angle)
            move_time = 0.8 + (distance / 180.0) * 0.4
            time.sleep(move_time)
            
            stop_pwm()
    except Exception as e:
        print(f"[MOTOR] Error controlando servo: {e}")

def control_motor(state):
    global _current_state
    
    if _current_state != state:
        _current_state = state
        if state == 'true':
            control_servo(90)
        else:
            control_servo(0)

try:
    init_servo()
except Exception:
    pass
