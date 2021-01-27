from MQTT.sub import client_mqtt
import os
from os import path
import time
import shutil
from datetime import datetime

class Listener:
    def __init__(self, *args):
        self.received = False
        if not (path.exists('./RecAudio') and path.exists('./RecTxt')):
            os.mkdir('./RecAudio/')
            os.mkdir('./RecTxt/')

    def listen(self):
        print('entering thread')
        print(self.received)
        f = open('ID.txt', 'r')
        user_id = f.readline().replace('\n', '')
        f.close()
        topic = '/' + user_id + '/messages'
        audio_topic = '/' + user_id + '/audio'
        txt_topic = '/' + user_id + '/text'

        txt_suffix = "txt"
        audio_suffix = "wav"

        client_instance = client_mqtt(txt_topic, audio_topic)
        client_instance.get_topics()
        caliente = client_instance.connect_mqtt()
        count = 1
        while(1):
            print("new while loop iteration")
            curr_time = datetime.now()
            curr_time = curr_time.strftime("%H--%M--%S");
            wav_file = curr_time + ".wav"
            txt_file = curr_time + ".txt"
            client_instance.subscribe_file(caliente, wav_file)
            count += 1
            caliente.loop_start()
            self.received = False
            print(self.received)
            while(1):
                if path.exists(wav_file):
                    time.sleep(10)
                    print("found .wav now save .txt")
                    if not path.exists(txt_file):
                        client_instance.subscribe_file(caliente, txt_file)
                        time.sleep(7)

                if path.exists(wav_file) and path.exists(txt_file):
                    self.received = True
                    print(self.received)
                    shutil.move(wav_file, "./RecAudio/" + wav_file)
                    shutil.move(txt_file, "./RecTxt/" + txt_file)
                    time.sleep(10)
                    break

    #caliente.disconnect()

if __name__ == "__main__":
    os.mkdir('./RecAudio/')
    os.mkdir('./RecTxt/')
    listen()
