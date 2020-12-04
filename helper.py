from MQTT.sub import client_mqtt
from MQTT.pub import PUB
from Speech.audio_msg import speech

f = open('ID.txt', 'r')
user_id = f.readline().replace('\n', '')
f.close()
### HELPER FUNCTIONS ###

def activate(activity):
    print("send message to LED Matrix")
    topic = '/' + user_id + '/reminders'
    pub = PUB(topic, 'reminder')
    client = pub.connect_mqtt()
    client.loop_start()
    pub.publish_text(client)
    client.disconnect()

    print("waiting for IMU activation for " + activity)
    imu_topic = '/' + user_id + '/imu'
    client_instance = client_mqtt(imu_topic)
    caliente = client_instance.connect_mqtt()
    client_instance.subscribe_msg(caliente)
    caliente.loop_start()
    while(client_instance.message == ''):
        pass
    caliente.disconnect()

    if activity == 'stretch':
        #TODO: call stretching function
        print("calling " + activity + " exercise")

    if activity == 'breath':
        print("calling " + activity + " exercise")
        pub = PUB(topic, 'breathe')
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
        pub = PUB(topic, 'talk')
        # Send audio message with the transcription
        client = pub.connect_mqtt()
        client.loop_start()
        pub.publish_file(client, audio_path)
        pub.publish_file(client, txt_path)
        client.disconnect()

def congrats(activity):
    #TODO: let users in network know you finished activity
    print("letting friends know you finished an activity")
