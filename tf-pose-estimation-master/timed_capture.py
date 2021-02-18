import cv2
import time
import argparse

#Run script by specifying the pose you want to create a reference for (e.g. squat). This is a requirement
#1. python timed_capture.py --ref_pose=<pose_name(s)> (e.g. python timed_capture.py --ref_pose=squat,warrior,tree)
#2. To start the timer, press space (you might have to click on the window with the webcam first so it can register the key press)
#3. The timer is by default 3 seconds, but you can change it by passing in --timer=<num_seconds> (e.g. python timed_capture.py --ref_pose=squat --timer=10)
#4. Once the timer is done, the reference image will be saved in images/references/<pose_name>_reference.jpg, which can be used to find the joints

#Parse input arguments
parser = argparse.ArgumentParser(description='Reference image capture. Press q to start timer')
parser.add_argument('--ref_pose', type=str, required=True, help='Reference pose name which will be saved in images/references/<pose_name>_reference.jpg')
parser.add_argument('--timer', type=int, default=3, help='Timer(int) which is the amt of time before capture')
args = parser.parse_args()
ref_pose = args.ref_pose.split(",") #SET THE REFERENCE POSES
timer = args.timer # SET THE COUNTDOWN TIMER
font = cv2.FONT_HERSHEY_SIMPLEX

# Open the camera
cap = cv2.VideoCapture(0)

def timer_img_capture(cap, pose):
    global timer
    timer = args.timer # SET THE COUNTDOWN TIMER
    while True:

        # Read and display each frame
        ret, img = cap.read()
        cv2.putText(img, "Press space to start timer",
                            (20, 30), font,
                            1, (0, 255, 255),
                            2, cv2.LINE_AA)
        cv2.putText(img, "Upcoming pose: " + pose,
                            (20, 60), font,
                            1, (0, 255, 255),
                            2, cv2.LINE_AA)
        cv2.imshow('a', img)

        # check for the key pressed
        k = cv2.waitKey(125)

        # set the key for the countdown
        # to begin. Here we set space
        # if key pressed is space
        if k == ord(' '):
            prev = time.time()

            while timer >= 0:
                ret, img = cap.read()

                # Display countdown on each frame
                # specify the font and draw the
                # countdown using puttext
                
                cv2.putText(img, str(timer),
                            (200, 250), font,
                            7, (0, 255, 255),
                            4, cv2.LINE_AA)
                cv2.putText(img, "Pose: " + pose,
                            (20, 30), font,
                            1, (0, 255, 255),
                            2, cv2.LINE_AA)
                cv2.imshow('a', img)
                cv2.waitKey(125)

                # current time
                cur = time.time()

                # Update and keep track of Countdown
                # if time elapsed is one second
                # than decrese the counter
                if cur-prev >= 1:
                    prev = cur
                    timer = timer-1

                # Press Esc to exit
                elif k == 27:
                    break

            #Timer is done
            else:
                ret, img = cap.read()
                
                # Display the clicked frame for 2
                # sec.You can increase time in
                # waitKey also
                cv2.imshow('a', img)

                # time for which image displayed
                cv2.waitKey(2000)

                # Save the frame
                cv2.imwrite('./images/references/' + pose + '_reference.jpg', img)

                # exit loop
                break


        # Press Esc to exit
        elif k == 27:
            break

for pose in ref_pose:
    print("Pose",pose)
    timer_img_capture(cap, pose)

# close the camera
cap.release()

# close all the opened windows
cv2.destroyAllWindows()