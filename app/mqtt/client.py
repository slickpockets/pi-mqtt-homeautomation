from paho.mqtt import client as mqtt_client
import time

from dotenv import dotenv_values
config = dotenv_values('.env')


    def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id=config["CLIENT_ID"])
    client.username_pw_set(username=config["USERNAME"], password=config["PASSWORD"])
    client.on_connect = on_connect
    client.connect(config["BROKER"], int(config["PORT"]))
    return client


def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg, topic):
        q.put(msg)

    client.subscribe(topic)
    client.on_message = on_message


def on_message(client, userdata, message):
    while not q.empty():
        message = q.get()
        print("queue: ",message)

def publish(client, topic, message, interval):
    msg_count = 0
    while True:
        time.sleep(interval)
        msg = message
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def pub(client, interval, topic, message):
    msg_count = 0
    while True:
        time.sleep(interval)
        results = client.publish(topic, messa)
        status = results[0]
        if status == 0:
            print(f"Send `{message}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        print('message count: {} for {}'.format(msg_count, topic))
