import flask
from flask import render_template, Blueprint, request, jsonify, make_response, Response, url_for
from app import db, mqtt
from app.gpio import *
import json
import os
from os.path import join, dirname, realpath
import time
default = Blueprint("default", __name__)

publish_topics=["homeassistant/thermostat/mode/state", "homeassistant/thermostat/temperature/state", "homeassistant/thermostat/temperature", "homeassistant/thermostat/humidity" ]
control_topics=["homeassistant/thermostat/mode/set", "homeassistant/thermostat/temperature/set", 'homeassistant/thermostat/temperature']

for i in control_topics:
    mqtt.subscribe(i, 1)

@mqtt.on_publish()
def handle_publish(client, userdata, mid):
    print('Published message with mid {}.'
          .format(mid))

@mqtt.on_subscribe()
def handle_subscribe(client, userdata, mid, granted_qos):
    print('Subscription id {} granted with qos {}.'
          .format(mid, granted_qos))



@mqtt.on_topic('homeassistant/thermostat/mode/set')
def handle_mode(client, userdata, message):
    timeout = db.get("timeout")
    currently = int(time.time())
    topic = "homeassistant/thermostat/mode/state"
    msg = message.payload.decode()
    print("topic: {} message {}".format(message.topic, msg))
    if msg in ["off", "auto", "cool", "fan_only", "heat"]:
        if currently - timeout < 30 and msg != "off":
            pass
        else:
            db.set(topic, msg)
            db.set("timeout", currently)
            state_function(msg)



@mqtt.on_topic('homeassistant/thermostat/temperature/set')
def handle_temp_set(client, userdata, message):
    msg = message.payload.decode()
    print("topic: {} message {}".format(message.topic, msg))
    topic = "homeassistant/thermostat/temperature/state"
    db.set(topic, msg)
    temptature_set(int(msg))

@mqtt.on_topic('homeassistant/thermostat/temperature')
def handle_temp(client, userdata, message):
    state = db.get("homeassistant/thermostat/mode/state")
    if state == "auto":
        temp_check(int(msg))


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    payload=message.payload.decode()
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print('Received message on topic {}: {}'.format(message.topic, message.payload.decode()))
