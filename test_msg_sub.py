from MQTT.sub import client_mqtt
import os
from os import path
import time
import shutil

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
    count = 1
    while(1):
        "new while loop iteration"
        wav_file = "test.wav"
        client_instance.subscribe_file(caliente, wav_file)
        count += 1
        caliente.loop_start()
        while(client_instance.message == ''):
            if path.exists(wav_file):
                time.sleep(10)
                print("found .wav now save .txt")
                if not path.exists("test.txt"):
                    client_instance.subscribe_file(caliente, "test.txt")
                    time.sleep(5)
                    if path.exists("./test.wav") and path.exists("./test.txt"):
                        shutil.move("test.wav", "./RecAudio/test.wav")
                        shutil.move("test.txt", "./RecTxt/test.txt")
                        break

    
    #caliente.disconnect()


if __name__ == "__main__":
    os.mkdir('./RecAudio/')
    os.mkdir('./RecTxt/')
    listen()

