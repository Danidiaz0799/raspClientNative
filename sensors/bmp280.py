import board
import busio
import adafruit_bmp280

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

def read_bmp280():
    try:
        temperature = sensor.temperature
        pressure = sensor.pressure
        return {'temperature': temperature, 'pressure': pressure}
    except Exception as e:
        print(f"Error leyendo BMP280: {e}")
        return None

def publish_bmp280_data(client, topic):
    sensor_data = read_bmp280()
    if sensor_data:
        temp = round(sensor_data['temperature'], 4)
        pressure = round(sensor_data['pressure'], 4)
        message = '{0},{1}'.format(temp, pressure).encode('utf-8')
        client.publish(topic, message)
        print("BMP280:", message.decode(), "Topico:", topic)
    else:
        print("Error al leer los datos del sensor BMP280")

