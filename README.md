# ProIT_WS2526_IoT_Ravi_FinalProject

## IoT-Based Temperature, Humidity & Dew Point Monitoring and Alert System

IoT Project winter semester 2025/26

**Author:** Ravi Kumar Thekare

---

## Project Overview

This project implements a comprehensive IoT environmental monitoring system that measures temperature and humidity in real-time using a DHT22 sensor and ESP32. It calculates advanced metrics like **Dew Point**, **Absolute Humidity**, and **Saturation Depression** via Node-RED, providing automated Telegram alerts and a live glassmorphism dashboard on the Raspberry Pi.

![System Dashboard](Documentation/images/dashboard.png)

---

## Components

### Hardware
* **Microcontroller:** ESP32 Development Board
* **Sensor:** DHT22 Temperature & Humidity Sensor
* **Processing Unit:** Raspberry Pi 
* **Power Supply:** USB 5V

### Software
* **Node-RED Ecosystem**
   * **Telegram Integration:** `telegram-in`, `telegram-out`, `telegram-payload-switch`
   * **Dashboard UI:** `ui_gauge`, `ui_chart` (Line Chart), `ui_template` (Glassmorphism)
   * **MQTT & Logic:** `mqtt-in`, `mqtt-out`, `function`, `switch`, `change`, `link-in`, `link-out`, `string`, `trigger`, `delay`
* **Mosquitto MQTT Broker** (Local installation on Raspberry Pi)

---

## Repo Structure

```
.
├── Documentation/
│   ├── images/                 # Project screenshots and diagrams
│   └── README.md               # Documentation overview
├── Hardware/
│   ├── ESP32/                  # Hardware docs and wiring
│   └── README.md               # Hardware overview
├── uPython/
│   ├── boot.py                 # Main ESP32 logic
│   ├── umqttsimple.py          # MQTT library for MicroPython
│   └── README.md               # firmware overview
├── Node-RED/
│   ├── README.md               # Node-RED overview
│   ├── function-nodes/         # Custom JavaScript logic
│   ├── template-nodes/         # Dashboard UI HTML
│   └── telegram_alert_flow.json # Complete Node-RED flow
├── RaspberryPi/
│   └── README.md               # Raspberry Pi overview & Setup
└── README.md
```

---

## Directory Navigation

*   📂 [**Documentation**](Documentation/README.md) - Images, presentations, and guides.
*   📂 [**Hardware**](Hardware/README.md) - Wiring and physical setup.
*   📂 [**uPython**](uPython/README.md) - ESP32 MicroPython firmware.
*   📂 [**Node-RED**](Node-RED/README.md) - Flows and dashboard configuration.
*   📂 [**RaspberryPi**](RaspberryPi/README.md) - Server setup, MQTT installation, and SSH guides.

---

## System Architecture

The system follows a simple IoT architecture:

```
ESP32 + DHT22  →  MQTT  →  Raspberry Pi (Node-RED)  →  Telegram Bot
   (Sensor)              (Message Broker)   (Processing)      (Alerts)
```

**Data Flow:**
1. **Sensing:** ESP32 reads temperature and humidity from DHT22 every 30 seconds.
2. **Transmission:** Data is published to Mosquitto MQTT topics on the Raspberry Pi.
3. **Ingestion:** Node-RED subscribes to MQTT streams and routes data to UI and processing nodes.
4. **Analysis:** Calculates **Dew Point**, **Absolute Humidity**, and **Saturation Depression**.
5. **Visualization:** Dashboard displays live gauges, historical trends, and complex environmental metrics.
6. **Reporting:** 
   - **Immediate:** Separate alerts sent to Telegram as soon as temp/humi thresholds are breached.
   - **Daily:** A consolidated "Environmental Analysis" report sent once per day.


---

## Key Features

✅ **Real-time Environmental Monitoring**
   - Precise Temperature & Humidity measurement
   - Automated **Dew Point** calculation (Magnus-Tetens)
   - Real-time **Absolute Humidity** & **Saturation Depression** monitoring

✅ **Smart Alerting System**
   - **Immediate Temp Alerts:** High (>25°C) or Low (<10°C) notifications.
   - **Immediate Humi Alerts:** High (>65%) or Low (<30%) notifications.
   - **Scheduled Summary:** Detailed "Environmental Analysis" report delivered **once per day** to prevent spam.
   - **Bot Command Suite:** Control your system via Telegram (/start, /status, /help).

✅ **Interactive Dashboard**
   - Glassmorphism UI (using HTML/CSS templates).
   - Live visual gauges and historical data charting.
   - Mobile-responsive dashboard accessible via the local network.

---

## ESP32 Firmware

The ESP32 microcontroller reads temperature and humidity data from the DHT22 sensor and publishes the values to the MQTT broker running on the Raspberry Pi.

**Development Environment:** Thonny IDE with MicroPython

### Hardware Connection

**DHT22 Wiring to ESP32:**

```
DHT22 Pin Layout:
┌─────────────┐
│  1  2  3  4 │
└─┬──┬──┬──┬──┘
  │  │  │  └── Pin 4: Not Connected
  │  │  └───── Pin 3: GND
  │  └──────── Pin 2: DATA
  └─────────── Pin 1: VCC (3.3V)

Connections:
- DHT22 Pin 1 (VCC)  → ESP32 3V3
- DHT22 Pin 2 (DATA) → ESP32 GPIO 2
- DHT22 Pin 3 (GND)  → ESP32 GND
- DHT22 Pin 4        → Not connected

```

### Sensor Reading

The following lines of code are required to read the sensor values:
```python
import dht
from machine import Pin

sensor = dht.DHT22(Pin(2))
sensor.measure() 
mytemp = sensor.temperature()
myhumi = sensor.humidity()
```

### WiFi Connection

A WiFi connection is established using:
```python
import network

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Rechnernetze', 'rnFIW625')
```

### MQTT Connection

And the connection with the MQTT broker:

#### Import MQTT Library
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

### Main Loop

The system continuously reads sensor data and publishes every 30 seconds:
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
