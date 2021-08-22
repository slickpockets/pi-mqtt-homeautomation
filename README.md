## in workign order
## raspberrypi mqtt pub/sub thermostat
#### listens for requests to change state from hoem assistant, then changes the working state by executing specific combinations of relay toggles to turn the various
#### utilties on/off : heater, cooler, fan

#### it also publishes the temp and humdidity to the queue and displays on the home assistant
## has special auto mode that will turn the fan or cooler /off the closer it gets to teh ideal temp.
## heater is allways explicitly enabled or disabled.

software used:
paho.mqtt client for python
flask-mqtt to better handle topic specific logic
sht30 libraries for listening to i2c bus for the temp/humidity,


python3 run.py will start up the flask server that publishes and subs to various topics to perform logic to switch on/ff various aspects of enviromental control: fan, heater cooler, off, ato

in the scripts folder asynch.py publishes the temp and humidity to teh mqtt broker for everyone to see. test_async.py does the exact same but with ranodom data, as the temp senosor is currently broken.

Written by Slickpocketsroberts.
the worlds greatest computer programmer and  lover.

if you are reading this, and like what u see, drop me a message to express your admiration.
