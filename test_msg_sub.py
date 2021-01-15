from MQTT.sub import client_mqtt
from os import path

f = open('ID.txt', 'r')
user_id = f.readline().replace('\n', '')
f.close()
topic = '/' + user_id + '/messages'
audio_topic = '/' + user_id + '/audio'
txt_topic = '/' + user_id + '/text'

txt_suffix = "txt"
audio_suffix = "wav"

def listen():
    client_instance = client_mqtt(audio_topic)
    client_instance.get_topics()
    caliente = client_instance.connect_mqtt()
    client_instance.subscribe_file(caliente, "testing.wav")
    caliente.loop_start()
    for i in range(0,10):
        while(client_instance.message == ''):
            pass
        print("client msg:" , client_instance.message)

    caliente.disconnect()

if __name__ == "__main__":
    listen()
