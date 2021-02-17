# from playsound import playsound
#
# playsound('StarWars3.wav')

import cv2
import time
font = cv2.FONT_HERSHEY_SIMPLEX
yellow_color = (0, 255, 255)
thickness = 4
font_scale=3

green_frame = cv2.imread('frame.jpg')
textsize_great_job = cv2.getTextSize("GREATAJOB", font, font_scale, thickness)[0]
gj_mid_x = int((green_frame.shape[1] - textsize_great_job[0]) / 2)
gj_mid_y = int((green_frame.shape[0] - textsize_great_job[1]) / 2)

cv2.putText(green_frame, "GREATAJOB", (gj_mid_x, gj_mid_y), font, 2, yellow_color, thickness, cv2.LINE_AA)
cv2.imshow('Hi', green_frame)
cv2.waitKey(6000)

# if key ==27:
#     cv2.destroyAllWindows()
