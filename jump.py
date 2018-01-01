import cv2
import numpy as np

img = cv2.imread("D:\\test.jpg")

color = img[10][10]
color = (int(color[0]),int(color[1]),int(color[2]))
# set blue thresh
lower_blue=np.array([125,43,46])
upper_blue=np.array([155,255,255])
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# 紫色
mask = cv2.inRange(hsv, lower_blue, upper_blue)
# 膨胀
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(9, 9))
dilated = cv2.dilate(mask,kernel)
_,cnts,_ = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
for c in cnts:
    (x,y,w,h) = cv2.boundingRect(c)
    cv2.rectangle(img,(x,y),(x+w,y+h),color,-1)
canny = cv2.Canny(img, 30, 250)
# 方块
_,cntscube,_ = cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img,cntscube,-1,(0,0,255),3)
for c in cntscube:
    (x,y,w,h) = cv2.boundingRect(c)
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
img = cv2.pyrDown(img)
img = cv2.pyrDown(img)
cv2.imshow("Image",img)
cv2.waitKey(0)
