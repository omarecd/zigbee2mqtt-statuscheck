import paho.mqtt.client as mqtt
import sys
import time
from config import *

# Global variable to track device state
device_state = None

def on_connect(client, userdata, flags, rc):
    """Callback function that runs when the client connects to the broker"""
    if rc == 0:
        print("Connected to MQTT Broker!")
        # Subscribe to all relevant device topics
        client.subscribe("zigbee2mqtt/0-plug-xmas")      # Device state topic
        client.subscribe("zigbee2mqtt/0-plug-xmas/set")  # Commands topic
        client.subscribe("zigbee2mqtt/0-plug-xmas/get")  # Get state topic
        print("Subscribed to all device topics")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    """Callback function that runs when a message is received"""
    global device_state
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
    
    if msg.topic == "zigbee2mqtt/0-plug-xmas":
        state = msg.payload.decode()
        if '"state":"ON"' in state:
            device_state = "ON"
        elif '"state":"OFF"' in state:
            device_state = "OFF"

def run_status_check():
    # Create MQTT client instance
    client = mqtt.Client(CLIENT_ID)
    
    # Set callback functions
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        # Connect to MQTT broker
        client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        
        # Start the loop in background
        client.loop_start()
        
        # Wait for connection to establish
        time.sleep(2)
        
        # Step 1: Send ON command
        print("\nStep 1: Sending ON command...")
        client.publish("zigbee2mqtt/0-plug-xmas/set", '{"state":"ON"}')
        
        # Wait for response
        time.sleep(5)
        
        # Step 2: Check if device responded
        print("\nStep 2: Checking device state...")
        client.publish("zigbee2mqtt/0-plug-xmas/get", '{"state":""}')
        
        # Wait for response
        time.sleep(5)
        
        # Final check
        if device_state == "ON":
            print("\n✅ Test SUCCESSFUL: Device is ON as expected!")
        else:
            print("\n❌ Test FAILED: Device did not turn ON!")
        
        # Clean disconnect
        client.loop_stop()
        client.disconnect()
        
    except KeyboardInterrupt:
        print("\nDisconnecting from broker")
        client.loop_stop()
        client.disconnect()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        client.loop_stop()
        client.disconnect()
        sys.exit(1)

if __name__ == "__main__":
    run_status_check() 