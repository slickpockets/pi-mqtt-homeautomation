from paho.mqtt import client as mqtt_client
import time
from config import config

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(config["CLIENT_ID"])
    client.username_pw_set(config["USERNAME"], config["PASSWORD"])
    client.on_connect = on_connect
    client.connect(config["BROKER"], config["PORT"])
    return client


def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg, topic):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        q.put(msg)

    client.subscribe(topic)
    client.on_message = on_message

# def publish(client):
#     msg_count = 0
#     while True:
#         time.sleep(1)
#         msg = f"messages: {msg_count}"
#         result = client.publish(topic, msg)
#         # result: [0, 1]
#         status = result[0]
#         if status == 0:
#             print(f"Send `{msg}` to topic `{topic}`")
#         else:
#             print(f"Failed to send message to topic {topic}")
#         msg_count += 1


def publish(client=config["CLIENT_ID"], topic, message, interval=10):
    msg_count = 0
    while True:
        time.sleep(interval)
        msg = message
        results = client.publish(topic, message)
        status = results[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        print('message count: {} for {}'.format(msg_count, topic))
