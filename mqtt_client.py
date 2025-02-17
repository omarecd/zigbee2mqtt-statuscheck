import paho.mqtt.client as mqtt
import time
import requests
from config import CLIENT_ID, MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE
from notification_secrets import PHONE_NUMBER, API_KEY


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
    #print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
    
    if msg.topic == "zigbee2mqtt/0-plug-xmas":
        state = msg.payload.decode()
        if '"state":"ON"' in state:
            device_state = "ON"
        elif '"state":"OFF"' in state:
            device_state = "OFF"


def send_failure_notification():
    """Send a GET request to notify failure"""
    #API_URL = "https://api.callmebot.com/whatsapp.php?phone=+32495389695&text=Zigbee+devices+are+presenting+a+problem&apikey=828428"  # Replace with your actual API URL
    API_URL = f"https://api.callmebot.com/whatsapp.php?phone=+{PHONE_NUMBER}&text=Zigbee+devices+are+presenting+a+problem&apikey={API_KEY}"
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            print("Notification sent successfully!")
    except Exception as e:
        print(f"❌ Error sending notification: {e}")


def main():
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
        time.sleep(3)
        

        print("\nStep 0: Checking device state...")
        client.publish("zigbee2mqtt/0-plug-xmas/get", '{"state":""}')
        time.sleep(3)


        # Final check
        if device_state == "ON":
            print("\nThe device is being used now, the test is not possible")

        else:
            print("\nThe device is not being used. Proceeding with test")

            # Step 1: Send ON command
            print("\nStep 1: Sending ON command...")
            client.publish("zigbee2mqtt/0-plug-xmas/set", '{"state":"ON"}')
            time.sleep(3)


            # Step 2: Check if device responded
            print("\nStep 2: Checking device state...")
            client.publish("zigbee2mqtt/0-plug-xmas/get", '{"state":""}')
            time.sleep(3)


            # Final check
            if device_state == "ON":
                print("\n✅ Test SUCCESSFUL: Device turned ON as expected!")
                print("\nTurning OFF the device and finishing test")
                client.publish("zigbee2mqtt/0-plug-xmas/set", '{"state":"OFF"}')


            else:
                print("\n❌ Test FAILED: Device did not turn ON!")
                send_failure_notification()
        
        # Clean disconnect
        client.loop_stop()
        client.disconnect()
        
    except KeyboardInterrupt:
        print("\nDisconnecting from broker")
        client.loop_stop()
        client.disconnect()
        return
    except Exception as e:
        print(f"Error: {e}")
        client.loop_stop()
        client.disconnect()
        return

if __name__ == "__main__":
    main()