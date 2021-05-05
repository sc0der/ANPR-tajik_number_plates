
from const import videoPath
import cv2 as cv2
import numpy as np

width = 1000
height = 1000
vehicle = 0
safina = 0
ashan = 0
zeleniy = 0

face_cascade = cv2.CascadeClassifier('.\haarcascades_number\haarcascade_russian_plate_number.xml')
vidcap = cv2.VideoCapture(videoPath)
vidcap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vidcap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
scaling_factor = 1
while True:
    ret, frame = vidcap.read()
    try:
        frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    except:
        vidcap = cv2.VideoCapture(videoPath)
        continue
    face_rects = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=3)
    for (x,y,w,h) in face_rects:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
    
    # draw lines
    # first plate line To Safina
    cv2.line(frame, (700, 100), (1020, 100), (0, 0, 255), 2)
    # second plate line from Main road
    cv2.line(frame, (200, 460), (1200, 480), (0, 0, 255), 2)

    # down line of traps To Zeleniy
    cv2.line(frame, (500, 200), (600, 100), (0, 255, 0), 2)
    # down line of traps To Ashan
    cv2.line(frame, (1100, 250), (1050, 110), (0, 255, 0), 2)
    cv2.putText(frame, "--> Ashan: {}".
    format(ashan), (1050, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.putText(frame, "<-- Zeleniy: {}".
    format(zeleniy), (200, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.putText(frame, " Main road: {}".
    format(vehicle), (100, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    cv2.putText(frame, "Safina: {}".
    format(safina), (700, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    cv2.imshow('Car Detector', frame)
    c = cv2.waitKey(1)
    if c == 27:
        break
vidcap.release()
cv2.destroyAllWindows()
