##MQTT broker for home automation
## see outline.txt for full info of implementation

todo:
  - alot

done:
  -  "homeassistant/thermostat/humidity"
  -  "homeassistant/thermostat/tempature"


Thermostat states:
homeassistant/thermostat/mode/state
states:
  - off
  - auto
  - cool
  - fan_only
  - heat   


thermostat commands
 homeassistant/thermostat/mode/set
commands:
  - off
  - auto
  - cool
  - fan_only
  - heat

Temperature Target State:
  topic: homeassistant/thermostat/temperature/state
  states:
  - The currently configured value for the temperature target.


Temperature Target:
  topic: homeassistant/thermostat/temperature/set
  states:
    - Any temperature value between 62 and 82.


Relay States:

off:
  relay_1: off
  relay_2: off
  relay_3: off
  relay_4: off

auto:
  - Depends on current state.

cool:
  relay_1: ON
  relay_2: ON
  relay_3: off
  relay_4: ON

fan_only:
  relay_1: off
  relay_2: ON
  relay_3: off
  relay_4: off

heat:
  relay_1: ON
  relay_2: ON
  relay_3: ON
  relay_4: off
