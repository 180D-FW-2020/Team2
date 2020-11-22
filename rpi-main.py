import threading

def listen():
    print("listening on topic for reminders!")

def imu():
    print("starting IMU here!")
    exec(open('./IMU/python_BerryIMU_gryo_accel_compass_filters/berryIMU_classifier.py').read())

def main():
    print("dispatch thread to start listening for reminders")
    t1 = threading.Thread(target=listen)
    #t2 = threading.Thread(target=imu)

    t1.start()
    #t2.start()
    imu()

if __name__ == "__main__":
    main()
