# Zigbee2MQTT Status Check

I have a nice Zigbee2MQTT setup, but I wanted to know when devices went offline. So my idea was to have a simple way to regularly check the status in this way:

For a preselected device (somethinhg that I can turn ON and OFF at any time without major issue) I check first if the device is OFF.
If it's OFF, I try to turn it ON and then I check the status.
If the status is ON, voilà ! Everything is OK. The device is turned OFF again.
If the status is not ON, then there is an issue somewhere. A notification is sent to me, by Whatsapp.
