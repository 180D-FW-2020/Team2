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

#Settings
w_cam = 432
h_cam = 368
resize_out_ratio = 4

offset_xy = 200

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

def print_good_job():
    pass

parser = argparse.ArgumentParser(description='tf-pose-estimation run')
parser.add_argument('--pose', type=str, default='tree')
args = parser.parse_args()
pose = args.pose
pose_list = pose.split(',')
#pass in as --pose=squat,warrior,tree


pose_mask_list = []
overlay_list = []
ref_joint_list_arrays = []

#circle
center_coord = (150,150)
radius = 100
color_bgr = (184, 143, 11)
circle_thickness = -1 #fill circle

black_frame = cv2.imread('frame.jpg')
green_frame = cv2.imread('green.png')

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

        #Draw timer
        cv2.circle(test_img, center_coord, radius, color_bgr, circle_thickness)

        font = cv2.FONT_HERSHEY_TRIPLEX
        cv2.putText(test_img, str(TIMER),
                    (100,200), font,
                    5, (255, 255, 255),
                    10, cv2.LINE_AA)

        cv2.imshow('Hi', test_img)
        if curr-prev>=1:
            prev = curr
            TIMER = TIMER-1

        k = cv2.waitKey(5)
        if k == 27:
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
    #str_accuracy = "{:.2f}".format(accuracy)
        str_accuracy = int(accuracy*100)
        status_arr = ["Get into position!", "Now hold for 3 secs!", "Great job!"]
        status = status_arr[0]
        font = cv2.FONT_HERSHEY_SIMPLEX
        acc_coord_from_top_left = (0,700) #bottom left corner
        #BGR
        yellow_color = (0, 255, 255)
        red_color = (0,0,255)
        green_color = (0,255,0)
        white_color = (255,255,255)
        black_color = (0,0,0)
        color = yellow_color
        thickness = 4
        font_scale = 3

        #Coord in (x,y) [left to right is x axis] [up and down is y axis]. Set the coordinates of the timer, status, and pose texts
        textsize_pose = cv2.getTextSize(pose.upper(), font, font_scale, thickness)[0]
        textsize_status = cv2.getTextSize(status, font, font_scale, thickness)[0]
        textsize_timer = cv2.getTextSize(str(TIMER), font, font_scale, thickness)[0]

        mid_x = int((black_frame.shape[1] - textsize_pose[0]) / 2)
        pose_coord = (mid_x, 70 +offset_xy)

        mid_x = int((black_frame.shape[1] - textsize_timer[0]) / 2)
        timer_coord = (mid_x,250+offset_xy)

        mid_x = int((black_frame.shape[1] - textsize_status[0]) / 2)
        status_coord = (mid_x, 150 +offset_xy)

        if accuracy >= 0.6:
            #Hold position
            color = green_color
            status = status_arr[1]
            cv2.putText(combined_image, "GOOD: " + str(str_accuracy) + "%", acc_coord_from_top_left, font, font_scale, color, thickness, cv2.LINE_AA)

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
                font_scale=5
                thickness = 5
                #Play great job sound
                T = Thread(target=play_audio_file, args = [2])
                T.start()

                textsize_great_job = cv2.getTextSize(status, font, font_scale, thickness)[0]
                gj_mid_x = int((green_frame.shape[1] - textsize_great_job[0]) / 2)
                gj_mid_y = int((green_frame.shape[0] - textsize_great_job[1]) / 2)

                cv2.putText(green_frame, status, (gj_mid_x, gj_mid_y), font, font_scale, black_color, thickness, cv2.LINE_AA)
                final = cv2.hconcat([combined_image, green_frame])
                cv2.imshow('Hi', final)
                cv2.waitKey(2000)

                break

        else:
            color = red_color
            status = status_arr[0]
            cv2.putText(combined_image, "BAD: " + str(str_accuracy), acc_coord_from_top_left, font, font_scale, color, thickness, cv2.LINE_AA)
            #reset timer back to 3 seconds
            TIMER = 3
            timer_start = False
        black_frame = cv2.imread('frame.jpg')
        #Pose string
        cv2.putText(black_frame, pose.upper(), pose_coord, font, font_scale, yellow_color, thickness, cv2.LINE_AA, False) #top left corner
        #Timer string
        cv2.putText(black_frame, str(TIMER), timer_coord, font, font_scale, white_color, thickness, cv2.LINE_AA)
        #Status string
        cv2.putText(black_frame, status, status_coord, font, font_scale, yellow_color, thickness, cv2.LINE_AA)

        final = cv2.hconcat([combined_image, black_frame])
        cv2.imshow('Hi', final)

# Release the camera and destroy all windows
cap.release()
cv2.destroyAllWindows()
