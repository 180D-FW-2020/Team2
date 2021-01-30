from MQTT.sub import client_mqtt
import os
from os import path
import time
import shutil
from datetime import datetime
from MQTT.pub import PUB
from Speech.audio_msg import speech
import subprocess

f = open('ID.txt', 'r')
user_id = f.readline().replace('\n', '')
f.close()

network_topic = '/team2/network'

txt_suffix = "txt"
audio_suffix = "wav"

def listen():
    client_instance = client_mqtt(network_topic)
    client_instance.get_topics()
    caliente = client_instance.connect_mqtt()
    client_instance.subscribe_msg(caliente)
    caliente.loop_start()

    while(1):
        if (client_instance.message != ''):
            print("new while loop iteration")
            try:
                dest_user = client_instance.message.split(':')[0]
                print(dest_user)
            except:
                print ("Couldn't get the destination ID")

            audio_topic = '/' + dest_user + '/audio'
            txt_topic = '/' + dest_user + '/text'

            audio_filename = "Message"
            speech_instance = speech(audio_filename)
            speech_instance.main_record()
            # Send recorded message to specific person
            audio_path = speech_instance.get_audiopath()
            txt_path = speech_instance.get_txtpath()

            pub = PUB(audio_topic, "hello from audio")
            client = pub.connect_mqtt()
            client.loop_start()
            pub.publish_file(client, audio_path)
            client.disconnect()

            time.sleep(10)

            pub = PUB(txt_topic, dest_user + 'hello from txt')
            client = pub.connect_mqtt()
            client.loop_start()
            pub.publish_file(client, txt_path)
            client.disconnect()

            client_instance.message = ''


if __name__ == "__main__":
    if not (path.exists('./RecAudio') and path.exists('./RecTxt')):
        os.mkdir('./RecAudio/')
        os.mkdir('./RecTxt/')
    listen()
