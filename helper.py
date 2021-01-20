from MQTT.sub import client_mqtt
from MQTT.pub import PUB
from Speech.audio_msg import speech
import subprocess
import os
import time

f = open('ID.txt', 'r')
user_id = f.readline().replace('\n', '')
f.close()

### HELPER FUNCTIONS ###

def activate():
    print("send message to LED Matrix")
    topic = "/team2/network"
    pub = PUB(topic, user_id + ':reminder')
    client = pub.connect_mqtt()
    client.loop_start()
    pub.publish_text(client)
    client.disconnect()

    print("waiting for IMU activation")
    imu_topic = '/' + user_id + '/imu'
    client_instance = client_mqtt(imu_topic)
    caliente = client_instance.connect_mqtt()
    client_instance.subscribe_msg(caliente, "msg.txt")
    caliente.loop_start()
    t_end = time.time() + (2*60) #give them 2 minutes to activate
    while(client_instance.message == '') and time.time() < t_end:
        pass
    try:
        type = client_instance.message.split(':')[1]
    except:
        type = ''
    caliente.disconnect()
    if type == 'VS':
        return True
        print("activation received!")
    return False

def exercise_stretch():
        print("calling stretching exercise")
        os.chdir('tf-pose-estimation-master')
        cmd = 'python run_compare_ref_test_webcam.py --pose=tree,squat,warrior'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        os.chdir('..')

def exercise_breathe():
        topic = '/team2/network'
        print("calling breathing exercise")
        pub = PUB(topic, user_id + ':breathe')
        client = pub.connect_mqtt()
        client.loop_start()
        pub.publish_text(client)
        client.disconnect()

def exercise_talk():
        topic = "/team2/network"
        print("calling talking to friends exercise")
        audio_filename = "Message"
        speech_instance = speech(audio_filename)
        speech_instance.msg_flow()
        # Send recorded message to specific person
        audio_path = speech_instance.get_audiopath()
        txt_path = speech_instance.get_txtpath()
        # Send transcription over - no audio message -
        pub = PUB(topic, user_id + ':talk')
        client = pub.connect_mqtt()
        client.loop_start()
        pub.publish_text(client)
        pub.publish_file(client, txt_path)
        client.disconnect()

def congrats():
    print("letting friends know you finished an activity")
    pub = PUB('/team2/network', user_id + ":" + 'finish')
    client = pub.connect_mqtt()
    client.loop_start()
    pub.publish_text(client)
    client.disconnect()