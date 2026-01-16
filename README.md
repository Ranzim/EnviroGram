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
* **Arduino IDE** (ESP32 firmware development)

---

## Repo Structure

```
.
├── Documentation
│   ├── setup_guide.md          # Complete installation guide
│   └── dew_point_info.md       # Dew point calculation explained
├── Hardware
│   └── ESP32
│       └── esp32_dht22.ino     # ESP32 firmware for DHT22 and MQTT
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
7. Users can query status via Telegram bot commands

---

## Key Features

✅ **Real-time Environmental Monitoring**
   - Temperature measurement (°C)
   - Humidity measurement (%)
   - Automatic dew point calculation

✅ **Telegram Alert System**
   - Instant notifications when thresholds exceeded
   - Bot command interface (/start, /status, /help)
   - Customizable alert messages

✅ **Interactive Dashboard**
   - Live data visualization with gauges
   - Historical charts showing trends
   - User-friendly web interface

✅ **Smart Alert Logic**
   - Hysteresis implementation prevents alert spam
   - Separate high/low thresholds
   - Configurable temperature and humidity limits

✅ **Self-Hosted Infrastructure**
   - Local MQTT broker on Raspberry Pi
   - No cloud dependency for core functionality
   - Data privacy and security

---

## ESP32 Firmware

The ESP32 microcontroller reads temperature and humidity data from the DHT22 sensor every 5 seconds and publishes the values to the MQTT broker running on the Raspberry Pi.

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

Optional: 4.7kΩ pull-up resistor between VCC and DATA
```

### DHT22 Sensor Reading

The DHT22 sensor is connected to **GPIO pin 4**:

```cpp
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  dht.begin();
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  if (!isnan(temperature) && !isnan(humidity)) {
    // Publish to MQTT
  }
}
```

### WiFi Connection

```cpp
#include <WiFi.h>

const char* ssid = "YourSSID";
const char* password = "YourPassword";

void setup() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}
```

### MQTT Publishing

```cpp
#include <PubSubClient.h>

const char* mqtt_server = "192.168.1.100";
const char* topic_temp = "home/ravi/temperature";
const char* topic_humi = "home/ravi/humidity";

WiFiClient espClient;
PubSubClient client(espClient);

void publishData(float temp, float humi) {
  client.publish(topic_temp, String(temp).c_str());
  client.publish(topic_humi, String(humi).c_str());
}
```

---

## Node-Red Flow

The Node-RED flow implements the complete monitoring and alert system with the following components:

### (1) Dashboard Visualization

The dashboard displays real-time environmental data with an intuitive interface:

**Features:**
- **Temperature gauge** (0-50°C range)
- **Humidity gauge** (0-100% range)
- **Dew point display** (calculated value)
- **Historical line charts** showing trends over time
- **Current status indicators**
- **Alert notifications**

Access dashboard at: `http://<raspberry-pi-ip>:1880/ui`

### (2) MQTT Subscription

MQTT input nodes subscribe to topics published by ESP32:

**Configuration:**
```
Server: localhost:1883
Username: ravi
Password: (configured)

Topics:
- home/ravi/temperature  (receives temp data)
- home/ravi/humidity     (receives humidity data)

QoS: 1 (at least once delivery)
```

The flow receives sensor data every 5 seconds and processes it for display and alerts.

### (3) Dew Point Calculation

A **function node** calculates the dew point using the **Magnus-Tetens formula**:

**Implementation:**

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

**Formula Explanation:**
- **a = 17.27** (dimensionless constant)
- **b = 237.7°C** (temperature constant)
- **Valid range:** -40°C to +50°C
- **Accuracy:** ±0.4°C under normal conditions

The calculated dew point provides insight into comfort levels and condensation risk.

### (4) Telegram Bot Integration

The system integrates a Telegram bot for remote monitoring and alerts.

**Telegram Receiver Node:**

Listens for incoming commands from users:

```
Supported Commands:
/start  - Initialize bot and get welcome message
/status - Request current sensor readings
/help   - Display available commands
```

**Example Interaction:**
```
User: /status
Bot: 🌡️ Current Climate Status
     Temperature: 23.5°C
     Humidity: 55%
     Dew Point: 14.2°C
     Status: Comfortable
     Last Update: 2026-01-16 22:30:15
```

**Telegram Sender Node:**

Sends automated alerts when thresholds are exceeded:

**Alert Message Format:**

**Alert Message Format:**
```
⚠️ HIGH TEMPERATURE ALERT!
Temperature: 29.5°C
Humidity: 65%
Dew Point: 22.1°C
Time: 2026-01-16 22:45:30

Status: Threshold exceeded
Recommendation: Check room ventilation
```

### (5) Alert System with Hysteresis

To prevent alert spam when values oscillate near thresholds, the system implements **hysteresis logic**.

**How Hysteresis Works:**

Instead of a single threshold, the system uses two values:
- **High threshold** (28°C) - Alert activates when exceeded
- **Low threshold** (26°C) - Alert deactivates when below this value

This creates a 2°C "buffer zone" that prevents rapid on/off toggling.

**Temperature Alert Logic:**

```javascript
var temp = msg.payload.temperature;
var threshold_high = 28;
var threshold_low = 26;

if (temp > threshold_high && !context.get('alertActive')) {
    context.set('alertActive', true);
    msg.payload = "⚠️ High temperature: " + temp + "°C";
    return msg;
} else if (temp < threshold_low && context.get('alertActive')) {
    context.set('alertActive', false);
    msg.payload = "✅ Temperature normal: " + temp + "°C";
    return msg;
}
```

**Benefits of Hysteresis:**
- ✅ Prevents notification fatigue
- ✅ More stable alert system
- ✅ Reduces false alarms
- ✅ Better user experience

**Threshold Configuration:**
```javascript
// Temperature thresholds (°C)
const TEMP_HIGH = 28;  // Alert ON
const TEMP_LOW = 26;   // Alert OFF

// Humidity thresholds (%)
const HUMI_HIGH = 70;  // Alert ON
const HUMI_LOW = 65;   // Alert OFF
```

### (6) Complete System Flow

The final integrated flow combines all components into a seamless monitoring system:

**Flow Sections:**
1. **MQTT Input** → Receives sensor data from ESP32
2. **Data Processing** → Combines temperature and humidity messages
3. **Dew Point Calculation** → Computes dew point value
4. **Dashboard Output** → Displays real-time data with gauges and charts
5. **Threshold Monitoring** → Checks for alert conditions
6. **Telegram Output** → Sends notifications and responds to commands
7. **Debug Nodes** → For troubleshooting and development

---

## Installation & Setup

This section provides step-by-step instructions for setting up the complete system.

### Prerequisites

**Hardware Requirements:**
- ESP32 development board
- DHT22 sensor
- Raspberry Pi 3 (or newer)
- MicroSD card (16GB minimum, Class 10)
- USB cables
- Breadboard and jumper wires

**Software Requirements:**
- Arduino IDE (for ESP32 programming)
- Raspberry Pi OS (Lite or Desktop)
- Internet connection for initial setup

### Step 1: Raspberry Pi Setup

#### 1.1 Install Operating System

```bash
# Download and install Raspberry Pi OS using Raspberry Pi Imager
# https://www.raspberrypi.com/software/

# After first boot, update the system
sudo apt-get update
sudo apt-get upgrade -y
```

#### 1.2 Install Mosquitto MQTT Broker

#### 1.2 Install Mosquitto MQTT Broker

```bash
# Install Mosquitto broker and clients
sudo apt-get install mosquitto mosquitto-clients -y

# Enable Mosquitto to start on boot
sudo systemctl enable mosquitto

# Check status
sudo systemctl status mosquitto
```

**Configure Authentication:**

```bash
# Create password for user 'ravi'
sudo mosquitto_passwd -c /etc/mosquitto/passwd ravi
# Enter password when prompted

# Edit Mosquitto configuration
sudo nano /etc/mosquitto/mosquitto.conf

# Add these lines at the end:
allow_anonymous false
password_file /etc/mosquitto/passwd

# Restart Mosquitto
sudo systemctl restart mosquitto
```

#### 1.3 Install Node-RED
#### 1.3 Install Node-RED

```bash
# Run the official Node-RED installation script
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)

# Answer 'y' to prompts
# This will take 10-15 minutes

# Enable Node-RED to start on boot
sudo systemctl enable nodered

# Start Node-RED
sudo systemctl start nodered

# Check status
sudo systemctl status nodered

# Access Node-RED at: http://<raspberry-pi-ip>:1880
```

#### 1.4 Install Required Node-RED Packages

```bash
# Navigate to Node-RED directory
cd ~/.node-red

# Install dashboard package
npm install node-red-dashboard

# Install Telegram bot package
npm install node-red-contrib-telegrambot

# Restart Node-RED to load new packages
sudo systemctl restart nodered
```

**Verify Installation:**
- Open browser to `http://<raspberry-pi-ip>:1880`
- Check that Node-RED editor loads successfully
- Verify dashboard is available at `http://<raspberry-pi-ip>:1880/ui`

### Step 2: Telegram Bot Setup

#### 2.1 Create Telegram Bot

1. Open Telegram app
2. Search for **@BotFather**
3. Start conversation and send: `/newbot`
4. Follow prompts:
   - Bot name: `Ravi Climate Monitor Bot`
   - Username: `ravi_climate_bot` (must end with 'bot')
5. **Copy the API token** (you'll need this for Node-RED)

Example token format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

#### 2.2 Get Your Chat ID

1. Search for **@userinfobot** on Telegram
2. Start the bot
3. **Copy your Chat ID** (numeric value)

Example Chat ID: `123456789`

### Step 3: ESP32 Setup

#### 3.1 Install Arduino IDE

1. Download from: https://www.arduino.cc/en/software
2. Install for your operating system (Windows/Mac/Linux)

#### 3.2 Add ESP32 Board Support

```
1. Open Arduino IDE
2. Go to: File → Preferences
3. In "Additional Board Manager URLs" add:
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
4. Click OK
5. Go to: Tools → Board → Boards Manager
6. Search: "ESP32"
7. Install: "esp32 by Espressif Systems"
```

#### 3.3 Install Required Libraries

```
Tools → Manage Libraries → Search and Install:

1. "DHT sensor library" by Adafruit
2. "Adafruit Unified Sensor"
3. "PubSubClient" by Nick O'Leary
```

#### 3.4 Configure and Upload Firmware

1. Open `Hardware/ESP32/esp32_dht22.ino` in Arduino IDE
2. **Edit configuration:**

2. **Edit configuration:**
   ```cpp
   const char* ssid = "YourWiFiSSID";           // Your WiFi name
   const char* password = "YourWiFiPassword";   // Your WiFi password
   const char* mqtt_server = "192.168.1.100";   // Your Raspberry Pi IP
   const char* mqtt_user = "ravi";              // MQTT username
   const char* mqtt_password = "password";      // MQTT password
   ```

3. **Connect ESP32 to computer via USB**

4. **Select board and port:**
   ```
   Tools → Board → ESP32 Dev Module
   Tools → Port → (select your ESP32 port)
   ```

5. **Click Upload button** (→ arrow icon)

6. **Open Serial Monitor** (115200 baud) to verify operation

**Expected Serial Output:**
```
WiFi connected
IP Address: 192.168.1.150
Connecting to MQTT...connected
Temp: 23.5°C, Humidity: 55.2%
```

### Step 4: Import Node-RED Flow

#### 4.1 Import Flow File

1. Open Node-RED: `http://<raspberry-pi-ip>:1880`
2. Click **Menu (☰)** in top-right corner
3. Select **Import**
4. Click **select a file to import**
5. Choose `Node-Red/telegram_alert_flow.json`
6. Click **Import**

#### 4.2 Configure MQTT Nodes

1. Double-click any **MQTT input node**
2. Click **pencil icon** next to Server dropdown
3. Configure connection:
   ```
   Server: localhost (or 127.0.0.1)
   Port: 1883
   ```
4. Go to **Security tab**
5. Enter:
   ```
   Username: ravi
   Password: (your MQTT password)
   ```
6. Click **Update**, then **Done**

#### 4.3 Configure Telegram Nodes

**Configure Telegram Receiver:**
1. Double-click **Telegram receiver** node
2. Click **pencil icon** next to Bot dropdown
3. Enter your **Bot Token** (from BotFather)
4. Click **Add**, then **Done**

**Configure Telegram Sender:**
1. Double-click **Telegram sender** node
2. Select your bot from dropdown
3. Enter your **Chat ID** in the node or leave for dynamic sending
4. Click **Done**

#### 4.4 Deploy Flow

1. Click **Deploy** button (top-right corner)
2. Wait for "Successfully deployed" message
3. Check for any error messages in debug panel

### Step 5: Testing

#### 5.1 Test ESP32 Connection

```bash
# On Raspberry Pi, subscribe to MQTT topics
mosquitto_sub -h localhost -t "home/ravi/#" -u ravi -P password

# You should see temperature and humidity values every 5 seconds:
home/ravi/temperature 23.5
home/ravi/humidity 55.2
```

#### 5.2 Test Node-RED Dashboard

1. Open browser: `http://<raspberry-pi-ip>:1880/ui`
2. Verify that gauges display current values
3. Check that charts are being populated
4. Confirm dew point is calculated correctly

#### 5.3 Test Telegram Bot

1. Open Telegram and find your bot
2. Send: `/start`
3. Expected response: Welcome message
4. Send: `/status`
5. Expected response: Current sensor readings

#### 5.4 Test Alert System

**Test temperature alert:**
1. Apply heat near DHT22 sensor (hand, warm air, etc.)
2. Wait for temperature to exceed 28°C
3. Verify alert received on Telegram
4. Let sensor cool down below 26°C
5. Verify "normalized" message received

---

## Dew Point Calculation Explained

### What is Dew Point?

The **dew point** is the temperature at which air becomes saturated with water vapor and condensation begins to form. It's a critical measurement for:

- **Human comfort assessment** - Better than relative humidity alone
- **Condensation prediction** - Prevents mold and moisture damage
- **HVAC optimization** - Improves climate control efficiency
- **Weather forecasting** - Indicates fog and precipitation potential

### Magnus-Tetens Formula

This project uses the Magnus-Tetens approximation, which provides excellent accuracy for typical environmental conditions:

**Formula:**
```
Step 1: Calculate α (alpha)
α = (a × T) / (b + T) + ln(RH/100)

Step 2: Calculate Dew Point (Td)
Td = (b × α) / (a - α)
```

**Parameters:**
- **T** = Temperature in Celsius (°C)
- **RH** = Relative Humidity in percentage (%)
- **Td** = Dew Point in Celsius (°C)
- **a** = 17.27 (empirical constant, dimensionless)
- **b** = 237.7 (empirical constant in °C)
- **ln** = Natural logarithm (base e)

### Why These Constants?

The constants **a = 17.27** and **b = 237.7** are derived from experimental water vapor data and provide:
- **High accuracy:** ±0.4°C for most atmospheric conditions
- **Wide range:** Valid from -40°C to +50°C
- **Computational efficiency:** No complex exponentials needed

### Implementation in Node-RED

The calculation is performed in a JavaScript function node:

```
α = (17.27 × T) / (237.7 + T) + ln(RH/100)
Td = (237.7 × α) / (17.27 - α)
```

### Practical Example

**Given Conditions:**
- Temperature: 25°C
- Humidity: 60%

**Step-by-Step Calculation:**

```
Step 1: Calculate α
α = (17.27 × 25) / (237.7 + 25) + ln(60/100)
α = 431.75 / 262.7 + ln(0.6)
α = 1.644 + (-0.511)
α = 1.133

Step 2: Calculate Td  
Td = (237.7 × 1.133) / (17.27 - 1.133)
Td = 269.32 / 16.137
Td = 16.69°C
```

**Result:** Dew point = **16.7°C** (Comfortable conditions)

### Dew Point Comfort Scale

Understanding what dew point values mean for human comfort:
- < 10°C: Comfortable
- 10-16°C: Acceptable  
- 16-21°C: Uncomfortable
- > 21°C: Very uncomfortable

| Dew Point (°C) | Comfort Level | Description |
|----------------|---------------|-------------|
| < 10°C | Very Comfortable | Dry air, pleasant conditions |
| 10-13°C | Comfortable | Slight humidity, still pleasant |
| 13-16°C | Acceptable | Slightly humid, most people comfortable |
| 16-18°C | Slightly Uncomfortable | Noticeable humidity for some |
| 18-21°C | Uncomfortable | Humid, sticky feeling |
| 21-24°C | Very Uncomfortable | Very humid, oppressive |
| > 24°C | Extremely Uncomfortable | Extremely oppressive conditions |

### Why Dew Point Matters

**Relative Humidity** changes with temperature, making it less reliable:
- 50% RH at 30°C feels very different than 50% RH at 20°C

**Dew Point** is an absolute measure:
- Doesn't change with temperature
- More accurate indicator of comfort
- Better for comparing conditions

---

## Troubleshooting

### Problem 1: ESP32 Not Connecting to WiFi
✅ Verify SSID and password  
✅ Ensure 2.4GHz WiFi (ESP32 doesn't support 5GHz)  
✅ Move closer to router  

### Problem 2: MQTT Connection Failed
✅ Check Raspberry Pi IP address  
✅ Verify Mosquitto is running: `sudo systemctl status mosquitto`  
✅ Test manually: `mosquitto_pub -h localhost -t test -m "hello" -u ravi -P password`  

### Problem 3: DHT22 Returns NaN
✅ Check wiring (VCC, DATA, GND)  
✅ Add 4.7kΩ pull-up resistor  
✅ Increase delay: `delay(2000);`  

### Problem 4: Telegram Bot Not Responding
✅ Verify bot token is correct  
✅ Check Node-RED is deployed  
✅ Restart Node-RED: `sudo systemctl restart nodered`  

### Problem 5: No Alerts Received
✅ Check threshold values (28°C high, 26°C low)  
✅ Verify temperature actually exceeds threshold  
✅ Check debug output in Node-RED  


---

## Acknowledgments

- **Course:** ProIT - IoT Project (WS2526)
- **Institution:** HTW Berlin
- **Semester:** Winter Semester 2025/26

---


