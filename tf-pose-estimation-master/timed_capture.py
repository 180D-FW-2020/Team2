import cv2
import time
import argparse

#Run script by specifying the pose you want to create a reference for (e.g. squat). This is a requirement
#1. python timed_capture.py --ref_pose=<pose_name> (e.g. python timed_capture.py --ref_pose=squat)
#2. To start the timer, press q (you might have to click on the window with the webcam first so it can register the key press)
#3. The timer is by default 7 seconds, but you can change it by passing in --timer=<num_seconds> (e.g. python timed_capture.py --ref_pose=squat --timer=10)
#4. Once the timer is done, the reference image will be saved in images/references/<pose_name>_reference.jpg, which can be used to find the joints

#Parse input arguments
parser = argparse.ArgumentParser(description='Reference image capture. Press q to start timer')
parser.add_argument('--ref_pose', type=str, required=True, help='Reference pose name which will be saved in images/references/<pose_name>_reference.jpg')
parser.add_argument('--timer', type=int, default=7, help='Timer(int) which is the amt of time before capture')
args = parser.parse_args()
ref_pose = args.ref_pose #SET THE REFERENCE POSE
TIMER = args.timer # SET THE COUNTDOWN TIMER

# Open the camera
cap = cv2.VideoCapture(0)

while True:

    # Read and display each frame
    ret, img = cap.read()
    cv2.imshow('a', img)

    # check for the key pressed
    k = cv2.waitKey(125)

    # set the key for the countdown
    # to begin. Here we set q
    # if key pressed is q
    if k == ord(' '):
        prev = time.time()

        while TIMER >= 0:
            ret, img = cap.read()

            # Display countdown on each frame
            # specify the font and draw the
            # countdown using puttext
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, str(TIMER),
                        (200, 250), font,
                        7, (0, 255, 255),
                        4, cv2.LINE_AA)
            cv2.imshow('a', img)
            cv2.waitKey(125)

            # current time
            cur = time.time()

            # Update and keep track of Countdown
            # if time elapsed is one second
            # than decrese the counter
            if cur-prev >= 1:
                prev = cur
                TIMER = TIMER-1

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
            cv2.imwrite('images/references/' + ref_pose + '_reference.jpg', img)

            # HERE we can reset the Countdown timer
            # if we want more Capture without closing
            # the camera

            # close the camera
            cap.release()

            # close all the opened windows
            cv2.destroyAllWindows()

            # exit program
            break


    # Press Esc to exit
    elif k == 27:
        break
