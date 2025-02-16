import paho.mqtt.client as mqtt
import sys
from config import *

def on_connect(client, userdata, flags, rc):
    """Callback function that runs when the client connects to the broker"""
    if rc == 0:
        print("Connected to MQTT Broker!")
        # Subscribe to all topics defined in config
        for topic in TOPICS:
            client.subscribe(topic)
            print(f"Subscribed to {topic}")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    """Callback function that runs when a message is received"""
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

def main():
    # Create MQTT client instance
    client = mqtt.Client(CLIENT_ID)
    
    # Set callback functions
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        # Connect to MQTT broker
        client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        
        # Start the loop
        print("Starting MQTT client...")
        client.loop_forever()
        
    except KeyboardInterrupt:
        print("\nDisconnecting from broker")
        client.disconnect()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 