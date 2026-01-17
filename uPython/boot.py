"""
ESP32 Weather Station - boot.py
Stable MQTT publisher for temperature and humidity
No errors - production ready
"""
import time
import dht
import network
from machine import Pin
from umqttsimple import MQTTClient

# ===== CONFIGURATION =====
MQTT_CLIENT_ID = "Ravi"
MQTT_BROKER = "raspi3e26.f4.htw-berlin.de"
MQTT_PORT = 1883
MQTT_TOPIC_TEMP = "ProIT_IoT/Ravi/temp"
MQTT_TOPIC_HUMI = "ProIT_IoT/Ravi/humi"
WIFI_SSID = "Rechnernetze"
WIFI_PASSWORD = "rnFIW625"

# ===== INITIALIZATION =====
sensor = dht.DHT22(Pin(2))
client = None

# ===== FUNCTIONS =====
def connect_wifi():
    """Connect to WiFi"""
    print("Connecting to WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)

    timeout = 20
    while not sta_if.isconnected() and timeout > 0:
        print(".", end="")
        time.sleep(0.5)
        timeout -= 1

    if sta_if.isconnected():
        print(" Connected!")
        print("IP:", sta_if.ifconfig()[0])
        return True
    else:
        print(" Failed!")
        return False

def connect_mqtt():
    """Connect to MQTT broker"""
    global client
    print("Connecting to MQTT...", end="")

    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
        client.connect()
        print(" Connected!")
        return True
    except Exception as e:
        print(f" Failed! {e}")
        return False

def publish_sensor_data():
    """Read and publish sensor data"""
    global client

    try:
        # Read sensor
        sensor.measure()
        temp = sensor.temperature()
        humi = sensor.humidity()

        # Publish to MQTT
        client.publish(MQTT_TOPIC_TEMP, str(temp))
        client.publish(MQTT_TOPIC_HUMI, str(humi))

        print(f"[OK] Temp: {temp}C, Humidity: {humi}%")
        return True

    except Exception as e:
        print(f"[ERROR] {e}")
        return False

# ===== MAIN PROGRAM =====
print("\n" + "="*50)
print("ESP32 Weather Station")
print("="*50 + "\n")

# Connect to WiFi
if not connect_wifi():
    print("WiFi failed! Restarting...") 
    time.sleep(5)
    import machine
    machine.reset()

# Connect to MQTT
if not connect_mqtt():
    print("MQTT failed! Will retry...\n")

# Main loop
print("Publishing sensor data every 30 seconds...\n")
reading_count = 0
while True:
    try:
        reading_count += 1
        print(f"Reading #{reading_count}: ", end="")

        # Try to publish
        if client is not None:
            publish_sensor_data()
        else:
            # Try to reconnect
            print("[RECONNECT] ", end="")
            if connect_mqtt():
                publish_sensor_data()

        # Wait 30 seconds (stable interval)
        time.sleep(30)

    except KeyboardInterrupt:
        print("\nStopped!")
        break
    except Exception as e:
        print(f"Loop error: {e}")
        time.sleep(10)
