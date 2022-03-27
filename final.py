import cv2
import numpy as np
import mediapipe as mp
from time import time, sleep
import random

def getNumberFingersUp(image):
    mp_Hands = mp.solutions.hands
    hands = mp_Hands.Hands()
    mpDraw = mp.solutions.drawing_utils
    finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
    thumb_Coord = (4,2)
    upCount = 0
    
    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(RGB_image)
    multiLandMarks = results.multi_hand_landmarks
    
    if multiLandMarks:
        handList = []
        for handLms in multiLandMarks:
            mpDraw.draw_landmarks(image, handLms, mp_Hands.HAND_CONNECTIONS)
            for idx, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                handList.append((cx, cy))
            for point in handList:
                cv2.circle(image, point, 10, (255, 255, 0), cv2.FILLED)
            
            for coordinate in finger_Coord:
                if handList[coordinate[0]][1] < handList[coordinate[1]][1]:
                    upCount += 1
            if handList[thumb_Coord[0]][0] > handList[thumb_Coord[1]][0]:
                upCount += 1
                
    return upCount

def updateSecretWord(word):
    secret_word = "cat"
    updated_word = ""
    
    while True:
        random_index = random.randint(0, len(word) - 1)
        print(word[random_index])
        
        if word[random_index] == " ":
            for idx, char in enumerate(word):
                if (idx == random_index):
                    updated_word += secret_word[random_index]
                else:
                    updated_word += word[idx]
            break
            
    return updated_word

def hasStars(word):
    for char in word:
        if char == " ":
            return True
    
    return False
            
drawing = False # true if mouse is pressed
pt1_x , pt1_y = None , None
r, g, b = 255, 255, 255

# mouse callback function
def line_drawing(event,x,y,flags,param):
    global pt1_x,pt1_y,drawing, r, g, b

    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        pt1_x,pt1_y=x,y

    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            cv2.line(img,(pt1_x,pt1_y),(x,y),color=(r,g,b),thickness=3)
            pt1_x,pt1_y=x,y
    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        cv2.line(img,(pt1_x,pt1_y),(x,y),color=(r,g,b),thickness=3)        


img = np.zeros((1024,1024,3), np.uint8)
cv2.namedWindow('test draw')
cv2.setMouseCallback('test draw', line_drawing)

camera = cv2.VideoCapture(0)
DELAY = 25
currentWord = "   "

for k in range(1_000_000):
    success, web_img = camera.read()

    if (k % 300 == 0 and hasStars(currentWord)):
        currentWord = updateSecretWord(currentWord)
        cv2.putText(img, currentWord, (400, 100), cv2.FONT_HERSHEY_PLAIN, 4, (0,255,0), 4)
    
    cv2.imshow('test draw',img)
    
    if (k % DELAY == 0):
        upCount = getNumberFingersUp(web_img)
        
        if upCount == 1:
            img = np.zeros((1024,1024,3), np.uint8)
        elif upCount == 2:
            r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
       
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        
cv2.destroyAllWindows()