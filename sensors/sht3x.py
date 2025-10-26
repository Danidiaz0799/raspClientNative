import time
import board
import busio
import adafruit_sht31d
from actuators.oled import display_data

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_sht31d.SHT31D(i2c, address=0x44)

def read_sht3x():
    try:
        temperature = sensor.temperature
        humidity = sensor.relative_humidity
        return {'temperature': temperature, 'humidity': humidity}
    except Exception as e:
        print(f"Error leyendo SHT3x: {e}")
        return None

def publish_sht3x_data(client, topic):
    sensor_data = read_sht3x()
    if sensor_data:
        temperature = round(sensor_data['temperature'], 4)
        humidity = round(sensor_data['humidity'], 4)
        message = '{0},{1}'.format(temperature, humidity).encode('utf-8')
        client.publish(topic, message)
        print("SHT3x:", message.decode(), "Topico:", topic)
        display_data(temperature, humidity)
    else:
        print("Error al leer los datos del sensor SHT3x")

