#!/usr/bin/python3

from paho.mqtt import client as mqtt_client
import smbus
import time

# Get I2C bus

{"relay:1": 4, "relay:2": 18, "relay:3": 23, "relay:4": 24}
#also a list
relay = [4,18,23,24]
broker = '10.1.10.3'
port = 1883
topic = 'sink'
# generate client ID with pub prefix randomly
client_id = 'Thermo'
username = 'mqtt'
password = 'mqtt'

controller ={
    "ac":
     {
     "name":"ac",
     "state_topic": "homeassistant/thermostat/ac/state",
     "command_topic": "homeassistant/thermostat/ac/set",
     "availability_topic": "homeassistant/thermostat/available"},
     "fan":
     {
     "name": "fan",
     "state_topic": "homeassistant/thermostat/fan/state",
     "command_topic": "homeassistant/thermostat/fan/set",
     "availability_topic": "homeassistant/thermostat/available"
     },
     "heater":
    {
     "name": "heater",
     "state_topic": "homeassistant/thermostat/heater/state",
     "command_topic": "homeassistant/thermostat/heater/set",
     "availability_topic": "homeassistant/thermostat/available"
     },
     "temp":
     {
     "name": "Temp"
     }
}

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


def getsht():
    bus = smbus.SMBus(1)

    # SHT30 address, 0x44(68)
    # Send measurement command, 0x2C(44)
    #		0x06(06)	High repeatability measurement
    bus.write_i2c_block_data(0x45, 0x2C, [0x06])

    time.sleep(0.5)

    # SHT30 address, 0x44(68)
    # Read data back from 0x00(00), 6 bytes
    # cTemp MSB, cTemp LSB, cTemp CRC, Humididty MSB, Humidity LSB, Humidity CRC
    data = bus.read_i2c_block_data(0x45, 0x00, 6)
    cTemp = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
    fTemp = cTemp * 1.8 + 32
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

    return("%.2f" %humidity,
     "%.2f" %fTemp,
    )



def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1

async def pub_temp(client):
    msg_count = 0
    while True:
        await asyncio.sleep(15)
        msg = str(get_fTemp())
        topic = "homeassistant/thermostat/temperature"
        await result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


async def pub_hum(client):
    msg_count = 0
    while True:
        await asyncio.sleep(15)
        msg = str(get_humidity())
            topic = "homeassistant/thermostat/humidity"
        await result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    pub_temp(client)
    pub_hum(client)
    #pub_temp(client)



if __name__ == '__main__':
    run()
