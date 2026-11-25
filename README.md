# Fog-Based Smart Campus Monitoring System

A middle-level IoT + Fog Computing project that monitors campus environmental conditions and performs decisions locally at a Fog Node before storing or forwarding information.

## Architecture

ESP32 Sensors → MQTT → Raspberry Pi Fog Node → Local Processing → Database / Cloud Dashboard

## Features

- Temperature and humidity monitoring
- PIR-based occupancy detection
- Air-quality monitoring using MQ-135
- MQTT communication
- Local fog processing
- Rule-based anomaly detection
- Immediate local decision making
- SQLite storage at the fog layer
- Web dashboard
- Reduced dependency on cloud processing

## Hardware

- ESP32
- DHT11 or DHT22
- PIR sensor
- MQ-135
- Raspberry Pi (Fog Node)
- Optional buzzer/relay for physical alerts

## Software

- Arduino IDE
- Python 3
- Eclipse Mosquitto MQTT broker
- SQLite
- HTML/CSS/JavaScript

## Setup

### 1. MQTT broker

Install Mosquitto on the Raspberry Pi and start it:

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable --now mosquitto
```

### 2. Fog node

```bash
cd fog_node
python3 -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
python main.py
```

Set another MQTT broker with:

```bash
export MQTT_BROKER=192.168.1.100
python main.py
```

### 3. ESP32

Open `esp32/sensor_code.ino` in Arduino IDE.

Install:
- DHT sensor library
- PubSubClient

Change Wi-Fi and MQTT settings:

```cpp
const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASSWORD = "YOUR_PASSWORD";
const char* MQTT_SERVER = "192.168.1.100";
```

Upload to the ESP32.

### 4. Dashboard

Open `dashboard/index.html` in a browser. The included dashboard uses demonstration values; connect it to an API/Firebase endpoint for live cloud data.

## Fog Computing Demonstration

The key concept is that sensor data is processed at the Raspberry Pi Fog Node instead of sending every raw reading directly to the cloud.

Example:

- Temperature > 30°C → ventilation decision
- Air quality > 700 → alarm decision
- Motion detected → occupancy event

This provides lower latency and allows local decisions even when cloud connectivity is unavailable.

## Future Enhancements

- Firebase/cloud synchronization
- Live WebSocket dashboard
- Email/SMS alerts
- Machine-learning anomaly detection
- Multiple classrooms/fog nodes
- Energy consumption analytics
- Docker deployment

## License

Educational project for college use.
