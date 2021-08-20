from flask import Flask
from flask_mqtt import Mqtt

mqtt = Mqtt()


def create_app():
    app = Flask(__name__)
    app = Flask(__name__)
    app.config['MQTT_BROKER_URL'] = '0.0.0.0'  # use the free broker from HIVEMQ
    app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
    app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
    app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
    mqtt.init_app(app)
    return app
 
