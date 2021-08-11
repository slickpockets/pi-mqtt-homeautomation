from app.mqtt import *
from app.sensors import *
from config import config
from queue import Queue

q=Queue()
relays = config["RELAY"]
client = config["CLIENT_ID"]
# humidity = publish(client, topic="homeassistant/thermostat/humidity", message=str(get_humidity()), interval=10)
#
# tempature = publish(client, topic="homeassistant/thermostat/temperature", message=str(get_fTemp(), interval=10))

control_topics=["homeassistant/thermostat/temperature/set", "homeassistant/thermostat/mode/state", "homeassistant/thermostat/mode/set", "homeassistant/thermostat/temperature/state"]





def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client, topic="homeassistant/thermostat/humidity", message=str(get_humidity()), interval=10)
    publish(client, topic="homeassistant/thermostat/temperature", message=str(get_fTemp(), interval=10))
    client.subscribe([("homeassistant/thermostat/temperature/set"),("homeassistant/thermostat/mode/state"), ("homeassistant/thermostat/mode/set"), ("homeassistant/thermostat/temperature/state")])
    #pub_temp(client)
