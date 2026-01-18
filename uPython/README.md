# uPython
This folder contains the MicroPython firmware for the ESP32 Weather Station.

## Contents
- `boot.py`: Main application logic for WiFi, MQTT, and sensor reading.
- `umqttsimple.py`: Mini MQTT client library for MicroPython.

## Usage
Upload both files to your ESP32 using Thonny or `ampy`. The ESP32 will automatically run `boot.py` on startup.

## Node-RED Integration
The data published by this firmware is processed and visualized in Node-RED. For a detailed breakdown of the flows, see the [Node-RED Documentation](../Node-RED/README.md).

