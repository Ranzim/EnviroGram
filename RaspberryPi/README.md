# Raspberry Pi Setup & Configuration

This guide covers the initial setup of the Raspberry Pi as the central processing hub and MQTT broker for the environmental monitoring system.

## 🚀 Getting Started

### 1. Connect via SSH
Access your Raspberry Pi from your terminal:
```bash
ssh -Y pi@raspi3e26.f4.htw-berlin.de
```

### 2. Update System Packages
Always start with an updated system:
```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Install Mosquitto MQTT Broker
Install the broker and client tools:
```bash
sudo apt install mosquitto mosquitto-clients -y
```

## ⚙️ Configuration

### 4. Configure Mosquitto
Edit the configuration file to allow connections:
```bash
sudo nano /etc/mosquitto/mosquitto.conf
```

### 5. Add Security & Listener Settings
Add these lines to the configuration file:
```conf
allow_anonymous false
listener 1883
```

### 6. Start & Verify Service
Enable and check the status of the MQTT service:
```bash
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
sudo systemctl status mosquitto
```

## 📊 Node-RED

### 7. Start Node-RED
To launch the Node-RED environment:
```bash
node-red-start
```
Once started, you can access the interface in your browser at:
`http://raspi3e26.f4.htw-berlin.de:1880`
