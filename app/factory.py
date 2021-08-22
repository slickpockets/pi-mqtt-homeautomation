import eventlet
import json
from flask import Flask
from flask_mqtt import Mqtt
from celery import Celery
import redis
from datetime import timedelta
eventlet.monkey_patch()
mqtt = Mqtt()
from dotenv import dotenv_values
config = dotenv_values('.env')


def setupdb(url=config['REDISURL'], password=config['REDISPASS'], db=config['REDISDB'], port=config['REDISPORT']):
    db = redis.StrictRedis(
        host=url,
        password=password,
        port=port,
        db=db,
        decode_responses=True
    )
    return(db)


def make_celery(app=None):
    app = app or create_app()
    celery = Celery(
        app.import_name,
        backend="redis://localhost:6370/0",
        broker="redis://localhost:6379/1"
    )
    celery.conf.update(app.config)
    celery.config_from_object(celeryconfig)
    TaskBase = celery.Task


    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery




def create_app():
    app = Flask(__name__)
    app.config['SECRET'] = ''
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['MQTT_BROKER_URL'] = config["BROKER"]
    app.config['MQTT_BROKER_PORT'] = int(config["PORT"])
    app.config['MQTT_USERNAME'] = config["USERNAME"]
    app.config['MQTT_PASSWORD'] = config["PASSWORD"]
    app.config['MQTT_KEEPALIVE'] = 5
    app.config['MQTT_TLS_ENABLED'] = False
    app.config['APP_NAME'] = 'relay'
    app.config['CELERYBEAT_SCHEDULE'] = {
        'periodic_task-every-minute': {
            'task': 'periodic_task',
            'schedule': timedelta(seconds=30)
            }
        }


    with app.app_context():
        mqtt.init_app(app)

    from app.default import default
    app.register_blueprint(default)

    return app
