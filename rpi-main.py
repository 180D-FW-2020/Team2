from multiprocessing import Process
from MQTT.sub import client_mqtt
from IMU.python_BerryIMU_gryo_accel_compass_filters.berryIMU_classifier import imu_run
from Matrix.matrix_functions import *

f = open('ID.txt', 'r')
user_id = f.readline().replace('\n', '')
f.close()

def listen():
    my_topic = '/' + user_id + '/reminders'
    net_topic = '/network/congrats'
    n_user = ''
    print("listening on topic for reminders!")
    print("listening on network for finished tasks!")

    # MQTT setup for laptop - RPI communication
    m_client_instance = client_mqtt(my_topic)
    m_caliente = m_client_instance.connect_mqtt()
    m_client_instance.subscribe_msg(m_caliente)
    m_caliente.loop_start()

    # MQTT setup for network communication
    n_client_instance = client_mqtt(net_topic)
    n_caliente = n_client_instance.connect_mqtt()
    n_client_instance.subscribe_msg(n_caliente)
    n_caliente.loop_start()
    
    while True:
        if(m_client_instance.message == 'reminder'):
            print('calling reminder led matrix')
            run_reminder()
        if(m_client_instance.message == 'breathe'):
            print('calling breath led program')
            run_breathe()
        if(n_client_instance.message != ''):
            print('message on network:' + n_client_instance.message)
            n_user = n_client_instance.message.split(':')[0]
            if(n_user != user_id):
                print('calling congrats led program')
                run_congrats()
        m_client_instance.set_message('')
        n_client_instance.set_message('')

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
