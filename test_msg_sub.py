from MQTT.sub import client_mqtt

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
    client_instance.subscribe_msg(caliente)
    caliente.loop_start()
    while True:
        base_name = "message"
        if(client_instance.message == 'audio'):
            print ("audio file!")
            filename = base_name + "." + audio_suffix
            client_instance.subscribe_file(caliente, filename)
        elif(client_instance.message == 'txt'):
            print ("txt file!")
            filename = base_name + "_transcript" + "." + txt_suffix
            client_instance.subscribe_file(caliente, filename)

if __name__ == "__main__":
    listen()
