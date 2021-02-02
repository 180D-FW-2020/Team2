from MQTT.sub import client_mqtt
from MQTT.pub import PUB
from Team2.Speech.audio_msg import speech
import subprocess
import os
import time

f = open('ID.txt', 'r')
user_id = f.readline().replace('\n', '')
f.close()

reminder_topic = '/' + user_id + '/reminders'
msg_topic = '/' + user_id + '/messages'
audio_topic = '/' + user_id + '/audio'
txt_topic = '/' + user_id + '/text'
imu_topic = '/' + user_id + '/imu'
network_topic = '/team2/network'

### HELPER FUNCTIONS ###

def activate():
    print("send message to LED Matrix")
    #topic = "/team2/network"
    pub = PUB(reminder_topic, 'reminder')
    client = pub.connect_mqtt()
    client.loop_start()
    pub.publish_text(client)
    client.disconnect()

    print("waiting for IMU activation")

def exercise_stretch():
        print("calling stretching exercise")
        os.chdir('tf-pose-estimation-master')
        cmd = 'python run_compare_ref_test_webcam.py --pose=tree,squat,warrior'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        os.chdir('..')

def exercise_breathe():
        #topic = '/team2/network'
        print("calling breathing exercise")
        pub = PUB(reminder_topic, 'breathe')
        client = pub.connect_mqtt()
        client.loop_start()
        pub.publish_text(client)
        client.disconnect()

def exercise_talk(dest_user):
        #topic = "/team2/network"
        print(dest_user)
        print("calling talking to friends exercise")
        audio_topic = '/' + dest_user + '/audio'
        txt_topic = '/' + dest_user + '/text'

        audio_filename = "Message"
        speech_instance = speech(audio_filename)
        speech_instance.main_record()
        # Send recorded message to specific person
        audio_path = speech_instance.get_audiopath()
        txt_path = speech_instance.get_txtpath()
        # Send transcription over - no audio message -
        pub = PUB(audio_topic, "hello from audio")
        client = pub.connect_mqtt()
        client.loop_start()
        pub.publish_file(client, audio_path)
        client.disconnect()

        pub = PUB(txt_topic, dest_user + 'hello from txt')
        client = pub.connect_mqtt()
        client.loop_start()
        pub.publish_file(client, txt_path)
        client.disconnect()


def congrats():
    print("letting friends know you finished an activity")
    pub = PUB(network_topic, user_id + ":" + 'finish')
    client = pub.connect_mqtt()
    client.loop_start()
    pub.publish_text(client)
    client.disconnect()


if __name__ == "__main__":
    exercise_talk('isabelketner')
