import cv2
import time
import argparse

from tf_pose import common
import numpy as np
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import logging

logger = logging.getLogger('TfPoseEstimatorRun')
logger.handlers.clear()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

#Settings
w_cam = 432
h_cam = 368
resize_out_ratio = 4

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

def get_tuple_array(humans):
    ret_array = []
    human_string = str(humans[0])

    #print("Human", human_string)
    keypoints_list = human_string.split('BodyPart:')[1:]

    #'0-(0.52, 0.18) score=0.85 '
    #print("List length", len(keypoints_list))
    for joint in keypoints_list:
        #['0-(0.52,', '0.18)', 'score=0.85', ''] we need to get rid of last one
        if len(joint.split(' ')) == '3':
            tuple = joint.split(' ')[:-1]
        else:
            tuple = joint.split(' ')
        index = float((tuple[0]+tuple[1]).split('-')[0])
        xy_coord = (tuple[0]+tuple[1]).split('-')[1]
        score = float(tuple[2].replace('score=',''))
        #print("index: ", index, " xy_coord: ", xy_coord, " score: ", score)
        ret_array.append((index, xy_coord, score))
    return ret_array

def timer_img_capture(cap, pose):
    global timer
    timer = args.timer # SET THE COUNTDOWN TIMER
    while True:

        # Read and display each frame
        ret, img = cap.read()
        img = cv2.flip(img,1)

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
                img = cv2.flip(img,1)
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
                img = cv2.flip(img,1)
                # Display the clicked frame for 2
                # sec.You can increase time in
                # waitKey also
                cv2.imshow('a', img)

                # time for which image displayed
                # cv2.waitKey(2000)

                # Save the frame
                cv2.imwrite('./images/references/' + pose + '_reference.jpg', img)
                
                #Initialize estimator
                e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(w_cam, h_cam))
                #Create skeleton from captured image
                skeleton = e.inference(img, resize_to_default=1, upsample_size=resize_out_ratio)
                if len(skeleton) is not 0:
                    #Draw skeleton over original image
                    skeleton_human_overlay_img = TfPoseEstimator.draw_humans(img, skeleton, imgcopy=False)
                    #Display skeleton for 3 seconds
                    TIMER = int(3)
                    start_time = time.time()
                    while TIMER >= 0:
                        current_time = time.time()

                        if current_time-start_time >= 1:
                            start_time = current_time
                            TIMER = TIMER-1
                        
                        #Coordinates of the joints
                        ref_joint_array = get_tuple_array(skeleton)
                        num_joints = len(ref_joint_array)
                        cv2.putText(img, "Skeleton joint count: " + str(num_joints) + '/' + str(18),
                            (20, 30), font,
                            1, (0, 255, 255),
                            2, cv2.LINE_AA)
                        cv2.imshow('a', skeleton_human_overlay_img)
                        cv2.waitKey(2000)

                        if num_joints != 18:
                            return False
                        else:
                            return True
                        

                # exit loop
                break


        # Press Esc to exit
        elif k == 27:
            break

for pose in ref_pose:
    print("Pose",pose)
    
    while(timer_img_capture(cap, pose) == False):
        pass

# close the camera
cap.release()

# close all the opened windows
cv2.destroyAllWindows()