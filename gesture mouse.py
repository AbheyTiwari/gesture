import cv2
import mediapipe as mp
import pyautogui
import webbrowser

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y=0
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x= int(landmark.x*frame_width)
                y= int(landmark.y*frame_height)
                if id == 8:
                    cv2.circle(img=frame, center=(x,y), radius=15, color=(255, 255, 255), thickness=2)
                    index_x= screen_width/frame_width*x
                    index_y= screen_height/frame_height*y
                    pyautogui.moveTo(x, y)
                    
                    
                if id == 4:
                    cv2.circle(img=frame, center=(x,y), radius=15, color=(255, 255, 255), thickness=2)
                    thumb_x= screen_width/frame_width*x
                    thumb_y= screen_height/frame_height*y
                    if abs(index_y-thumb_y) <20:
                        pyautogui.click()
                        pyautogui.sleep(1)
                    
                if id == 12:
                    cv2.circle(img=frame, center=(x,y), radius=15, color=(255, 255, 255), thickness = 2)
                    index_x= screen_width/frame_width*x
                    index_y= screen_height/frame_height*y
                    if abs(index_y-thumb_y) <20:
                        pyautogui.click()
                        pyautogui.sleep(1)
                    
                
                if id == 16:
                    cv2.circle(img=frame, center=(x,y), radius=15, color=(255, 255, 255), thickness =2)
                    index_x= screen_width/frame_width*x
                    index_y= screen_height/frame_height*y
                    
                
                if id == 20:
                    cv2.circle(img=frame, center=(x,y), radius=15, color=(255, 255, 255), thickness=2)
                    pinky_x= screen_width/frame_width*x
                    pinky_y= screen_height/frame_height*y
                    if abs(thumb_y-pinky_y) <20:
                        webbrowser.open('https://www.draupaditrust.org/')
                    
    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)