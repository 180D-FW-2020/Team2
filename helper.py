from MQTT.sub import client_mqtt
from MQTT.pub import PUB
from Speech.audio_msg import speech

### HELPER FUNCTIONS ###

def activate(activity):
    print("send message to LED Matrix")
    pub = PUB('/team2/reminders', 'reminder')
    client = pub.connect_mqtt()
    client.loop_start()
    pub.publish_text(client)
    client.disconnect()

    print("waiting for IMU activation for " + activity)
    client_instance = client_mqtt('/team2/imu')
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
        pub = PUB('/team2/reminders', 'breathe')
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
        pub = PUB('/team2/reminders', 'talk')
        client = pub.connect_mqtt()
        client.loop_start()
        print("Sending " + audio_path + "...")
        pub.publish_audio(client, audio_path)
        client.disconnect()

def congrats(activity):
    #TODO: let users in network know you finished activity
    print("letting friends know you finished an activity")
