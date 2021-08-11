#!/usr/bin/python3

from paho.mqtt import client as mqtt_client
import smbus
import time

# Get I2C bus
broker = '127.0.0.1'
port = 1883
# generate client ID with pub prefix randomly
client_id = 'subscriber_thermo'
username = 'mqtt'
password = 'mqtt'

        control_topics=["homeassistant/thermostat/temperature/set", "homeassistant/thermostat/mode/state", "homeassistant/thermostat/mode/set", "homeassistant/thermostat/temperature/state"]

def connect_mqtt(client_id, broker, port) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def subscribe2(client: mqtt_client, topics):
    def on message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topics)
    client.on_message = on_message

def publish(client, message, topic):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = str(msg_count) + " " + message
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt("thermo", "127.0.0.1", 1883)
    client.loop_forever()
    client.subscribe(control_topics)


if __name__ == '__main__':
    run()
