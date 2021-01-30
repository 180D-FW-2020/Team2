import numpy as np
import cv2

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

#Return (index, coordinate_string, score)
def get_tuple_array(humans):
    ret_array = []
    human_string = str(humans[0])
    
    print("Human", human_string)
    keypoints_list = human_string.split('BodyPart:')[1:]
        
    #'0-(0.52, 0.18) score=0.85 '
    print("List length", len(keypoints_list))
    for joint in keypoints_list:
        #['0-(0.52,', '0.18)', 'score=0.85', ''] we need to get rid of last one
        if len(joint.split(' ')) == '3':
            tuple = joint.split(' ')[:-1]
        else:
            tuple = joint.split(' ')
        index = float((tuple[0]+tuple[1]).split('-')[0])
        xy_coord = (tuple[0]+tuple[1]).split('-')[1]
        score = float(tuple[2].replace('score=',''))
        print("index: ", index, " xy_coord: ", xy_coord, " score: ", score)
        ret_array.append((index, xy_coord, score))
    return ret_array

cap = cv2.VideoCapture(0)

# load the overlay file
overlay = cv2.imread('skeleton.jpg')

# detect which pixels in the overlay have something in them
# and make a binary mask out of it
overlayMask = cv2.cvtColor( overlay, cv2.COLOR_BGR2GRAY )
res, overlayMask = cv2.threshold( overlayMask, 10, 1, cv2.THRESH_BINARY_INV)

# expand the mask from 1-channel to 3-channel
h,w = overlayMask.shape
overlayMask = np.repeat( overlayMask, 3).reshape( (h,w,3) )

#path = "./images/downward_dog.jpg"
#img = cv2.imread(path)
## here's where the work gets done :
#
## mask out the pixels that you want to overlay
#img *= overlayMask
#
## put the overlay on
#img += overlay

# Show the image.

w_cam = 432
h_cam = 368
resize_out_ratio = 4
e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(w_cam, h_cam))


while True:
    ret, img = cap.read()

#print('image process+')
    humans = e.inference(img, resize_to_default=(w > 0 and h > 0), upsample_size=resize_out_ratio)

#print('postprocess+')
    img = TfPoseEstimator.draw_humans(img, humans, imgcopy=False)
    
    #https://stackoverflow.com/questions/20957433/how-to-draw-a-transparent-image-over-live-camera-feed-in-opencv
    # mask out the pixels that you want to overlay
    img *= overlayMask

    # put the overlay on
    img += overlay

    cv2.imshow("hi", img)
    k = cv2.waitKey(10)
    # Press q to break
    if k == ord('q'):
        break

# Release the camera and destroy all windows
cap.release()
cv2.destroyAllWindows()

