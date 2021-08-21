import asyncio
import time
from app.sensors.sht30 import get_fTemp, get_humidity
from config import config

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

client = connect_mqtt()


async def temp():
    while True:
        await asyncio.sleep(15)
        client.publish("homeassistant/thermostat/tempature", get_fTemp())

async def humidity():
    while True:
        await asyncio.sleep(15)
        client.publish("homeassistant/thermostat/humidity", get_humidity())



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(temp())
    asyncio.ensure_future(humidity())
    loop.run_forever()
