import cv2
import sys
from cvzone.SelfiSegmentationModule import SelfiSegmentation

noseCascade = cv2.CascadeClassifier("./haarcascade_mcs_nose.xml")

def removeBackground(img):
    """
    Removes the background of an image in OpenCV.
    Keyword Arguments
    img: the image to remove the background from.
    Returns the image with the background removed.
    """
    segmentor = SelfiSegmentation()
    img = segmentor.removeBG(img, (255, 255, 255), threshold = 0.55)
    return img

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    nose = noseCascade.detectMultiScale(gray, 1.3, 5)
    
    # Draw a rectangle around the nose
    for (x, y, w, h) in nose:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
    # Display the resulting frame
    frame = removeBackground(frame)
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
