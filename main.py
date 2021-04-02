import numpy as np
import cv2 as cv

vidcap = cv.VideoCapture("rtsp://admin:1234567.@10.254.36.11:554/ISAPI/Streaming/Channels/102")
# plates_cascade = cv.CascadeClassifier('haarcascade_russian_plate_number.xml')
width = 1000
height = 1000
vidcap.set(cv.CAP_PROP_FRAME_WIDTH, width)
vidcap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
ret, frame1 = vidcap.read()
vehicle = 0
safina = 0
ashan = 0
zeleniy = 0

while vidcap.isOpened():
    ret, frame2 = vidcap.read()
    frame = frame2.copy()
    if not ret:
        break
    fgMask = cv.absdiff(frame1, frame2)
    fgMask = cv.cvtColor(fgMask, cv.COLOR_RGB2GRAY)
    _, thresh = cv.threshold(fgMask, 50, 255, cv.THRESH_BINARY)
    frame1 = frame2

    # draw lines
    cv.line(frame, (700, 100), (1020, 100), (0,0,255), 2) #  first plate line To Safina
    cv.line(frame, (200, 460), (1200, 480), (0,0,255), 2) # second plate line from Main road

    cv.line(frame, (500, 200), (600, 100), (0,255,0), 2) # down line of traps To Zeleniy
    cv.line(frame, (1100, 250), (1050, 110), (0,255, 0), 2) # down line of traps To Ashan

    # extract contours
    conts, _ = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    for c in conts:
        
        #ignore small contours
        if cv.contourArea(c) < 100:
            continue
        x, y, w, h = cv.boundingRect(c)
        print("h: ", h)
        print("w: ", w)
        print("y: ", y)
        print("x: ", x)
        #draw  thr bound rect
        if w > 30:
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            xMiddle = int((x+(x+w))/2)
            yMiddle = int((y+(y+h))/2)
            cv.circle(frame, (xMiddle, yMiddle), 5, (0, 0, 255), 5)
            if yMiddle > 450 and yMiddle<480:
                vehicle += 1
            elif xMiddle < 500 and xMiddle > 490 and yMiddle < 200:
                zeleniy += 1
            elif xMiddle > 1050 and xMiddle < 1100 and yMiddle < 250:
                ashan += 1
            elif yMiddle > 90 and yMiddle < 100:
                safina += 1


    # cv.imshow("foreground Mask", fgMask)
    cv.putText(frame, "--> Ashan: {}".
    format(ashan), (1050, 100), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv.putText(frame, "<-- Zeleniy: {}".
    format(zeleniy), (200, 200), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv.putText(frame, " Main road: {}".
    format(vehicle), (100, 400), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    cv.putText(frame, "Safina: {}".
    format(safina), (700, 80), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    cv.imshow("Original video", frame)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

cv.destroyAllWindows()
vidcap.release()

