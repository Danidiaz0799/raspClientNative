import smbus

I2C_PORT = 1
GY302_ADDRESS = 0x23

def read_gy302():
    try:
        bus = smbus.SMBus(I2C_PORT)
        data = bus.read_i2c_block_data(GY302_ADDRESS, 0x10, 2)
        light_level = (data[1] + (256 * data[0])) / 1.2
        return {'light_level': light_level}
    except Exception as e:
        print(f"Error leyendo GY-302: {e}")
        return None

def publish_gy302_data(client, topic):
    sensor_data = read_gy302()
    if sensor_data:
        light_level = round(sensor_data['light_level'], 4)
        message = '{0}'.format(light_level).encode('utf-8')
        client.publish(topic, message)
        print("GY-302:", message.decode(), "Topico:", topic)
    else:
        print("Error al leer los datos del sensor GY-302")

