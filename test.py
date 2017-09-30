import cv2

cap = cv2.VideoCapture("rtmp://live.hkstv.hk.lxdns.com/live/hks")
print cap.isOpened()
cascPath = "/home/hua/code/lbpcascade_frontalface.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
while cap.isOpened():
    ret,frame =cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,minSize=(10,10))
    #print faces
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(100,255,100),2)
    cv2.imshow("frame", frame)
    cv2.waitKey(1)

