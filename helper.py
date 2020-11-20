from MQTT.sub import client_mqtt

### CONSTANTS ###

#minutes
stretch_reminder = .5
breath_reminder = .5
talk_reminder = 1

congrats_message ="Congrats on completing a task!\nYou will be reminded to complete more tasks throughout the day."

### HELPER FUNCTIONS ###

def activate(activity):
    #TODO: use MQTT to let RPi know to light em tf up
    print("send message to LED Matrix")

    #listen on MQTT broker to see if any gestures are being detected at the current moment
    print("waiting for IMU activation for " + activity)
    client_instance = client_mqtt('/team2/imu')
    caliente = client_instance.connect_mqtt()
    client_instance.subscribe_msg(caliente)
    caliente.loop_start()
    while(client_instance.message == ''): #while(client_instance.message != 'activation msg') ??
        pass
    caliente.disconnect()

    if activity == 'strech':
        #TODO: call stretching function
        print("calling " + activity + " exercise")
    if activity == 'breath':
        #TODO: call breathing function
        print("calling " + activity + " exercise")
    if activity == 'talk':
        #TODO: call talking to friends function
        print("calling " + activity + " exercise")

def congrats (activity):
    #TODO: let users in network know you finished activity
    print("letting friends know you finished an activity")
