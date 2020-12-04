from MQTT.sub import client_mqtt

f = open('ID.txt', 'r')
user_id = f.readline().replace('\n', '')
f.close()
topic = '/' + user_id + '/reminders'

def listen():
    print("listening on topic for reminders!")
<<<<<<< HEAD
    client_instance = client_mqtt('/team2/messages')
=======
    client_instance = client_mqtt(topic)
>>>>>>> ade3be9f077fd1d7bebca06bcc54eeef49e32f5f
    caliente = client_instance.connect_mqtt()
    client_instance.subscribe_wav(caliente)
    client_instance.subscribe_txt(caliente)
    caliente.loop_start()
    while True:
        if(client_instance.message == 'talk'):
            print('receiving message + transcript')

if __name__ == "__main__":
    listen()
