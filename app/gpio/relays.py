import pigpio
#array of gpio pins relays are connecetd to so you can change pins easily
relay_nums = [4,18,23,24]
relays = {"relay_1": relay_nums[0], "relay_2": relay_nums[1], "relay_3": relay_nums[2], "relay_4": relay_nums[3]}
##on / off statements, not certain if its normally open or closed.
OFF = 1
ON = 0
from app.mqtt.client import client 

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


### state funciton handles logic involved in whcih switches to tun on/off
## on off values can be swtiched at top of screen
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
    state_function(state)
    client.publish("homeassistant/thermostat/mode/state", state)
