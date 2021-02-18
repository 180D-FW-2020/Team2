from multiprocessing import Process
from MQTT.sub import client_mqtt
from IMU.python_BerryIMU_gryo_accel_compass_filters.berryIMU_classifier import imu_run
from Matrix.matrix_functions import *
from datetime import datetime

f = open('config.txt', 'r')
f.readline()
user_id = f.readline().split('=')[1].replace('\n', '')
f.close()


def listen():
    cur_time = datetime.now()
    my_topic = '/' + user_id + '/reminders'
    get_user = ''
    network = '/team2/network'
    get_user = ''
    print("listening for reminders!")
    print("listening for finished tasks!")

    # MQTT setup for laptop - RPI communication
    client_instance = client_mqtt(my_topic, network)
    caliente = client_instance.connect_mqtt()
    client_instance.subscribe_msg(caliente)
    caliente.loop_start()
    run_clear()
    while True:
        if(client_instance.message != ''):
            print('message on network:' + client_instance.message)
            task = client_instance.message
            if(((datetime.now() - cur_time).total_seconds()) > 1):
                if(task == 'reminder'):
                    print('calling reminder led matrix')
                    run_reminder()
                elif(task == 'breathe'):
                    print('calling breath led program')
                    run_breathe()
                else:
                    print(task)
                    get_user = client_instance.message.split(':')[0]
                    task = client_instance.message.split(':')[1]
                    if(get_user != user_id):
                        print('calling congrats led program')
                        run_congrats()

            cur_time = datetime.now()
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
