# Base code for MQTT from tutorial: https://github.com/pholur/180D_sample
# Adjustments for subscribing and writing the .wav file

# POSSIBLE BROKERS
# mqtt.eclipse.org
# test.mosquitto.org
# broker.emqx.io

import random
from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'

class client_mqtt:
    def __init__(self, topic):
        self.topic = topic
        self.message = ''

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(client_id)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client

    def subscribe_file(self, client: mqtt_client, filename):
        def on_message(client, userdata, msg):
            print("Write")
            f = open(filename, 'wb')
            f.write(msg.payload)
            f.close()

        client.subscribe(self.topic)
        client.on_message = on_message

    def subscribe_msg(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            self.message = msg.payload.decode()
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        client.subscribe(self.topic)
        client.on_message = on_message

    def disconect_mqtt(self, client):
        client.disconnect()

    def set_message(self, msg):
        self.message = msg


#sample implementation
"""
    client_instance = client_mqtt('/isabel/michelle')
    caliente = client_instance.connect_mqtt()
    client_instance.subscribe_msg(caliente)
    caliente.loop_start()
    #do stuff
    #use loop_forever if ur not doing stuff
    client_instance.disconnect_mqtt(caliente)
"""
