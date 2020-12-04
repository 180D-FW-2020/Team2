from MQTT.sub import client_mqtt

f = open('ID.txt', 'r')
user_id = f.readline().replace('\n', '')
f.close()
topic = '/' + user_id + '/reminders'

def listen():
    print("listening on topic for reminders!")
    client_instance = client_mqtt(topic)
    caliente = client_instance.connect_mqtt()
    client_instance.subscribe_wav(caliente)
    caliente.loop_start()
    while True:
        if(client_instance.message == 'talk'):
            print('received audio msg')
            run_reminder()
        client_instance.set_message('')

if __name__ == "__main__":
    listen()
