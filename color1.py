import numpy as np
import argparse
import cv2
import time

def colorSpace(frame):
    gray_image1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    im_color1 = cv2.applyColorMap(gray_image1, cv2.COLORMAP_JET)
    return im_color1

def getLines(lines,frame):
    #print "lines "+str(len(lines))
    minx=800
    maxx=0
    miny=800
    maxy=0
    counthorizontal=0
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),2)
            #print ((x1-x2)**2+(y1-y2)**2)**(1/2)
            
        return frame

def redExtraction(im_color1):
    img_hsv = cv2.cvtColor(im_color1, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    # join my masks
    mask = mask0+mask1

    # set my output img to zero everywhere except my mask
    output_img = frame.copy()
    output_img[np.where(mask==0)] = 0
    return output_img
    
def colorSpaceRedExtraction(frame):
    im_color1=colorSpace(frame)
    extracted=redExtraction(im_color1)
    return extracted


boundaries = [
    ([0, 0, 150], [0, 0, 255]),
    ([150, 150, 0], [255, 255, 200]),
    ([25, 146, 190], [62, 174, 250]),
    ([103, 86, 65], [145, 133, 128])
]
vc = cv2.VideoCapture(0)
k=0
if vc.isOpened(): # try to get the first frame
    rval, frames = vc.read()
else:
    rval = False

while rval:
    framek = cv2.resize(frames, (640, 480))
    frame = framek[90:390,160:460]
    extracted1=colorSpaceRedExtraction(frame)
    #time.sleep(0.5)
    rval, frames = vc.read()
    framek = cv2.resize(frames, (640, 480))
    frame = framek[90:390,160:460]
    extracted2=colorSpaceRedExtraction(frame)  
    imageDifference=extracted1-extracted2
    imageDifference = cv2.cvtColor(imageDifference, cv2.COLOR_BGR2GRAY)
    imageDifference = cv2.erode(imageDifference, None, iterations=2)
    imageDifference = cv2.dilate(imageDifference, None, iterations=2)
    kernel = np.ones((10,10),np.float32)/25
    dst = cv2.filter2D(imageDifference,-1,kernel)
    blurred = cv2.bilateralFilter(dst,15,80,80)
    ret,blurred = cv2.threshold(blurred,200,255,cv2.THRESH_BINARY)
    
    #edges = cv2.Canny(blurred, 50, 150,apertureSize = 3)

    #gamma=0.05
    #invGamma = 1.0 / gamma
    #table = np.array([((i / 255.0) ** invGamma) * 255
    #for i in np.arange(0, 256)]).astype("uint8")
 
	
    #gamma1=cv2.LUT(edges, table)
    #kernel = np.ones((4,4),np.uint8)
    #kernel1 = np.ones((4,4),np.uint8)
    #opening = cv2.morphologyEx(gamma1, cv2.MORPH_OPEN, kernel)
    #opening = cv2.morphologyEx(gamma1, cv2.MORPH_CLOSE, kernel)
    #opening = cv2.dilate(opening,kernel1,iterations = 4)
    #opening = cv2.erode(opening,kernel1,iterations = 4)
    #kernel = np.ones((10,10),np.float32)/25
    #dst = cv2.filter2D(gamma1,-1,kernel)
    #blurred = cv2.bilateralFilter(dst,15,80,80)
    #equ = cv2.equalizeHist(dst)
    #edges = cv2.Canny(opening, 290, 350,apertureSize = 3)
    #minLineLength = 1
    #maxLineGap = 5
    #lines = cv2.HoughLinesP(opening,1,np.pi/180,1,minLineLength,maxLineGap)
    #lines = cv2.HoughLinesP(blurred,1,np.pi/180,1,minLineLength,maxLineGap)

    frame1=frame
    k,contours,hierarchy = cv2.findContours(blurred, 1, 2)
    try:
        if contours is not None:
            cnt = contours[0]
            area = cv2.contourArea(cnt)
            #print area
            if((area>1000)):
                M = cv2.moments(cnt)
                centroid_x = int(M['m10']/M['m00'])
                centroid_y = int(M['m01']/M['m00'])
                print centroid_x
                print centroid_y
                pt1 = (centroid_x,centroid_y)
                frame1=cv2.circle(frame1,pt1,5,(0,255,0),5)
                #cv2.circle(frame,(int(centroid_x),int(centroid_y)),5,(200,0,0),2)
                x,y,w,h = cv2.boundingRect(cnt)
                frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                print "momment(" + str(centroid_x)+"," + str(centroid_y)+") rectangle middle ("+str(x+w/2)+","+str(y+h/2)+")"
                frame1=cv2.circle(frame1,(int(x+w/2),int(y+h/2)),5,(0,0,255),5)
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                #frame = cv2.drawContours(frame,[box],0,(0,0,255),2)
                approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
                #print len(approx)
                #cv2.drawContours(frame,[cnt],0,255,-1)
                #print [cnt]
                rc = cv2.minAreaRect(contours[0])
                box = cv2.boxPoints(approx)
                cnts = cnts[0] if imutils.is_cv2() else cnts[1]
                c = max(cnts, key=cv2.contourArea)
                extLeft = tuple(c[c[:, :, 0].argmin()][0])
                extRight = tuple(c[c[:, :, 0].argmax()][0])
                extTop = tuple(c[c[:, :, 1].argmin()][0])
                extBot = tuple(c[c[:, :, 1].argmax()][0])
                cv2.circle(frame, extLeft, 8, (0, 0, 255), -1)
                cv2.circle(frame, extRight, 8, (0, 255, 0), -1)
                cv2.circle(frame, extTop, 8, (255, 0, 0), -1)
                cv2.circle(frame, extBot, 8, (255, 255, 0), -1)
                for p in box:
                    pt = (p[0],p[1])
                    print pt
                    cv2.circle(frame,pt,5,(200,0,0),2)
                
    except:
        print "no contor"
    #lines = cv2.HoughLines(opening,1,np.pi/180,50)
    #if lines is not None:
        #print len(lines)
        #for rho,theta in lines[0]:
            #a = np.cos(theta)
            #b = np.sin(theta)
            #x0 = a*rho
            #y0 = b*rho
            #x1 = int(x0 + 1000*(-b))
            #y1 = int(y0 + 1000*(a))
            #x2 = int(x0 - 1000*(-b))
            #y2 = int(y0 - 1000*(a))

            #cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),2)
    #if lines is not None:
        #print "lines "+str(len(lines))
        #for line in lines:
            #for rho,theta in line:            
                #a = np.cos(theta)
                #b = np.sin(theta)
                #x0 = a*rho
                #y0 = b*rho
                #x1 = int(x0 + 1000*(-b))
                #y1 = int(y0 + 1000*(a))
                #x2 = int(x0 - 1000*(-b))
                #y2 = int(y0 - 1000*(a))
                #cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
                #print str(rho)+" "+str(theta)
    #if lines is not None:
        #frame=getLines(lines,frame)

    #edges = cv2.Canny(gray_filtered,150,250)
    #cv2.imshow("color",opening)
    #cv2.imshow("edges",gamma1)
    #cv2.imshow("red",approx)
    cv2.imshow("object",blurred)
    cv2.imshow("preview",frame)
    cv2.imshow("previewq",frame1)
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    rval, frames = vc.read()
cv2.destroyWindow("preview")
