# -*- coding: utf-8 -*-
from config.wifi_config import connect_wifi
from config.mqtt_config import connect_mqtt
from actuators.light import control_light
from actuators.fan import control_fan
from actuators.humidifier import control_humidifier
from actuators.motor import control_motor
from sensors.sht3x import publish_sht3x_data
from config import config
from actuators.oled import display_message
import time
import threading

def register_client(client):
    registration_message = f"{config.CLIENT_ID}"
    client.publish(config.TOPIC_REGISTER, registration_message)
    print(f"Cliente registrado: {config.CLIENT_ID}")

def on_message(client, userdata, message):
    print(f"Mensaje: {message.topic}")
    if message.topic == config.TOPIC_LIGHT:
        state = message.payload.decode('utf-8')
        control_light(state)
    elif message.topic == config.TOPIC_FAN:
        state = message.payload.decode('utf-8')
        control_fan(state)
    elif message.topic == config.TOPIC_HUMIDIFIER:
        state = message.payload.decode('utf-8')
        control_humidifier(state)
    elif message.topic == config.TOPIC_MOTOR:
        state = message.payload.decode('utf-8')
        control_motor(state)

def mqtt_loop(client):
    while True:
        try:
            client.loop()
        except Exception as e:
            print(f"Error MQTT: {e}")
            client = connect_mqtt()
            setup_mqtt_client(client)
        time.sleep(1)

def setup_mqtt_client(client):
    client.on_message = on_message
    client.subscribe(config.TOPIC_LIGHT)
    client.subscribe(config.TOPIC_FAN)
    client.subscribe(config.TOPIC_HUMIDIFIER)
    client.subscribe(config.TOPIC_MOTOR)
    register_client(client)

def sht3x_loop(client):
    while True:
        try:
            publish_sht3x_data(client, config.TOPIC_SHT3X)
        except Exception as e:
            print(f"Error sensor: {e}")
        time.sleep(5)

def main():
    print("Iniciando cliente...")
    display_message("Conectando a Wi-Fi...")
    if connect_wifi():
        print("WiFi conectado")
        display_message("Wi-Fi Conectado")
        client = connect_mqtt()
        if client:
            print(f"MQTT conectado como {config.CLIENT_ID}")
            display_message(f"Conectado como {config.CLIENT_ID}")
            setup_mqtt_client(client)
            
            threading.Thread(target=mqtt_loop, args=(client,)).start()
            threading.Thread(target=sht3x_loop, args=(client,)).start()
            
            print("Loops iniciados")
            while True:
                register_client(client)
                time.sleep(300)
        else:
            print("Error: No se pudo conectar a MQTT")
            display_message("No se conecto a MQTT")
    else:
        print("Error: No se pudo conectar a WiFi")
        display_message("No se conecto a Wi-Fi")

if __name__ == "__main__":
    main()
