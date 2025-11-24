import time
import board
import busio
import adafruit_sht31d
from actuators.oled import display_data  # Importar la funcion para mostrar datos en la pantalla OLED

# Configuracion del sensor SHT3x (opcional)
sensor = None
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_sht31d.SHT31D(i2c, address=0x44)  # Especificar la direccion I2C
    print("Sensor SHT3x inicializado correctamente en dirección 0x44")
except Exception as e:
    print(f"Sensor SHT3x no disponible: {e}")
    sensor = None

def read_sht3x():
    try:
        temperature = sensor.temperature
        humidity = sensor.relative_humidity
        return {'temperature': temperature, 'humidity': humidity}
    except:
        return None

def publish_sht3x_data(client, topic):
    if sensor is None:
        print("Sensor SHT3x no disponible, omitiendo publicación")
        return
    
    sensor_data = read_sht3x()
    if sensor_data:
        temperature = round(sensor_data['temperature'], 4)
        humidity = round(sensor_data['humidity'], 4)
        message = '{0},{1}'.format(temperature, humidity).encode('utf-8')
        client.publish(topic, message)
        print(f"SHT3x: T={temperature}°C H={humidity}%")
        display_data(temperature, humidity)
    else:
        print("Error leyendo SHT3x")
