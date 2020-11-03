# Base code for MQTT from tutorial: https://github.com/pholur/180D_sample
# Adjustments for reading existing .wav file and publishing

import time
import random
from paho.mqtt import client as mqtt_client
broker = 'test.mosquitto.org'
port = 1883
topic = "/isabel/michelle"
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
     msg_count = 0
     while True:
         time.sleep(1)
         # msg = f"messages: {msg_count}"
         f = open("name.wav", "rb")
         soundstr = f.read()
         f.close()
         msg = bytearray(soundstr)
         # result = client.publish(topic, msg)
         result = client.publish(topic, msg)
         # result: [0, 1]
         status = result[0]
         if status == 0:
             print(f"Send `{msg}` to topic `{topic}`")
         else:
             print(f"Failed to send message to topic {topic}")
         msg_count += 1

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
