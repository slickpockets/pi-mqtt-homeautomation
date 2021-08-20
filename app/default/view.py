import flask
from flask import render_template, Blueprint, request, jsonify, make_response, Response, url_for
from app import db, mqtt
from app.gpio import *
import json
import os
from os.path import join, dirname, realpath

default = Blueprint("default", __name__)
publish_topics=["homeassistant/thermostat/mode/state", "homeassistant/thermostat/temperature/state" ]
control_topics=["homeassistant/thermostat/mode/set", "homeassistant/thermostat/temperature/set"]

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
def handle_progress(client, userdata, message):
    msg = message.payload.decode()
    print("topic: {} message {}".format(message.topic, msg))
    if msg is in ["off", "auto", "cool", "fan_only", "heat"]:
        topic = "homeassistant/thermostat/mode/state"
        db.set(topic, msg)
        process_state(topic, msg)



@mqtt.on_topic('homeassistant/thermostat/temperature/set')
def handle_progress(client, userdata, message):
    msg = message.payload.decode()
    print("topic: {} message {}".format(message.topic, msg))
    topic = "homeassistant/thermostat/temperature/state"
    db.set(topic, msg)


    process_state(topic, msg)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    payload=message.payload.decode()
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print('Received message on topic {}: {}'.format(message.topic, message.payload.decode()))
