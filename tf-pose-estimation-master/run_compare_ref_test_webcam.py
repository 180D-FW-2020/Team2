import argparse
import logging
import sys
import time


from tf_pose import common
import cv2
import numpy as np
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

from threading import Thread
from playsound import playsound

logger = logging.getLogger('TfPoseEstimatorRun')
logger.handlers.clear()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

TIMER = int(10)

#Initialize camera
cap = cv2.VideoCapture(0)
cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#Colors BGR
yellow_color = (0, 255, 255)
red_color = (0,0,255)
green_color = (17, 87, 5)
white_color = (255,255,255)
black_color = (0,0,0)
blue_color = (176, 123, 0)
orange_color = (0, 179, 255)

#Settings
w_cam = 432
h_cam = 368
resize_out_ratio = 4

offset_xy = 200

#Will be filled 
pose_mask_list = []
overlay_list = []
ref_joint_list_arrays = []

#Circle for timer
center_coord = (150,150)
radius = 100
color_bgr = (184, 143, 11)
circle_thickness = -1 #fill circle

status_arr = ["NOW POSE", "HOLD FOR 3 SEC", "GREAT JOB"]
status = status_arr[0]

#Sounds
sounds = ['intro_pose.wav', 'hold.wav', 'great_job.wav']

#Sound thread function
def play_audio_file(sound_index):
    playsound('sounds/' + sounds[sound_index])

#Return (index, coordinate_string, score)
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

def compare_img_ret_accuracy(test_joint_array, ref_joint_array):

    #Now compare the joint coordinates
    #Loop through all joints
    #joint is a tuple of (index, coordinate_string, score)

    total = len(test_joint_array)
    correct = 0
    accuracy_arr = []

    if len(test_joint_array) != len(ref_joint_array):
        return -1
    for index in range(0,len(test_joint_array)):
        xy_threshold = 0.05

        test_joint = test_joint_array[index]
        x_coord_test = float(test_joint[1].split(',')[0].replace('(',''))
        y_coord_test = float(test_joint[1].split(',')[1].replace(')',''))

        ref_joint = ref_joint_array[index]
        x_coord_ref = float(ref_joint[1].split(',')[0].replace('(',''))
        y_coord_ref = float(ref_joint[1].split(',')[1].replace(')',''))

        if (x_coord_test >= x_coord_ref - xy_threshold and x_coord_test <= x_coord_ref + xy_threshold
            and y_coord_test >= y_coord_ref - xy_threshold and y_coord_test <= y_coord_ref + xy_threshold):
            correct+=1
            accuracy_arr.append((index, "Good"))
        else:
            accuracy_arr.append((index, "Bad"))

    accuracy = float(correct/total)
#    print("Correct: ", correct, "Accuracy", accuracy)
#    print(accuracy_arr)
    return accuracy

def retColorImage(width, height, color):
    blank_image = np.zeros((height,width,3), np.uint8)
    blank_image[0:height,0:width] = color
    return blank_image

#Pass in the 2 halves and the text to go on it
def retFinalImage(webcam_frame, timer_str, timer_color, frame1, text1, frame2, text2):
    #Pose and status
    frame1_copy = frame1.copy()
    cv2.putText(frame1_copy, text1, (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 5, cv2.LINE_AA)

    frame2_copy = frame2.copy()
    cv2.putText(frame2_copy, text2, (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 5, cv2.LINE_AA)
    top_concat = cv2.hconcat([frame1_copy, frame2_copy])

    cv2.circle(webcam_frame, center_coord, radius, timer_color, circle_thickness)
    cv2.putText(webcam_frame, timer_str,(100,200), cv2.FONT_HERSHEY_TRIPLEX, 5, (255, 255, 255), 10, cv2.LINE_AA)

    final = cv2.vconcat([top_concat, webcam_frame])

    return final

#Top bar
top_bar_height = 100 #in pixels
top_bar_width = int(cap_width/2)
green_frame = retColorImage(top_bar_width, top_bar_height, green_color)
blue_frame = retColorImage(top_bar_width, top_bar_height, blue_color)
orange_frame = retColorImage(top_bar_width, top_bar_height, orange_color)

#Parse input arguments to get pose list
parser = argparse.ArgumentParser(description='tf-pose-estimation run')
parser.add_argument('--pose', type=str, default='tree')
args = parser.parse_args()
pose = args.pose
pose_list = pose.split(',')
#pass in as --pose=squat,warrior,tree

#Create the joint overlay for each verification pose
for pose in pose_list:
    #Get joints of skeleton from reference image
    ref_image = cv2.imread('./images/references/' + pose + '_reference.jpg')
    e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(w_cam, h_cam))
    humans_ref = e.inference(ref_image, resize_to_default=1, upsample_size=resize_out_ratio)
    ref_joint_array = get_tuple_array(humans_ref)

    #Save skeleton image with black background
    black_background = np.zeros(ref_image.shape)
    ref_skeleton_img = TfPoseEstimator.draw_humans(black_background, humans_ref, imgcopy=False)
    filename_to_write = pose + '_reference_skeleton.jpg'
    cv2.imwrite(filename_to_write, ref_skeleton_img)

    #Create reference skeleton overlay using the black background
    overlay = cv2.imread(pose + '_reference_skeleton.jpg')
    overlayMask = cv2.cvtColor( overlay, cv2.COLOR_BGR2GRAY )
    res, overlayMask = cv2.threshold( overlayMask, 10, 1, cv2.THRESH_BINARY_INV)

    #Expand the mask from 1-channel to 3-channel
    h,w = overlayMask.shape
    overlayMask = np.repeat( overlayMask, 3).reshape( (h,w,3) )
    pose_mask_list.append(overlayMask)
    overlay_list.append(overlay)
    ref_joint_list_arrays.append(ref_joint_array)

#Go through all the poses
for i in range(len(pose_list)):

    pose = pose_list[i]
    overlay = overlay_list[i]
    overlayMask = pose_mask_list[i]
    ref_joint_array = ref_joint_list_arrays[i]
    timer_start = False

    #Start intro sound
    T = Thread(target=play_audio_file, args = [0])
    T.start()

    #Wait 10 seconds before checking if pose is correct
    prev = time.time()
    TIMER = int(10)
    while TIMER >= 0:
        curr = time.time()

        ret, test_img = cap.read()
        test_img = cv2.flip(test_img,1)

        test_img *=overlayMask
        test_img+=overlay

        final_frame = retFinalImage(test_img, str(TIMER), color_bgr, blue_frame, pose.upper(), orange_frame, status)

        cv2.imshow('Hi', final_frame)
        if curr-prev>=1:
            prev = curr
            TIMER = TIMER-1

        k = cv2.waitKey(5)
        if k == ord('q'):
            break

    #Reset timer back to 3 for holding
    TIMER = 3

    #Start the check
    while True:

        ret, test_img = cap.read()
        test_img = cv2.flip(test_img,1)

        humans_test = e.inference(test_img, resize_to_default=(w > 0 and h > 0), upsample_size=resize_out_ratio)
        test_joint_array = []
        if len(humans_test) is not 0:
            test_joint_array = get_tuple_array(humans_test)
            test_img = TfPoseEstimator.draw_humans(test_img, humans_test, imgcopy=False)

        combined_image = test_img
        combined_image *= overlayMask
        combined_image += overlay

        k = cv2.waitKey(10)
        # Press q to break
        if k == ord('q'):
            break

        accuracy = compare_img_ret_accuracy(test_joint_array, ref_joint_array)
        str_accuracy = int(accuracy*100)
        font = cv2.FONT_HERSHEY_SIMPLEX
        acc_coord_from_top_left = (0,700) #bottom left corner

        thickness = 5
        font_scale = 3

        if accuracy >= 0.6:
            #Hold position
            status = status_arr[1]
            cv2.putText(combined_image, "GOOD: " + str(str_accuracy) + "%", acc_coord_from_top_left, font, font_scale, green_color, thickness, cv2.LINE_AA)

            #Start timer when it is false and play "Now hold" sound
            if timer_start is False:
                timer_start = True
                prev = time.time()
                cur = time.time()
                T = Thread(target=play_audio_file, args = [1])
                T.start()

            #Timer is already running
            else:
                cur = time.time()
            #If one second has elapsed
            if cur-prev >= 1:
                prev = cur
                TIMER = TIMER-1
            #If timer is up, break
            if TIMER <=0:
                status = status_arr[2]
                font_scale=2
                thickness = 5
                #Play great job sound
                T = Thread(target=play_audio_file, args = [2])
                T.start()

                final_frame = retFinalImage(combined_image, str(TIMER), green_color, blue_frame, pose.upper(), green_frame, status)
                cv2.imshow('Hi', final_frame)
                cv2.waitKey(2000)

                status = status_arr[0]
                break

        else:
            status = status_arr[0]
            cv2.putText(combined_image, "BAD: " + str(str_accuracy), acc_coord_from_top_left, font, font_scale, red_color, thickness, cv2.LINE_AA)
            #reset timer back to 3 seconds
            TIMER = 3
            timer_start = False
        
        final_frame = retFinalImage(combined_image, str(TIMER), green_color, blue_frame, pose.upper(), orange_frame, status)
        cv2.imshow('Hi', final_frame)

# Release the camera and destroy all windows
cap.release()
cv2.destroyAllWindows()
