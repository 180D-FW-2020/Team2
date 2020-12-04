from MQTT.sub import client_mqtt

def listen():
    print("listening on topic for reminders!")
    client_instance = client_mqtt('/team2/messages')
    caliente = client_instance.connect_mqtt()
    client_instance.subscribe_wav(caliente)
    client_instance.subscribe_txt(caliente)
    caliente.loop_start()
    while True:
        if(client_instance.message == 'talk'):
            print('receiving message + transcript')

if __name__ == "__main__":
    listen()
