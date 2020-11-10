# Base code for MQTT from tutorial: https://github.com/pholur/180D_sample
# Adjustments for subscribing and writing the .wav file

# POSSIBLE BROKERS
# mqtt.eclipse.org
# test.mosquitto.org
# broker.emqx.io

import random
from paho.mqtt import client as mqtt_client


broker = 'mqtt.eclipse.org'
port = 1883
topic = "/isabel/michelle"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print("Write")
        f = open('phrase4_rec.wav', 'wb')
        f.write(msg.payload)
        f.close()
        client.disconnect()
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
