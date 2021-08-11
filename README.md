##MQTT broker for home automation
## see outline.txt for full info of implementation
# most new work is in gpio.py in working
todo:
  - need to make an entry to store the thermostate state (what its set to between 60-80 to base actions upon) (callback on message/topic to store the value in redis for immediate retrival)
  - integrate it into app
  - use flask_mqtt for ease of use and access to on_topic callbacks.
  -refactor to look pretty


done:
  -  "homeassistant/thermostat/humidity"
  -  "homeassistant/thermostat/tempature"
  - all state change and processing logic done, need ot test on rpi wiht temp sensor.
