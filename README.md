# RaspClientNative

Cliente IoT para Raspberry Pi, especializado en monitoreo y control ambiental en tiempo real. Se integra de forma nativa con el servidor [RaspServer](https://github.com/Danidiaz0799/raspServer) usando MQTT.

[Repositorio en GitHub](https://github.com/Danidiaz0799/raspClientNative)

---

## Características principales

- Control remoto de actuadores: ventilador, luz, humidificador y motor (GPIO).
- Lectura periódica de sensores I2C (ejemplo: SHT3x).
- Publicación automática de datos ambientales vía MQTT.
- Visualización local en pantalla OLED.
- Reconexión automática de Wi-Fi y MQTT.

---

## Arquitectura y flujo de integración

| Componente          | Función principal                                           |
|---------------------|------------------------------------------------------------|
| Sensores I2C        | Lectura de temperatura, humedad, etc.                      |
| Actuadores GPIO     | Control de dispositivos físicos (ventilador, luz, etc.)    |
| Pantalla OLED       | Visualización local de datos y mensajes                    |
| boot.py             | Orquestador: integra sensores, actuadores y comunicación   |
| Broker MQTT         | Intermediario de mensajes entre cliente y servidor         |
| RaspServer          | Backend central: almacena datos, envía comandos, expone API|
| Base de datos       | Almacenamiento histórico de mediciones y eventos           |
| API REST            | Gestión y visualización de datos (frontend externo)        |

**Flujo resumido:**
1. El cliente lee sensores y publica datos en tópicos MQTT.
2. El servidor central (RaspServer) recibe datos, almacena y puede enviar comandos de control.
3. Los comandos viajan por MQTT y son ejecutados por el cliente en los actuadores.
4. Toda la comunicación es asíncrona y bidireccional vía MQTT.

---

## Integración con RaspServer
- El servidor [RaspServer](https://github.com/Danidiaz0799/raspServer) centraliza los datos y gestiona la lógica de control.
- Comunicación bidireccional: el servidor puede enviar comandos a los actuadores del cliente.
- Los datos históricos quedan almacenados en la base de datos del servidor.

---

## Dependencias principales

- `Adafruit-Blinka`, `adafruit-circuitpython-*`, `RPi.GPIO`, `smbus`, `spidev`: Acceso a hardware y sensores I2C/SPI.
- `paho-mqtt`: Comunicación MQTT.
- `pillow`: Visualización en OLED.

Consulta las versiones exactas en el archivo `requirements.txt`.

---

## ¿Cómo funciona?

1. **Conexión Wi-Fi:** El cliente intenta conectarse a una red Wi-Fi usando las credenciales configuradas.
2. **Conexión MQTT:** Una vez conectado a la red, establece conexión con un broker MQTT especificado en la configuración.
3. **Registro:** El cliente se registra en el servidor publicando su `CLIENT_ID`.
4. **Subscripción y Control:** Se suscribe a tópicos específicos para recibir comandos de control de actuadores.
5. **Lectura y Publicación de Sensores:** Lee periódicamente los valores de los sensores y los publica en tópicos MQTT.
6. **Visualización:** Muestra información ambiental y mensajes en la pantalla OLED.

## Arquitectura y Estructura del Proyecto

```
raspClientNative/
├── actuators/           # Control de actuadores (fan, light, humidifier, motor, oled)
├── sensors/             # Lectura de sensores (sht3x, bmp280, etc.)
├── config/              # Configuración Wi-Fi, MQTT y parámetros globales
├── boot.py              # Script principal de arranque de la aplicación
├── requirements.txt     # Dependencias Python
└── projectClient.service# Servicio systemd para ejecución automática
```

### Principales módulos:
- **actuators/**: Control de hardware (GPIO) para ventilador, luz, humidificador, motor y pantalla OLED.
- **sensors/**: Lectura de sensores ambientales (temperatura, humedad, presión, luz, etc.).
- **config/**: Parámetros de conexión (Wi-Fi, MQTT, tópicos, credenciales, etc.).
- **boot.py**: Orquestación general del flujo de la aplicación.

## Conexión al Servidor

- **Wi-Fi:** Utiliza `nmcli` para conectarse a la red definida en `config/wifi_config.py`.
- **MQTT:** Se conecta al broker MQTT definido en `config/mqtt_config.py` usando la librería `paho-mqtt`.
- **Tópicos:**
  - Registro: `config.TOPIC_REGISTER`
  - Control: `config.TOPIC_LIGHT`, `config.TOPIC_FAN`, `config.TOPIC_HUMIDIFIER`, `config.TOPIC_MOTOR`
  - Sensores: `config.TOPIC_SHT3X`, etc.
- **Mensajes:**
  - Los comandos de actuadores se reciben como cadenas (`'true'` o `'false'`).
  - Los datos de sensores se publican como cadenas separadas por coma (ej. `23.5,45.7`).

## Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/Danidiaz0799/raspClientNative
cd raspClientNative
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar Wi-Fi y MQTT
Editar los archivos en `config/` para establecer SSID, contraseña, broker MQTT, tópicos, etc.

### 4. Ejecutar la aplicación manualmente
```bash
python3 boot.py
```

### 5. (Opcional) Instalar como servicio systemd
Para ejecución automática al arrancar:
- Copiar `projectClient.service` a `/etc/systemd/system/`
- Habilitar y arrancar el servicio:
```bash
sudo systemctl enable projectClient.service
sudo systemctl start projectClient.service
```
