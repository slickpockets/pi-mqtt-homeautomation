#!/usr/bin/python3

from paho.mqtt import client as mqtt_client
import smbus
import time

# Get I2C bus

{"relay:1": 4, "relay:2": 18, "relay:3": 23, "relay:4": 24}
#also a list
relay = [4,18,23,24]
broker = '127.0.0.1'
port = 1883
# generate client ID with pub prefix randomly
client_id = 'Thermo2'
username = 'mqtt'
password = 'mqtt'

def get_fTemp():
    bus = smbus.SMBus(1)
    bus.write_i2c_block_data(0x45, 0x2C, [0x06])
    time.sleep(0.5)
    data = bus.read_i2c_block_data(0x45, 0x00, 6)
    cTemp = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
    fTemp = cTemp * 1.8 + 32
    return(str(round(fTemp, 2)))

def get_humidity():
    bus = smbus.SMBus(1)
    bus.write_i2c_block_data(0x45, 0x2C, [0x06])
    time.sleep(0.5)
    data = bus.read_i2c_block_data(0x45, 0x00, 6)
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
    return(str(round(humidity, 2)))


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

def publish(client, topic, message):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"message#: {msg_count} message:  {message}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1

def pub(client, topic, message):
    while True:
        time.sleep(1)
        msg = message
        topic = topic
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")



client = connect_mqtt("thermo3", "127.0.0.1", 1883)




thermoset = publish(client, topic="homeassistant/thermostat/mode/state", message="on")
def run():

    client.loop_start()
    thermoset
    time.sleep(1)

if __name__ == "__main__":
    run()
