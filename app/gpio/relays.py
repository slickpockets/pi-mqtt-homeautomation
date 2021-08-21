import pigpio
from app import db
#array of gpio pins relays are connecetd to so you can change pins easily
relay_nums = [4,18,23,24]
relays = {"relay_1": relay_nums[0], "relay_2": relay_nums[1], "relay_3": relay_nums[2], "relay_4": relay_nums[3]}
##on / off statements, not certain if its normally open or closed.
OFF = 1
ON = 0
from dotenv import dotenv_values
config = dotenv_values('.env')
import pigpio

gpio = pigpio.pi()

# from app.mqtt.client import client
from app.mqtt.client import connect_mqtt
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

def temp_state_lookup():
    return(db.get("homeassistant/thermostat/temperature/state"))

def mode_state_lookup():
    return(db.get("homeassistant/thermostat/mode/state"))

### state funciton handles logic involved in whcih switches to tun on/off
## on off values can be swtiched at top of screen
def state_function(state):
    if state == 'off':
        relaysoff()
        ###automatic is my magnum opus, it subscribes to the tempature to constatnly change itself dynamically
        ## when the desired temp is > 110% of the the current temp, then it will turn the cool funciton on
        #else when it closes that gap, it goes to fans
    elif state == "auto":
        client.subscribe("homeassistant/thermostat/temperature")
        current_temp = int(get_fTemp())
        thermo_temp = int(temp_state_lookup())
        if current_temp  > (thermo_temp*1.1):
            relaysoff()
            cool_function()
            client.publish("homeassistant/thermostat/mode/state", "cool")
        elif current_temp > thermo_temp:
            relaysoff()
            fan_function()
            client.publish("homeassistant/thermostat/mode/state", "cool")
        else:
            pass ## no heat unless its explicit
    elif state == "fan_only":
        relaysoff()
        fan_function()
        client.publish("homeassistant/thermostat/mode/state", "fan_only")
    elif state == "cool":
        relaysoff()
        cool_function()
        client.publish("homeassistant/thermostat/mode/state", "cool")
    elif state == "heat":
        relaysoff()
        heat_funciton()
        client.publish("homeassistant/thermostat/mode/state", "heat")

def temptature_set(value):
    client.publish("homeassistant/thermostat/temperature/state", value)
    if int(value *1.1) <  get_fTemp():
        relaysoff()
        cool_function()
        client.publish("homeassistant/thermostat/mode/state", "cool")
    elif int(value) < get_fTemp():
        relaysoff()
        fan_function()
        client.publish("homeassistant/thermostat/mode/state", "fan_only")
    else:
        pass

def temp_check(value):
    while mode_state_lookup() == "auto":
        if value+10 < get_fTemp():
            relaysoff()
            cool_function()
            client.publish("homeassistant/thermostat/mode/state", "cool")
        elif int(value) < get_fTemp():
            relaysoff()
            fan_function()
            client.publish("homeassistant/thermostat/mode/state", "fan_only")
        else:
            pass
