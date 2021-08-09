from app.mqtt.client import *

def run():
    client = connect_mqtt()
    client.loop_start()
    pub_temp(client)
    pub_hum(client)
    subscribe(client)



if __name__ == '__main__':
    run()
