# RaspClientNative

RaspClientNative es una aplicación desarrollada para ejecutarse en una Raspberry Pi y controlar y monitorear dispositivos IoT (Internet of Things) a través de comunicación MQTT. El cliente se conecta a una red Wi-Fi, se comunica con un servidor MQTT (broker) y permite el control de actuadores y la lectura de sensores ambientales, mostrando información relevante en una pantalla OLED.

## Tabla de Contenidos
- [¿Para qué sirve?](#para-que-sirve)
- [¿Cómo funciona?](#como-funciona)
- [Arquitectura y Estructura del Proyecto](#arquitectura-y-estructura-del-proyecto)
- [Conexión al Servidor](#conexion-al-servidor)
- [Instalación y Ejecución](#instalacion-y-ejecucion)
- [Dependencias](#dependencias)
- [Autores](#autores)

---

## ¿Para qué sirve?

RaspClientNative está diseñado para integrarse en sistemas de automatización y monitoreo ambiental, permitiendo:
- Controlar actuadores (ventilador, luz, humidificador, motor) de forma remota mediante mensajes MQTT.
- Medir temperatura y humedad ambiental usando sensores (ej. SHT3x, BMP280, etc.).
- Publicar periódicamente los datos de los sensores al servidor MQTT.
- Mostrar información y mensajes en una pantalla OLED conectada a la Raspberry Pi.

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
git clone <repo_url>
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

## Dependencias
Principales librerías usadas (ver `requirements.txt`):
- paho-mqtt
- RPi.GPIO
- Adafruit CircuitPython (sensores, pantalla)
- luma.core, pillow (pantalla OLED)
- nmcli (gestión de Wi-Fi)

## Autores
- Proyecto desarrollado por [Tu Nombre o Equipo]

---

## Notas adicionales
- El sistema está diseñado para ejecutarse en Raspberry Pi con Raspbian.
- Asegúrate de tener habilitado I2C y acceso a GPIO.
- Personaliza los pines y parámetros en los scripts según tu hardware.

---

# Licencia
[Indica aquí la licencia de tu proyecto si aplica]
