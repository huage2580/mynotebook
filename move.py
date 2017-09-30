import cv2

cap = cv2.VideoCapture("rtmp://live.hkstv.hk.lxdns.com/live/hks")
print cap.isOpened()

avg = None

while cap.isOpened():
    ret,frame =cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21),0)
    if avg is None:
        avg = gray.copy().astype("float")
        continue
    cv2.accumulateWeighted(gray,avg,0.5)#low mean acc
    frameDelta = cv2.absdiff(gray,cv2.convertScaleAbs(avg))
    thresh = cv2.threshold(frameDelta,8,255,cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh,None,iterations=2)
    (cnts,_) = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        if cv2.contourArea(c) < 700:#rect
            continue
        (x,y,w,h) = cv2.boundingRect(c)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow("frame", frame)
    cv2.waitKey(1)

