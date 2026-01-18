# Node-RED Flow Documentation

This folder contains the official Node-RED flow configuration for the IoT Environmental Monitoring system. The flows are organized into several logical steps to handle data ingestion, processing, visualization, and alerting.

## Node-RED Step-by-Step Flow

### 1. MQTT Climate Streams (flow1)
How it works: Subscribes to MQTT topics from the ESP32 and routes live data to dashboard gauges and historical charts.

![MQTT Climate Streams](../Documentation/images/flow1.png)

### 2. Local Data Publication (flow2)
How it works: Relays local sensor data between brokers to ensure readings are reachable by both the dashboard and external subscribers.

![Publish Local Data](../Documentation/images/flow2.png)

### 3. Telegram Alert Base (Send Flow)
How it works: A centralized integration flow that connects all alert logic to the Telegram Bot API.

![Telegram Send Flow](../Documentation/images/telegrams%20send%20bot.png)

### 4. Temperature Alert Logic (Temp Alert Flow)
How it works: Monitors temperature thresholds (High > 25°C, Low < 10°C). Alerts are sent **separately and immediately** to Telegram as soon as a threshold is exceeded.

![Temperature Alert Flow](../Documentation/images/Temprature-alert-flow.png)

### 5. Humidity Alert Logic (Humi Alert Flow)
How it works: Monitors humidity thresholds (High > 65%, Low < 30%). Alerts are sent **separately and immediately** to Telegram when these conditions are met.

![Humidity Alert Flow](../Documentation/images/humi-alert%20%20flow.png)

### 6. Environmental Analyser (Daily Report Flow)
How it works: Advanced analyzer that calculates Dew Point, Absolute Humidity, and Depression. To keep the notification feed clean, this detailed report is scheduled to be sent **only once per day**.

![Environmental Analysis](../Documentation/images/environmental%20analys%20flow-wtih%20delay%20one%20message%20per%20day.png)

### 7. Real-time Push Notifications (Alert Result)
How it works: The end-user experience where instant alerts appear on the mobile device from the Telegram bot.

![Push Alerts](../Documentation/images/temp&humi%20alert.png)

### 8. Comprehensive Daily Analysis Report
How it works: The final summary report delivered once per day. It includes all calculated environmental metrics and precise location metadata.

![Environmental Report](../Documentation/images/environmenet%20nalayse%20alert.png)

- **Metrics Included:**
  - 🌡️ **Temperature**
  - 💧 **Humidity**
  - ❄️ **Dew Point**
  - 📊 **Absolute Humidity**
  - 📉 **Depression**
  - 📍 **Location Info**
- **Timestamping:** Every report includes a precise timestamp of the analysis.
