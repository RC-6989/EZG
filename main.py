#Gesture Controll for Windows
#Code by Rohit Chavali, Maurya Panchal, and Rishit Chavali

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.framework.formats import landmark_pb2
import time
from math import sqrt
import win32api, win32con
import math
import time
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


pyautogui.FAILSAFE = False
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
asdf = cast(interface, POINTER(IAudioEndpointVolume))

volume_level = asdf.GetMasterVolumeLevel()
volRange = volume = asdf.GetVolumeRange()
minvol = volRange[0]
maxvol = volRange[1]


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
click = 0
show_im = False
drawSpec1 = mp_drawing.DrawingSpec(thickness = 2, circle_radius = 1)

video = cv2.VideoCapture(0)

def findPosition(image, handNo=0):
    lmList = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
    return lmList

def leftClick():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        
        time.sleep(0.3)
        
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    
def rightClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    
    time.sleep(0.3)
    
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)

global tab
tab = 1
def alt_tab():
    global tab
    for x in range(tab):
        pyautogui.keyDown("alt")
        time.sleep(0.2)
        pyautogui.keyDown("tab")    
        time.sleep(0.4)
        pyautogui.keyUp("alt")
        pyautogui.keyUp("tab")
    tab += 1
    time.sleep(0.8)


with mp_hands.Hands() as hands:
    while video.isOpened():
        _, frame = video.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        imageHeight, image_Width, _ = image.shape
        results = hands.process(image)
        lmList = findPosition(image)
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, 
                                          mp_hands.HAND_CONNECTIONS, 
                                          mp_drawing.DrawingSpec(color = (50, 255, 50), 
                                                                 thickness = 2, 
                                                                 circle_radius = 2))
        try:
            for hand in results.multi_handedness:
                handType=hand.classification[0].label
        except: 
            continue
        
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                for point in mp_hands.HandLandmark:
                    normalizedLandmark = handLandmarks.landmark[point]
                    pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x, 
                                                                                           normalizedLandmark.y, 
                                                                                           image_Width, imageHeight)
                    point = str(point)
                    
                    if handType == "Right":
                        if point == 'HandLandmark.INDEX_FINGER_TIP':
                            try:
                                indexfingertip_x = pixelCoordinatesLandmark[0]
                                indexfingertip_y =  pixelCoordinatesLandmark[1]
                                win32api.SetCursorPos((indexfingertip_x*5, indexfingertip_y*6))
                                          
                            except:
                                pass
                        
                        elif point == 'HandLandmark.THUMB_TIP':
                            try:
                                thumbfingertip_x = pixelCoordinatesLandmark[0]
                                thumbfingertip_y =  pixelCoordinatesLandmark[1]

                            except:
                                pass
                if handType == "Right": 
                    for handLms in results.multi_hand_landmarks:
                        for id, lm in enumerate(handLms.landmark):
                            lineval_1 = None
                            lineval_2 = None
                            lineval_3 = None
                            h, w, c,  = image.shape
                            cx, cy = int(lm.x*w), int(lm.y*h)

                            if id == 4:
                                line_val1 = (cx, cy)

                                cv2.circle(image, (cx, cy), 3, (255, 0, 255), cv2.FILLED)

                            if id == 12:
                                line_val2 = (cx, cy)

                            if id == 20:
                                line_val3 = (cx, cy)


                                cv2.circle(image, (cx, cy), 3, (255, 0, 255), cv2.FILLED)

                    cv2.line(image, line_val1, line_val2, (190, 190, 190), 2)
                    cv2.line(image, line_val1, line_val3, (190,190,190), 2)
            if handType == "Right":
                lx, ly = int((line_val1[0] + line_val2[0])/2), int((line_val1[1] + line_val2[1])/2)
                cv2.circle(image, (lx, ly), 3, (255, 0, 255), cv2.FILLED)

                length_line = math.hypot( line_val2[0] - line_val1[0],line_val2[1] - line_val1[1])
                length_line1 = math.hypot( line_val3[0] - line_val1[0],line_val3[1] - line_val1[1])


                if int(length_line) < 15:
                        leftClick()

                if int(length_line1) < 15:
                        rightClick()

                if lmList[8][1]>500:
                       alt_tab()

        if handType == "Left":
         if results.multi_hand_landmarks:
          for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                lineval_1 = None
                lineval_2 = None
                h, w, c,  = frame.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                if id == 4:
                    line_val1 = (cx, cy)
                    cv2.circle(frame, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
                if id == 8:
                    line_val2 = (cx, cy)
                    
                    cv2.circle(frame, (cx, cy), 3, (255, 0, 255), cv2.FILLED)

            cv2.line(frame, line_val1, line_val2, (190, 190, 190), 2)
            
            lx, ly = int((line_val1[0] + line_val2[0])/2), int((line_val1[1] + line_val2[1])/2)
            cv2.circle(frame, (lx, ly), 3, (255, 0, 255), cv2.FILLED)
            
            length_line = math.hypot( line_val2[0] - line_val1[0],line_val2[1] - line_val1[1])
            
            
            vol_1 = np.interp(length_line, [11, 150], [minvol, maxvol])
            asdf.SetMasterVolumeLevel(vol_1, None)
            
            mp_drawing.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS, 
                                  drawSpec1, drawSpec1)
        if show_im:
            cv2.imshow("img", image)
            cv2.waitKey(1)


 

 
