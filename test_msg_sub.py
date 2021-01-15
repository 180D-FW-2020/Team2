from MQTT.sub import client_mqtt
from os import path
import time

f = open('ID.txt', 'r')
user_id = f.readline().replace('\n', '')
f.close()
topic = '/' + user_id + '/messages'
audio_topic = '/' + user_id + '/audio'
txt_topic = '/' + user_id + '/text'

txt_suffix = "txt"
audio_suffix = "wav"

def listen():
    client_instance = client_mqtt(txt_topic, audio_topic)
    client_instance.get_topics()
    caliente = client_instance.connect_mqtt()
    client_instance.subscribe_file(caliente, "test.wav")
    caliente.loop_start()
    while(client_instance.message == ''):
        if path.exists("test.wav"):
            time.sleep(10)
            print("found .wav - save in .txt")
            if not path.exists("test.txt"):
                client_instance.subscribe_file(caliente, "test.txt")

    caliente.disconnect()

if __name__ == "__main__":
    listen()
