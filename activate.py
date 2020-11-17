from MQTT.sub import client_mqtt

def activate(activity):
    print("send message to LED Matrix")
    #use MQTT to let RPi know to light em tf up
    print("wait for IMU input for " + activity)
    #listen on MQTT broker to see if any gestures are being detected rn
    #this means IMU can run continuously, but we will only be listening during select moments
    client_instance = client_mqtt('/isabel/michelle')
    caliente = client_instance.connect_mqtt()
    client_instance.subscribe_msg(caliente)
    caliente.loop_start()
    while(client_instance.message == ''):
        pass
    print(client_instance.message)
    caliente.disconnect()

    if activity == 'strech':
        print("calling " + activity + " exercise")
    if activity == 'breath':
        print("calling " + activity + " exercise")
    if activity == 'talk':
        print("calling " + activity + " exercise")
