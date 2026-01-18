# ProIT_WS2526_IoT_Ravi_FinalProject

## IoT-Based Temperature, Humidity & Dew Point Monitoring and Alert System

IoT Project winter semester 2025/26

**Author:** Ravi Kumar Thekare

---

## Project Overview

This project implements a comprehensive IoT environmental monitoring system that measures temperature and humidity in real-time using a DHT22 sensor connected to an ESP32 microcontroller. The system calculates dew point using the Magnus-Tetens formula and sends automated alerts via Telegram when environmental thresholds are exceeded. All data is visualized through a Node-RED dashboard running on a Raspberry Pi.

![System Dashboard](Documentation/images/dashboard.png)

---

## Components

### Hardware
* **Microcontroller:** ESP32 Development Board
* **Sensor:** DHT22 Temperature & Humidity Sensor
* **Processing Unit:** Raspberry Pi 3
* **Power Supply:** USB 5V

### Software
* **Node-Red**
   * Telegram Nodes (node-red-contrib-telegrambot)
   * MQTT Nodes
   * Dashboard Nodes
   * Function Nodes (Dew Point Calculation)
* **Mosquitto MQTT Broker** (Local installation on Raspberry Pi)

---

## Repo Structure

```
.
├── Documentation/
│   ├── images/                 # Project screenshots and diagrams
│   ├── presentation/           # Presentation slides
│   ├── README.md               # Documentation overview
│   ├── setup_guide.md          # Complete installation guide
│   └── dew_point_info.md       # Dew point calculation explained
├── Hardware/
│   ├── ESP32/                  # Hardware docs and wiring
│   └── README.md               # Hardware overview
├── uPython/                    # MicroPython boot and library files
├── Node-RED/
│   ├── README.md               # Node-RED overview
│   └── telegram_alert_flow.json # Complete Node-RED flow
├── RaspberryPi/
│   ├── README.md               # Raspberry Pi overview
│   └── mqtt_setup.md           # Mosquitto broker configuration
├── Tests/
│   └── README.md               # Test procedures
└── README.md
```

---

## Directory Navigation

*   📂 [**Documentation**](Documentation/README.md) - Images, presentations, and guides.
*   📂 [**Hardware**](Hardware/README.md) - Wiring and physical setup.
*   📂 [**uPython**](uPython/README.md) - ESP32 MicroPython firmware.
*   📂 [**Node-RED**](Node-RED/README.md) - Flows and dashboard configuration.
*   📂 [**RaspberryPi**](RaspberryPi/README.md) - Server setup and configuration.
*   📂 [**Tests**](Tests/README.md) - Testing and verification.

---

## System Architecture

The system follows a simple IoT architecture:

```
ESP32 + DHT22  →  MQTT  →  Raspberry Pi (Node-RED)  →  Telegram Bot
   (Sensor)              (Message Broker)   (Processing)      (Alerts)
```

**Data Flow:**
1. ESP32 reads temperature and humidity from DHT22 every 5 seconds
2. Data is published to MQTT topics on Raspberry Pi
3. Node-RED subscribes to MQTT topics and processes data
4. Dew point is calculated using Magnus-Tetens formula
5. Dashboard displays real-time data with charts and gauges
6. When thresholds are exceeded, Telegram alerts are sent


---

## Key Features

✅ **Real-time Environmental Monitoring**
   - Temperature measurement (°C)
   - Humidity measurement (%)
   - Automatic dew point calculation

✅ **Telegram Alert System**
   - Instant notifications when thresholds exceeded
   - Bot command interface (/start, /status, /help)
 

✅ **Interactive Dashboard**
   - Live data visualization with gauges
   - Historical charts showing trends
   - User-friendly Node-Red_UI interface

✅ **Smart Alert Logic**
   - -Smart threshold system prevents alert spam
   - Separate high/low thresholds
   - Configurable temperature and humidity limits

✅ **Self-Hosted Infrastructure**
   - Local MQTT broker on Raspberry Pi
   - No cloud dependency for core functionality
   

---

## ESP32 Firmware & Hardware

The ESP32 microcontroller reads temperature and humidity data from the DHT22 sensor and publishes the values to the MQTT broker running on the Raspberry Pi.

**Development Environment:** Thonny IDE with MicroPython

### 🔌 Hardware Connection

The DHT22 sensor is connected to the ESP32 to provide digital climate readings.

**Wiring Diagram:**
- **DHT22 VCC** (Pin 1)  → ESP32 **3V3**
- **DHT22 DATA** (Pin 2) → ESP32 **GPIO 2**
- **DHT22 GND** (Pin 3)  → ESP32 **GND**

### 📝 Sensor Reading Logic
The system uses the standard `dht` library to interface with the sensor on GPIO 2.

```python
import dht
from machine import Pin

sensor = dht.DHT22(Pin(2))
sensor.measure() 
mytemp = sensor.temperature()
myhumi = sensor.humidity()
```

### 🌐 WiFi Configuration
```python
import network

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('WIFI_SSID', 'WIFI_PASSWORD')
```

### 📡 MQTT Integration
We use the `umqttsimple` library for lightweight communication.

```python
from umqttsimple import MQTTClient
```

#### MQTT Configuration
```python
MQTT_CLIENT_ID = "Ravi"
MQTT_BROKER = "raspi3e26.f4.htw-berlin.de"
MQTT_PORT = 1883
MQTT_TOPIC_TEMP = "ProIT_IoT/Ravi/temp"
MQTT_TOPIC_HUMI = "ProIT_IoT/Ravi/humi"
```

#### Create MQTT Client
```python
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
```

#### Connect to Broker
```python
client.connect()
```

#### Publish Sensor Data
```python
client.publish(MQTT_TOPIC_TEMP, str(mytemp))
client.publish(MQTT_TOPIC_HUMI, str(myhumi))
```

### 🔄 Main Execution Loop
The system reads and publishes sensor data every 30 seconds.
```python
while True:
    sensor.measure()
    mytemp = sensor.temperature()
    myhumi = sensor.humidity()
    
    client.publish(MQTT_TOPIC_TEMP, str(mytemp))
    client.publish(MQTT_TOPIC_HUMI, str(myhumi))
    
    time.sleep(30)  # Wait 30 seconds before next reading
```

---

## Node-Red Flow

The system logic is implemented in Node-RED through a series of interconnected flows. Each flow handles a specific part of the data lifecycle, from MQTT ingestion to Telegram alerting.

### Step 1: MQTT Climate Streams (flow1)
![MQTT Climate Streams](Documentation/images/flow1.png)
**How it works:** Subscribes to MQTT topics from the ESP32 and routes live data to dashboard gauges and historical charts.

### Step 2: Local Data Publication (flow2)
![Publish Local Data](Documentation/images/flow2.png)
**How it works:** Relays local sensor data between brokers to ensure readings are reachable by both the dashboard and external subscribers.

### Step 3: Telegram Alert Sender
![Telegram Sender](Documentation/images/telegrams%20send%20bot.png)
**How it works:** A centralized integration flow that connects all alert logic to the Telegram Bot API.

### Step 4: Temperature Alert Logic (Temp Alert Flow)
![Temperature Alert Flow](Documentation/images/Temprature-alert-flow.png)
**How it works:** Monitors temperature thresholds (High > 25°C, Low < 10°C). Alerts are sent **separately and immediately** to Telegram when a threshold is breached.

### Step 5: Humidity Alert Logic (Humi Alert Flow)
![Humidity Alert Flow](Documentation/images/humi-alert%20%20flow.png)
**How it works:** Monitors humidity thresholds (High > 65%, Low < 30%). Alerts are sent **separately and immediately** as independent messages.

### Step 6: Environmental Analyser (Daily Report Flow)
![Environmental Analysis](Documentation/images/environmental%20analys%20flow-wtih%20delay%20one%20message%20per%20day.png)
**How it works:** Calculates advanced metrics. To prevent clutter, this comprehensive report is scheduled with a delay to be sent **only once per day**.

### Step 7: Real-time Push Notifications (Alert Result)
![Push Alerts](Documentation/images/temp&humi%20alert.png)
**How it works:** The final user experience where instant alerts appear on the mobile device via the Telegram bot.

### Step 8: Comprehensive Environmental Report (Daily)
![Environmental Report](Documentation/images/environmenet%20nalayse%20alert.png)
**How it works:** A detailed snapshot of all calculated metrics delivered once per day to provide a daily environmental summary.


## Acknowledgments

- **Course:** ProIT - IoT Project (WS2526)
- **Institution:** HTW Berlin
- **Semester:** Winter Semester 2025/26

---


