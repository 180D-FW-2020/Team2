from MQTT.sub import client_mqtt
from os import path

f = open('ID.txt', 'r')
user_id = f.readline().replace('\n', '')
f.close()
topic = '/' + user_id + '/messages'

txt_suffix = "txt"
audio_suffix = "wav"

def listen():
    print("listening on topic for received messages and transcriptions!")
    client_instance = client_mqtt(topic)
    caliente = client_instance.connect_mqtt()
    caliente.loop_start()
    while True:
        client_instance.subscribe_msg(caliente)
        base_name = "message"
        if(client_instance.message == 'audio'):
            print ("audio file!")
            filename = base_name + "." + audio_suffix
            client_instance.subscribe_file(caliente, filename)
        if(client_instance.message == 'transcript'):
            print ("transcript file!")
        #     filename = base_name + "_transcript" + "." + txt_suffix
        #     client_instance.subscribe_file(caliente, filename)
        client_instance.set_message('')

if __name__ == "__main__":
    listen()
