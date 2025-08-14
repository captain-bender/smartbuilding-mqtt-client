# monitor.py
import paho.mqtt.client as mqtt
import json

BROKER_HOSTNAME = "localhost"
BROKER_PORT = 1883

# The V2 on_connect callback includes a 'properties' argument
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # We only subscribe on a successful connection.
        print("Connected to MQTT Broker!")
        client.subscribe("smartbuilding/#")

def on_message(client, userdata, msg):
    print(f"Received message on topic '{msg.topic}': {msg.payload.decode()}")

# Using the modern V2 client constructor
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "building_monitor_client")
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_HOSTNAME, BROKER_PORT, 60)
client.loop_forever()