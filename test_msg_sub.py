from MQTT.sub import client_mqtt
import os
from os import path
import time
import shutil
from datetime import datetime
from MQTT.pub import PUB
import glob

class Listener:
    def __init__(self, *args):
        #self.received = False
        self.activated = False
        self.snoozed = False
        self.congrats = False
        self.dest_user=''
        self.sent_from_me=False
        self.audio_file = 'one_direction_has_my_heart.txt'
        self.text_file = 'one_direction_has_my_heart.txt'

    def set_activated(self, activated):
        self.activated = activated
    def set_snoozed(self, snoozed):
        self.snoozed = snoozed
    def set_sent_from_me(self, sent):
        self.sent_from_me=sent
    def set_congrats(self, congrats):
        self.congrats = congrats

    def listen(self):
        f = open('config.txt', 'r')
        f.readline()
        self.user_id = f.readline().split('=')[1].replace('\n', '')
        f.close()
        topic = '/' + self.user_id + '/messages'
        audio_topic = '/' + self.user_id + '/audio/#'
        txt_topic = '/' + self.user_id + '/text/#'
        imu_topic = '/' + self.user_id + '/imu'
        network_topic = '/team2/#'
        txt_suffix = "txt"
        audio_suffix = "wav"

        self.client_instance = client_mqtt(txt_topic, audio_topic, imu_topic, network_topic)
        self.client_instance.get_topics()
        self.caliente = self.client_instance.connect_mqtt()
        if not (path.exists('./RecAudio') and path.exists('./RecTxt')):
            os.mkdir('./RecAudio/')
            os.mkdir('./RecTxt/')
        while(1):
            '''
            remaining_files = glob.glob('*.txt')
            for f in remaining_files:
                if f != 'config.txt':
                    print(f'moving... `{f}`')
                    shutil.move(f, "./RecTxt/" + f)
            remaining_files = glob.glob('*.wav')
            for f in remaining_files:
                print(f'moving... `{f}`')
                shutil.move(f, "./RecAudio/" + f)
            '''
            print("new while loop iteration")
            curr_time = datetime.now()
            curr_time = curr_time.strftime("%H--%M--%S");
            wav_file = "./RecAudio/" + curr_time + ".wav"
            txt_file = "./RecTxt/" +curr_time + ".txt"
            self.client_instance.subscribe_file(self.caliente, curr_time)
            self.caliente.loop_start()
            #self.received = False
            self.sent_from_me = False
            t_now = time.time()
            while(1):
                if path.exists(self.client_instance.audio_file) and self.client_instance.first_received:
                    self.audio_file = self.client_instance.audio_file
                    self.text_file = self.client_instance.text_file
                    time.sleep(10)
                    print("found .wav now save .txt")
                    if not path.exists(self.text_file):
                        self.client_instance.subscribe_file(self.caliente, curr_time)
                        time.sleep(10)

                if path.exists(self.audio_file) and path.exists(self.text_file):
                    time.sleep(10)
                    break

                if time.time() > (t_now + 5):
                    self.client_instance.set_message('')
                    t_now = time.time() #messages expire after 5s
                    self.activated = False
                    self.snoozed = False
                    self.congrats = False
                if self.client_instance.message == 'Reminder:VS':
                    self.activated = True
                    self.client_instance.message = ''
                elif self.client_instance.message == "Reminder:LR":
                    self.snoozed = True
                    self.client_instance.message = ''
                elif self.client_instance.message != '':
                    self.dest_user = self.client_instance.message.split(':')[0]
                    task = self.client_instance.message.split(':')[1]
                    if(self.dest_user != self.user_id):
                        self.congrats = True
                '''
                else:
                    self.activated = False
                    self.snoozed = False
                    self.congrats = False
                '''

if __name__ == "__main__":
    os.mkdir('./RecAudio/')
    os.mkdir('./RecTxt/')
    listen()
