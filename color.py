# import the necessary packages
import numpy as np
import argparse
import cv2
import time

vc = cv2.VideoCapture(0)
images=0
twoimages=0
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

boundaries = [
    ([0, 0, 150], [0, 0, 180]),
    ([250, 250, 0], [255, 255, 255]),
    ([25, 146, 190], [62, 174, 250]),
    ([103, 86, 65], [145, 133, 128])
]
image1=frame
image2=frame
# loop over the boundaries
while rval:
    image=frame

    
    #blur = cv2.blur(image,(10,10))
    #image=blur
    lower = np.array(boundaries[1][0], dtype = "uint8")
    upper = np.array(boundaries[1][1], dtype = "uint8")
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    #cv2.imshow("images",output)
    rval, frame = vc.read()
    if images==0:
        image1=output
        images=1
        time.sleep(2)
    else:
        image2=output
        twoimages=1
        images=0
    if twoimages==1:
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            print 'ok1'
        twoimages=0
        whiteMin = np.array([0, 0, 200], np.uint8)
        whiteMax = np.array([255, 50, 50], np.uint8)
        dst = cv2.inRange(image1, whiteMin, whiteMax)
        image1Count = cv2.countNonZero(dst)
        dst = cv2.inRange(image2, whiteMin, whiteMax)
        image2Count = cv2.countNonZero(dst)
        if image1Count>=image2Count:
            imageChange=image1 - image2
        else:
            imageChange=image2 - image1
        #imageChange = cv2.erode(imageChange, None, iterations=1)
        #imageChange = cv2.dilate(imageChange, None, iterations=1)
        cv2.imshow("images",imageChange)
        plot_image = np.concatenate((image1, image2), axis=1)
        cv2.imshow("images",plot_image)
