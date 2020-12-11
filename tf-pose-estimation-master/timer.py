import time
import cv2
import numpy as np
#Initialize camera
# cap = cv2.VideoCapture(0)

# TIMER = int(10)
# #Wait 10 seconds before checking if pose is correct
# prev = time.time()

def retColorImage(width, height, color):
    blank_image = np.zeros((height,width,3), np.uint8)
    blank_image[:,:] = color
    return blank_image



# font = cv2.FONT_HERSHEY_SIMPLEX
# thickness = 5
# font_scale = 2
# color = (255, 255, 255)


# green_frame = cv2.imread('green.png')

# blue_frame = green_frame.copy()
# height, width, channels = blue_frame.shape
# blue_frame[np.where((blue_frame == [75,176,0]).all(axis = 2))] = [176, 123, 0]
# blue_frame = blue_frame[0:100, 0:int(width/2)]
# cv2.putText(blue_frame, "WARRIOR", (50, 70), font, font_scale, color, thickness, cv2.LINE_AA)

# orange_frame = green_frame.copy()
# height, width, channels = orange_frame.shape
# orange_frame[np.where((orange_frame == [75,176,0]).all(axis = 2))] = [0, 179, 255]
# orange_frame = orange_frame[0:100, 0:int(width/2)]
# cv2.putText(orange_frame, "HOLD THE POSE", (50, 70), font, font_scale, color, thickness, cv2.LINE_AA)



cap = cv2.VideoCapture(0)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

blue_frame = retColorImage(int(w/2),100, (255,0,0))
green_frame = retColorImage(int(w/2),100, (0,255,0))

top_concat = cv2.hconcat([green_frame, blue_frame])
#blue_frame = np.array(blue_frame[0:height, 0:width]) #[y:y+h, x:x+w]
while True:
    #final = cv2.vconcat([top_concat, green_frame])

    #cv2.imshow('Hi', final)
    cv2.imshow('Hi', top_concat)
    k = cv2.waitKey(5)
    if k == 27:
        break

# while TIMER>=0:
#     curr = time.time()
    
#     ret, test_img = cap.read()
#     test_img = cv2.flip(test_img,1)
    
#     center_coord = (150,150)
#     radius = 100
#     color_bgr = (184, 143, 11)
#     thickness = -1 #fill circle
    
#     cv2.circle(test_img, center_coord, radius, color_bgr, thickness)
    
#     font = cv2.FONT_HERSHEY_TRIPLEX
#     cv2.putText(test_img, str(TIMER),
#                 (100,200), font,
#                 5, (255, 255, 255),
#                 10, cv2.LINE_AA)

#     final = cv2.vconcat([test_img, black_background])
    
#     cv2.imshow('Hi', final)
#     if curr-prev>=1:
#         prev = curr
#         TIMER = TIMER-1
    
#     k = cv2.waitKey(5)
#     if k == 27:
#         break


# Release the camera and destroy all windows
cap.release()
cv2.destroyAllWindows()
