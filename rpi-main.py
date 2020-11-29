from multiprocessing import Process
from MQTT.sub import client_mqtt
from IMU.python_BerryIMU_gryo_accel_compass_filters.berryIMU_classifier import imu_run
from Matrix.matrix_functions import *

def listen():
    print("listening on topic for reminders!")
    client_instance = client_mqtt('/team2/reminders')
    caliente = client_instance.connect_mqtt()
    client_instance.subscribe_msg(caliente)
    caliente.loop_start()
    while True:
        if(client_instance.message == 'reminder'):
            print('calling reminder led matrix')
            run_reminder()
        if(client_instance.message == 'breathe'):
            print('calling breath led program')
            run_breathe()
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
