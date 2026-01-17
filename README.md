# ProIT_WS2526_IoT_Ravi_FinalProject

## IoT-Based Temperature, Humidity & Dew Point Monitoring and Alert System

IoT Project winter semester 2025/26

**Author:** Ravi Kumar Thekare

---

## Project Overview

This project implements a comprehensive IoT environmental monitoring system that measures temperature and humidity in real-time using a DHT22 sensor connected to an ESP32 microcontroller. The system calculates dew point using the Magnus-Tetens formula and sends automated alerts via Telegram when environmental thresholds are exceeded. All data is visualized through a Node-RED dashboard running on a Raspberry Pi.

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
├── Documentation
│   ├── setup_guide.md          # Complete installation guide
│   └── dew_point_info.md       # Dew point calculation explained
├── Hardware
│   └── ESP32
│      
├── Node-Red
│   └── telegram_alert_flow.json # Complete Node-RED flow
├── RaspberryPi
│   └── mqtt_setup.md           # Mosquitto broker configuration
└── README.md
```

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

## ESP32 Firmware

The ESP32 microcontroller reads temperature and humidity data from the DHT22 sensor  and publishes the values to the MQTT broker running on the Raspberry Pi.

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
- DHT22 Pin 2 (DATA) → ESP32 GPIO 4
- DHT22 Pin 3 (GND)  → ESP32 GND
- DHT22 Pin 4        → Not connected

```


## ESP32 Firmware

The ESP32 microcontroller reads temperature and humidity from the DHT22 sensor and publishes to MQTT.

**Development Environment:** Thonny IDE with MicroPython

### Hardware Connection

The DHT22 sensor is connected to **GPIO pin 2**.
```
Connections:
- DHT22 VCC  → ESP32 3V3
- DHT22 DATA → ESP32 GPIO 2
- DHT22 GND  → ESP32 GND
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

In Node-Red I started with MQTT subscription to receive sensor data as shown in (1).

**(1) MQTT Subscription**

![MQTT Subscription](Documentation/images/01_mqtt_subscription.png)

I subscribed to MQTT topics from the ESP32:
- `ProIT_IoT/Ravi/temp` - My temperature data
- `ProIT_IoT/Ravi/humi` - My humidity data

Additionally, I subscribed to the shared ProIT topics to display all students' data:
- `ProIT_IoT/+/temp` - All students' temperature
- `ProIT_IoT/+/humi` - All students' humidity

The data is displayed on the dashboard as shown in (2).

**(2) Dashboard Visualization**

![Dashboard](Documentation/images/02_dashboard.png)

I created a comprehensive dashboard with:

**Left Side - Shared Data:**
- Temperature Data of ProITD (line chart showing all students)
- Humidity Data of ProITD (line chart showing all students)

**Right Side - My Local Data:**
- Local Temperature gauge (showing my ESP32 data)
- Local Humidity gauge (showing my ESP32 data)
- Dew Point calculation display (bottom right section)

In the following session I implemented dew point calculation using a function node (3).

**(3) Dew Point Calculation**

![Dew Point Calculation](Documentation/images/03_dewpoint_calc.png)

I calculated dew point using the Magnus-Tetens formula:
```javascript
var temp = msg.payload.temperature;
var humidity = msg.payload.humidity;

var a = 17.27;
var b = 237.7;

var alpha = ((a * temp) / (b + temp)) + Math.log(humidity/100.0);
var dewPoint = (b * alpha) / (a - alpha);

msg.payload.dewPoint = dewPoint.toFixed(2);
return msg;
```

The calculated dew point is displayed in the bottom-right section of the dashboard.

Then I integrated Telegram bot to receive commands from users (4).

**(4) Telegram Receiver**

![Telegram Receiver](Documentation/images/04_telegram_receiver.png)

I configured the Telegram receiver node to listen for bot commands like `/start` and `/status`.

And I created the message format to send alerts to the bot (5).

**(5) Telegram Sender**

![Telegram Sender](Documentation/images/05_telegram_sender.png)

I set up the Telegram sender node to send formatted alert messages including:
- Current temperature
- Current humidity
- Calculated dew point
- Timestamp

In the following session I added temperature threshold monitoring (6).

**(6) Temperature Alert System**

![Temperature Alerts](Documentation/images/06_temp_alerts.png)

I implemented temperature monitoring with two-level thresholds:

**Threshold values:**
- High temperature: **> 20°C**
- Low temperature: **< 15°C**

The system uses switch nodes to check temperature range and activates alerts when thresholds are exceeded. Formatted messages are sent via Telegram when temperature goes too high or too low.

**(7) Humidity Alert System**

![Humidity Alerts](Documentation/images/07_humidity_alerts.png)

Similarly, I implemented humidity monitoring with threshold checks:

**Threshold values:**
- High humidity: **> 42%**
- Low humidity: **< 30%**

The alerts include dew point information in the Telegram messages.

**(8) Local MQTT Broker**

![MQTT Broker](Documentation/images/08_mqtt_broker.png)

I set up Mosquitto broker at `raspi3e26.f4.htw-berlin.de` to handle all MQTT communication.

**MQTT Topics:**
- `ProIT_IoT/Ravi/temp` - My temperature data
- `ProIT_IoT/Ravi/humi` - My humidity data
- `ProIT_IoT/+/temp` - All students' temperature
- `ProIT_IoT/+/humi` - All students' humidity

**(9) Complete System Flow**

![Complete Flow](Documentation/images/09_complete_flow.png)

The complete system combines MQTT subscription, dashboard visualization, dew point calculation, temperature and humidity alerts, and Telegram bot integration for remote monitoring.

## Acknowledgments

- **Course:** ProIT - IoT Project (WS2526)
- **Institution:** HTW Berlin
- **Semester:** Winter Semester 2025/26

---


