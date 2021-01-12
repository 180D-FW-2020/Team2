from MQTT.sub import client_mqtt
from MQTT.pub import PUB
from Speech.audio_msg import speech
import subprocess
import os
import time

f = open('ID.txt', 'r')
user_id = f.readline().replace('\n', '')
f.close()

reminder_topic = '/' + user_id + '/reminders'
msg_topic = '/' + user_id + '/messages'
imu_topic = '/' + user_id + '/imu'
network_topic = '/team2/network'

### HELPER FUNCTIONS ###

def activate(activity):
    print("send message to LED Matrix"
    pub = PUB(reminder_topic)
    client = pub.connect_mqtt()
    client.loop_start()
    pub.publish_text(client)
    client.disconnect()

    print("waiting for IMU activation for " + activity)
    client_instance = client_mqtt(imu_topic)
    caliente = client_instance.connect_mqtt()
    client_instance.subscribe_msg(caliente)
    caliente.loop_start()
    while(client_instance.message == ''):
        pass
    caliente.disconnect()
    print("activation received!")
    return

def exercise(activity):
    if activity == 'stretch':
        print("calling " + activity + " exercise")
        os.chdir('tf-pose-estimation-master')
        cmd = 'python run_compare_ref_test_webcam.py --pose=tree,squat,warrior'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        os.chdir('..')

    if activity == 'breathe':
        print("calling " + activity + " exercise")
        pub = PUB(reminder_topic)
        client = pub.connect_mqtt()
        client.loop_start()
        pub.publish_text(client)
        client.disconnect()

    if activity == 'talk':
        print("calling " + activity + " exercise")
        audio_filename = "Message"
        speech_instance = speech(audio_filename)
        speech_instance.msg_flow()
        # Send recorded message to specific person
        audio_path = speech_instance.get_audiopath()
        txt_path = speech_instance.get_txtpath()
        # Send transcription over - no audio message -
        pub = PUB(msg_topic)
        client = pub.connect_mqtt()
        client.loop_start()
        pub.publish_text(client)
        pub.publish_file(client, txt_path)
        client.disconnect()

def congrats(activity):
    if activity == 'breathe':
        time.sleep(30)
    print("letting friends know you finished an activity")
    pub = PUB(msg_topic)
    client = pub.connect_mqtt()
    client.loop_start()
    pub.publish_text(client)
    client.disconnect()

def always_subbing():
    client_instance = client_mqtt(msg_topic,network_topic)
    caliente = client_instance.connect_mqtt()
    client_instance.subscribe_msg(caliente)
    caliente.loop_start()
    while(client_instance.message == ''):
        pass
    caliente.disconnect()
