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

def getNoseCoordinates(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    nose = noseCascade.detectMultiScale(gray, 1.3, 5)
    
    if len(nose) == 0:
        return ()

    allCoordinates = nose[0]
    
    return (int(allCoordinates[0] + 0.5 * allCoordinates[2]),  int(allCoordinates[1] + 0.5 * allCoordinates[3]))

def draw():
    video_capture = cv2.VideoCapture(0)
    brushCoordinates = []
    
    while True:
        success, frame = video_capture.read()
        # frame = removeBackground(frame)
        
        brushCoordinates.append(getNoseCoordinates(frame))
        
        if cv2.waitKey(1) & 0xFF == ord('d'):
            brushCoordinates = []
        else:   
            for coordinate in brushCoordinates:
                if len(coordinate) > 0:
                    cv2.circle(frame, coordinate, radius = 10, color = (0, 0, 255), thickness = -1)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    
def returnSavedPlot():
    pass

draw()