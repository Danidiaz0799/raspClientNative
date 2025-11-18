import paho.mqtt.client as mqtt
from config import config
import time

def connect_mqtt():
    client = mqtt.Client()
    while True:
        try:
            client.connect(config.SERVER, 1883, 60)
            return client
        except OSError as e:
            time.sleep(5)
