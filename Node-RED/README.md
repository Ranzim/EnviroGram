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
How it works: Monitors temperature thresholds (High > 10°C, Low < 5°C) and generates formatted alerts using state-management to prevent message spam.

![Temperature Alert Flow](../Documentation/images/Temprature-alert-flow.png)

### 5. Humidity Alert Logic (Humi Alert Flow)
How it works: Similar to temperature monitoring, this triggers alerts for humidity violations (High > 20%, Low < 10%).

![Humidity Alert Flow](../Documentation/images/humi-alert%20%20flow.png)

### 6. Environmental Analysis (Environmental Flow)
How it works: Combines temperature and humidity data to calculate advanced metrics like Dew Point, Absolute Humidity, and Saturation Depression.

![Environmental Analysis](../Documentation/images/Environmenet%20analysis.png)

### 7. Real-time Push Notifications (Alert Result)
How it works: The end-user experience where instant alerts appear on the mobile device from the Telegram bot.

![Push Alerts](../Documentation/images/temp&humi%20alert.png)

### 8. Comprehensive Analysis Report
How it works: Sends a detailed "ENVIRONMENTAL METRICS" report to Telegram, including all calculated values and a precise timestamp.

![Environmental Report](../Documentation/images/environmenet%20nalayse%20alert.png)

- **Metrics Included:**
  - 🌡️ **Temperature**
  - 💧 **Humidity**
  - ❄️ **Dew Point**
  - 📊 **Absolute Humidity**
  - 📉 **Depression**
  - 📍 **Location Info**
- **Timestamping:** Every report includes a precise timestamp of the analysis.
