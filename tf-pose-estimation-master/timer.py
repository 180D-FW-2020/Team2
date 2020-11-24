import time
import cv2
import numpy as np
#Initialize camera
cap = cv2.VideoCapture(0)

TIMER = int(10)
#Wait 10 seconds before checking if pose is correct
prev = time.time()

ref_image = cv2.imread('./images/references/' + 'warrior' + '_reference.jpg')
black_background = cv2.imread('frame.jpg') #np.zeros(ref_image.shape)

while TIMER>=0:
    curr = time.time()
    
    ret, test_img = cap.read()
    test_img = cv2.flip(test_img,1)
    
    center_coord = (150,150)
    radius = 100
    color_bgr = (184, 143, 11)
    thickness = -1 #fill circle
    
    cv2.circle(test_img, center_coord, radius, color_bgr, thickness)
    
    font = cv2.FONT_HERSHEY_TRIPLEX
    cv2.putText(test_img, str(TIMER),
                (100,200), font,
                5, (255, 255, 255),
                10, cv2.LINE_AA)

    final = cv2.vconcat([test_img, black_background])
    
    cv2.imshow('Hi', final)
    if curr-prev>=1:
        prev = curr
        TIMER = TIMER-1
    
    k = cv2.waitKey(5)
    if k == 27:
        break


# Release the camera and destroy all windows
cap.release()
cv2.destroyAllWindows()
