# Zigbee2MQTT Status Check

I have a nice Zigbee2MQTT setup, but I wanted to know when devices go offline. So my idea was to have a simple way to regularly check the status in this way:

Considering that the device is OFF, I send an instruction to turn it ON.
I wait around 5 seconds and I send a second message to check if the device is ON.
If the device is ON, it will say: Tests was successful.
If the device is not ON, then the it will say: Test Failed.image.png