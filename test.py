import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import time

#necessary modules imported.

cap = cv2.VideoCapture(0) #0 is id num for webcam
detector = HandDetector(maxHands=1) #will only need 1 hand so
classifier = Classifier("Model/keras_model.h5","Model/labels.txt")
offset = 20
imgSize = 300

folder = "Data/C"
counter = 0

labels = ["A", "B", "C"]


while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)

    #for cropping img
    if hands:
        hand = hands[0] #coz only one hand no other
        x,y,w,h = hand['bbox'] #bounding box

        imgWhite = np.ones((imgSize,imgSize,3),np.uint8)*255

        imgCrop = img[y-offset: y + h+offset, x-offset: x + w+offset] #basically our pic is matrix so should give height and width

        aspectRatio = h/w
        if aspectRatio >1:
            k = imgSize/h
            wCal = math.ceil(k*w)
            imgResize = cv2.resize(imgCrop,(wCal, imgSize))
            imgResizeShape = imgResize.shape

            #to centre the pic
            wGap = math.ceil((imgSize-wCal)/2)
            imgWhite[:, wGap: wCal + wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite,draw=False)
            print(prediction,index)


        else: #doing for width
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize,hCal))
            imgResizeShape = imgResize.shape

            # to centre the pic
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap: hCal + hGap, :] = imgResize
            prediction, index = classifier.getPrediction(imgWhite,draw=False)

        cv2.rectangle(imgOutput, (x - offset, y - offset-50),(x-offset+90,y - offset-50+50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput,labels[index],(x,y-26),cv2.FONT_HERSHEY_COMPLEX,1.7,(255,255,255),2)
        cv2.rectangle(imgOutput,(x-offset,y-offset),(x+w+offset,y+h+offset ),(255,0,255),4)


        cv2.imshow("ImageCrop",imgCrop)
        cv2.imshow("ImageWhite", imgWhite)



    cv2.imshow("Image",imgOutput)
    cv2.waitKey(1) #delay of 1 msec

