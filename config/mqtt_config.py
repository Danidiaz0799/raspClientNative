import paho.mqtt.client as mqtt
from config import config
import time

def connect_mqtt():
    client = mqtt.Client()
    while True:
        try:
            client.connect(config.SERVER, 1883, 60)
            print("Conexion MQTT establecida")
            return client
        except Exception as e:
            print(f"Error MQTT: {e}. Reintentando en 5s...")
            time.sleep(5)
