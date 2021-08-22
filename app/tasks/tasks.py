from app import celery
from app.sensors.sht30 import *
from paho.mqtt import client as mqtt_client
import time
from dotenv import dotenv_values
config = dotenv_values('.env')


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id=config["CLIENT_ID"])
    client.username_pw_set(username=config["USERNAME"], password=config["PASSWORD"])
    client.on_connect = on_connect
    client.connect(config["BROKER"], int(config["PORT"]))
    return client


# @celery.task()
# def humidity_task():
#     return(get_humidity())
#
# @celery.task()
# def tempature_task():
#     return(get_fTemp())


@celery.task(name ="periodic_task")
def periodic_task():
    print('Hi! from periodic_task')
    logger.info("Hello! from periodic task")
