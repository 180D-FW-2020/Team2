# Base code for MQTT from tutorial: https://github.com/pholur/180D_sample
# Adjustments for subscribing and writing the .wav file

# POSSIBLE BROKERS
# mqtt.eclipseprojects.io
# test.mosquitto.org
# broker.emqx.io

import random
from paho.mqtt import client as mqtt_client
import os
import os.path
from os import path
import sys
import re

broker = 'mqtt.eclipseprojects.io'
port = 1883
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
id_path = os.path.join(os.getcwd(), 'ID.txt')



class client_mqtt:
    def __init__(self, *args):
        self.topic_list = []
        self.message = ''
        f = open(id_path, 'r')
        self.user_id = f.readline().replace('\n', '')
        f.close()
        for arg in args:
            self.topic_tuple = (arg, 0)
            self.topic_list.append(self.topic_tuple)


    def get_topics(self):
        print(self.topic_list)


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
            # Added this because subscriber kept overwriting files with "self.msg" parameters
            #look at sender based on user id????
            audio_rec = re.search('audio', msg.topic)
            text_rec = re.search('text', msg.topic)
            audio_file = filename + '.wav'
            text_file = filename + '.txt'
            print(audio_file)
            print(text_file)
            if audio_rec:
                if not path.exists(audio_file):
                    print("Write")
                    f = open(audio_file, 'wb')
                    print(msg.payload)
                    f.write(msg.payload)
                    f.close()
            elif text_rec:
                if not path.exists(text_file):
                    print("Write")
                    f = open(text_file, 'wb')
                    print(msg.payload)
                    f.write(msg.payload)
                    f.close()
            else:
                self.message = msg.payload.decode()
                print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


        client.subscribe(self.topic_list)
        client.on_message = on_message

    def subscribe_msg(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            self.message = msg.payload.decode()
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        client.subscribe(self.topic_list)
        client.on_message = on_message

    def disconnect_mqtt(self, client):
        client.disconnect()

    def set_message(self, msg):
        self.message = msg


def run():
    #sample implementation
    client_instance = client_mqtt("/team2/audiomsg", "/team2/michelletan")
    client_instance.get_topics()
    caliente = client_instance.connect_mqtt()
    client_instance.subscribe_file(caliente, "testing.txt")
    caliente.loop_start()
    for i in range(0, 20):
        while(client_instance.message == ''):
            pass
        print("client msg:" , client_instance.message)

    caliente.disconnect()
    print("activation received!")
    return

if __name__ == "__main__":
    run()
