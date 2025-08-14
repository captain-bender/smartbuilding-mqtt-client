# controller.py
import paho.mqtt.client as mqtt
import time
import json

BROKER_HOSTNAME = "localhost"
BROKER_PORT = 1883
CONTROLLER_STATUS_TOPIC = "smartbuilding/controllers/hvac/status"

lwt_payload = json.dumps({"status": "offline", "reason": "lost_connection"})

# Using the modern V2 client constructor
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "hvac_controller_client_with_lwt")
client.will_set(CONTROLLER_STATUS_TOPIC, payload=lwt_payload, qos=1, retain=True)

client.connect(BROKER_HOSTNAME, BROKER_PORT, 60)
client.loop_start()

online_payload = json.dumps({"status": "online"})
print(f"Publishing 'online' status to {CONTROLLER_STATUS_TOPIC} with retain=True")
client.publish(CONTROLLER_STATUS_TOPIC, payload=online_payload, qos=1, retain=True)

print("\nController is now online.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nClean shutdown.")
    client.loop_stop()
    client.disconnect()