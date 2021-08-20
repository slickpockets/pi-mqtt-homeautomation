#!/usr/bin/python3
from paho.mqtt import client as mqtt_client
import smbus
import pigpio
#array of gpio pins relays are connecetd to so you can change pins easily
relay_nums = [4,18,23,24]

relays = {"relay_1": relay_nums[0], "relay_2": relay_nums[1], "relay_3": relay_nums[2], "relay_4": relay_nums[3]}
##on / off statements, not certain if its normally open or closed.
OFF = 1
ON = 0

gpio = pigpio.pi()


from dotenv import dotenv_values
config = dotenv_values('.env')


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client("thermo")
    client.username_pw_set("mqtt", "mqtt")
    client.on_connect = on_connect
    client.connect("10.1.10.3", 1883)
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

### gpio.read(#) to read a pins values
## gpio.write(relay, ON/OFF) to acitgate
username = "mqtt"
password = "mqtt"
client = connect_mqtt()

def relaysoff():
    gpio.write(relays["relay_1"], OFF)
    gpio.write(relays["relay_2"], OFF)
    gpio.write(relays["relay_3"], OFF)
    gpio.write(relays["relay_4"], OFF)
    ##need to do error checking and catching
    return('ok')

def relayson():
    gpio.write(relays["relay_1"], ON)
    gpio.write(relays["relay_2"], ON)
    gpio.write(relays["relay_3"], ON)
    gpio.write(relays["relay_4"], ON)
    ##need to do error checking and catching
    return('ok')

def heat_function():
    gpio.write(relays["relay_1"], ON)
    gpio.write(relays["relay_2"], ON)
    gpio.write(relays["relay_3"], ON)
    ##need to do error checking and catching
    return('ok')

def cool_function():
    gpio.write(relays["relay_1"], ON)
    gpio.write(relays["relay_2"], ON)
    gpio.write(relays["relay_4"], ON)
    ##need to do error checking and catching
    return('ok')

def fan_function():
    gpio.write(relays["relay_2"], ON)
    ##need to do error checking and catching
    return('ok')


def lookup_state():
    ## db.get("homeassistant/thermostat/temperature/state")
    pass

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

def state_function(state):
    if state == 'off':
        pass
    elif state == "auto":
        current_temp = get_fTemp()
        thermo_temp = lookup_state()
        if current_temp > thermo_temp:
            cool_function()
        elif current_temp <= thermo_temp:
            heat_function()
        pass
    elif state == "fan_only":
        fan_function()
    elif state == "cool":
        current_temp = get_fTemp()
        thermo_temp = lookup_state()
        if current_temp > thermo_temp:
            cool_function()
        elif current_temp < thermo_temp:
            pass ### all relays off allready
    elif state == "heat":
        current_temp = get_fTemp()
        thermo_temp = lookup_state()
        if current_temp < thermo_temp:
            heat_function()
        elif current_temp >= thermo_temp:
            pass ### all relays off



def process_state(state):
    relayoff()
    client.publish("homeassistant/thermostat/mode/state", state)
    state_function(state)
