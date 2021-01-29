from MQTT.sub import client_mqtt
import os
from os import path
import time
import shutil
from datetime import datetime
from MQTT.pub import PUB

class Listener:
    def __init__(self, *args):
        self.received = False
        self.activated = False
        self.snoozed = False
        self.congrats = False
        self.dest_user=''

    def set_activated(self, activated):
        self.activated = activated

    def listen(self):
        f = open('ID.txt', 'r')
        self.user_id = f.readline().replace('\n', '')
        f.close()
        topic = '/' + self.user_id + '/messages'
        audio_topic = '/' + self.user_id + '/audio'
        txt_topic = '/' + self.user_id + '/text'
        imu_topic = '/' + self.user_id + '/imu'
        network_topic = '/team2/network'
        txt_suffix = "txt"
        audio_suffix = "wav"

        self.client_instance = client_mqtt(txt_topic, audio_topic, imu_topic, network_topic)
        self.client_instance.get_topics()
        self.caliente = self.client_instance.connect_mqtt()
        if not (path.exists('./RecAudio') and path.exists('./RecTxt')):
            os.mkdir('./RecAudio/')
            os.mkdir('./RecTxt/')
        count = 1
        while(1):
            print("new while loop iteration")
            curr_time = datetime.now()
            curr_time = curr_time.strftime("%H--%M--%S");
            wav_file = curr_time + ".wav"
            txt_file = curr_time + ".txt"
            self.client_instance.subscribe_file(self.caliente, wav_file)
            count += 1
            self.caliente.loop_start()
            self.received = False
            print(self.received)
            t_now = time.time()
            while(1):
                if path.exists(wav_file):
                    time.sleep(10)
                    print("found .wav now save .txt")
                    if not path.exists(txt_file):
                        self.client_instance.subscribe_file(self.caliente, txt_file)
                        time.sleep(7)

                if path.exists(wav_file) and path.exists(txt_file):
                    self.received = True
                    print(self.received)
                    shutil.move(wav_file, "./RecAudio/" + wav_file)
                    shutil.move(txt_file, "./RecTxt/" + txt_file)
                    time.sleep(10)
                    break

                if time.time() > (t_now + 5):
                    self.client_instance.set_message('')
                    t_now = time.time() #messages expire after 5s
                if self.client_instance.message == 'Reminder:VS':
                    self.activated = True
                elif self.client_instance.message == "Reminder:RR":
                    self.snoozed = True
                elif self.client_instance.message != '':
                    self.dest_user = self.client_instance.message.split(':')[0]
                    task = self.client_instance.message.split(':')[1]
                    if(self.dest_user != self.user_id):
                        self.congrats = True
                else:
                    self.activated = False
                    self.snoozed = False
                    self.congrats = False


if __name__ == "__main__":
    os.mkdir('./RecAudio/')
    os.mkdir('./RecTxt/')
    listen()