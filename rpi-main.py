from multiprocessing import Process
from MQTT.sub import client_mqtt
from IMU.python_BerryIMU_gryo_accel_compass_filters.berryIMU_classifier import imu_run
from Matrix.matrix_functions import *

f = open('ID.txt', 'r')
user_id = f.readline().replace('\n', '')
f.close()

def listen():
    #my_topic = '/team2' + user_id + '/reminders'
    my_topic = '/team2/network'
    get_user = ''
    print("listening for reminders!")
    print("listening for finished tasks!")

    # MQTT setup for laptop - RPI communication
    client_instance = client_mqtt(my_topic)
    caliente = client_instance.connect_mqtt()
    client_instance.subscribe_msg(caliente)
    caliente.loop_start()

    while True:
        if(client_instance.message != ''):
            #print('message on network:' + client_instance.message)
            get_user = client_instance.message.split(':')[0]
            task = client_instance.message.split(':')[1]
            if(get_user == user_id):
                if(task == 'reminder'):
                    print('calling reminder led matrix')
                    run_reminder()
                if(task == 'breathe'):
                    print('calling breath led program')
                    run_breathe()
                if(task == "talk"):
                    print('calling breath led program')
                    base_name = "message"
                    audio_suffix = "wav"
                    filename = base_name + "." + audio_suffix
                    client_instance.subscribe_file(caliente, filename)
            else:
                if (task == 'finish'):
                    print('calling congrats led program')
                    run_congrats()

            client_instance.set_message('')

def imu():
    print("starting IMU here!")
    imu_run()

def main():
    print('starting processes')
    p1 = Process(target = listen)
    p2 = Process(target = imu)
    p1.start()
    p2.start()

if __name__ == "__main__":
    main()
