#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para el servo motor SG90
Ejecuta: python3 test_servo.py
"""

import RPi.GPIO as GPIO
import time

# Configuración
SERVO_PIN = 18  # GPIO 18

def setup_gpio():
    """Configura GPIO"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    GPIO.output(SERVO_PIN, GPIO.LOW)
    print(f"[TEST] GPIO {SERVO_PIN} configurado como salida")

def set_angle(angle):
    """
    Mueve el servo a un ángulo específico usando PWM manual
    angle: 0-180 grados
    """
    # Convertir ángulo a ancho de pulso
    # Servo SG90 típicamente:
    # 0° = 1ms (5% duty cycle)
    # 90° = 1.5ms (7.5% duty cycle)  
    # 180° = 2.5ms (12.5% duty cycle)
    
    pulse_width_ms = 1.0 + (angle / 180.0) * 1.5
    
    print(f"[TEST] Moviendo a {angle}° (pulso: {pulse_width_ms:.2f}ms)")
    
    # Generar 50 pulsos (1 segundo) para que el servo se mueva
    for _ in range(50):
        GPIO.output(SERVO_PIN, GPIO.HIGH)
        time.sleep(pulse_width_ms / 1000.0)
        GPIO.output(SERVO_PIN, GPIO.LOW)
        time.sleep((20.0 - pulse_width_ms) / 1000.0)
    
    print(f"[TEST] Posición {angle}° establecida")

def test_servo():
    """Prueba completa del servo"""
    print("=" * 50)
    print("PRUEBA DEL SERVO MOTOR SG90")
    print("=" * 50)
    print(f"Pin GPIO: {SERVO_PIN}")
    print("Conexiones esperadas:")
    print("  - Naranja/Amarillo (señal) -> GPIO 18")
    print("  - Rojo (alimentación) -> 5V")
    print("  - Negro/Marrón (tierra) -> GND")
    print("=" * 50)
    
    try:
        setup_gpio()
        
        print("\n[TEST] Iniciando prueba en 3 segundos...")
        time.sleep(3)
        
        # Prueba 1: Mover a 0 grados
        print("\n[TEST] Prueba 1: Moviendo a 0° (posición inicial)")
        set_angle(0)
        time.sleep(1)
        
        # Prueba 2: Mover a 90 grados
        print("\n[TEST] Prueba 2: Moviendo a 90° (compuerta abierta)")
        set_angle(90)
        time.sleep(1)
        
        # Prueba 3: Mover a 180 grados
        print("\n[TEST] Prueba 3: Moviendo a 180° (máxima extensión)")
        set_angle(180)
        time.sleep(1)
        
        # Prueba 4: Volver a 0 grados
        print("\n[TEST] Prueba 4: Volviendo a 0°")
        set_angle(0)
        time.sleep(1)
        
        # Prueba 5: Movimiento suave de 0 a 90
        print("\n[TEST] Prueba 5: Movimiento suave de 0° a 90°")
        for angle in range(0, 91, 10):
            set_angle(angle)
            time.sleep(0.2)
        
        # Volver a 0
        print("\n[TEST] Volviendo a posición inicial (0°)")
        set_angle(0)
        time.sleep(1)
        
        print("\n" + "=" * 50)
        print("[TEST] ¡PRUEBA COMPLETADA!")
        print("=" * 50)
        print("\nSi el servo NO se movió, verifica:")
        print("  1. Las conexiones (GPIO 18, 5V, GND)")
        print("  2. Que el servo tenga alimentación externa de 5V")
        print("  3. Que el pin GPIO 18 esté libre")
        print("  4. Que el servo no esté dañado")
        
    except KeyboardInterrupt:
        print("\n[TEST] Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n[TEST] ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        GPIO.output(SERVO_PIN, GPIO.LOW)
        GPIO.cleanup()
        print("\n[TEST] GPIO limpiado")

if __name__ == "__main__":
    test_servo()

