# Configuracion de la red Wi-Fi
SSID = 'Stev7'
PASSWORD = 'hola12345'

CLIENT_ID = 'mushroom1'
CLIENT_NAME = 'Cultivo Champiñones Principal'
CLIENT_DESCRIPTION = 'Sistema automatizado de cultivo de hongos - Raspberry Pi 3b'

SERVER = '172.16.132.223'

TOPIC_PREFIX = f'clients/{CLIENT_ID}/'
TOPIC_REGISTER = f'{TOPIC_PREFIX}register'
TOPIC_FAN = f'{TOPIC_PREFIX}fan'
TOPIC_LIGHT = f'{TOPIC_PREFIX}light'
TOPIC_HUMIDIFIER = f'{TOPIC_PREFIX}humidifier'
TOPIC_MOTOR = f'{TOPIC_PREFIX}motor'
TOPIC_SHT3X = f'{TOPIC_PREFIX}sensor/sht3x'
TOPIC_BMP280 = f'{TOPIC_PREFIX}sensor/bmp280'
TOPIC_GY302 = f'{TOPIC_PREFIX}sensor/gy302'

