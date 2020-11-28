from MQTT.sub import client_mqtt
from MQTT.pub import PUB

### HELPER FUNCTIONS ###

def activate(activity):
    print("send message to LED Matrix")
    pub = PUB('/team2/reminders', 'reminder')
    client = pub.connect_mqtt()
    client.loop_start()
    pub.publish_text(client)

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
        
    if activity == 'talk':
        #TODO: call talking to friends function
        print("calling " + activity + " exercise")

def congrats(activity):
    #TODO: let users in network know you finished activity
    print("letting friends know you finished an activity")
