from MQTT.sub import client_mqtt
from MQTT.pub import PUB
from Speech.audio_msg import speech
import subprocess
import os
import time

network_topic = '/team2/network'

### HELPER FUNCTIONS ###

def activate(user_id):
    reminder_topic = '/' + user_id + '/reminders'
    print("send message to LED Matrix")
    pub = PUB(reminder_topic, 'reminder')
    client = pub.connect_mqtt()
    client.loop_start()
    pub.publish_text(client)
    client.disconnect()

    print("waiting for IMU activation")

def config_stretch():
    print("calling stretching exercise")
    os.chdir('tf-pose-estimation-master')
    cmd = 'python timed_capture.py --ref_pose=tree,squat,warrior'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    os.chdir('..')

def exercise_stretch():
        print("calling stretching exercise")
        os.chdir('tf-pose-estimation-master')
        cmd = 'python run_compare_ref_test_webcam.py --pose=tree,squat,warrior'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        os.chdir('..')

def exercise_breathe(user_id):
        reminder_topic = '/' + user_id + '/reminders'
        print("calling breathing exercise")
        pub = PUB(reminder_topic, 'breathe')
        client = pub.connect_mqtt()
        client.loop_start()
        pub.publish_text(client)
        client.disconnect()

def congrats(user_id):
    print("letting friends know you finished an activity")
    pub = PUB(network_topic, user_id + ":" + 'finish')
    client = pub.connect_mqtt()
    client.loop_start()
    pub.publish_text(client)
    client.disconnect()


if __name__ == "__main__":
    exercise_talk('isabelketner')
