# MQTT Configuration
MQTT_BROKER = "192.168.0.137"  # Change this to your broker address
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

# Topics to subscribe to
TOPICS = [
#    "home/sensors/#",     # Example topic - change these to your needed topics
    "zigbee2mqtt/0-plug-xmas"      # Example topic - change these to your needed topics
]

# Client settings
CLIENT_ID = "python_mqtt_client"