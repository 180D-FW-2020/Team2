import threading

def listen():
    print("listening on topic for reminders!")

def imu():
    print("starting IMU here!")

def main():
    print("dispatch thread to start listening for reminders")
    t1 = threading.Thread(target=listen)
    t2 = threading.Thread(target=imu)

    t1.start()
    t2.start()

if __name__ == "__main__":
    main()
