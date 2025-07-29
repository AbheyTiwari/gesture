import cv2
import mediapipe as mp
import webbrowser as wb
import pyautogui
import time
import math

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
screen_width, screen_height = pyautogui.size()
fingertips = [4, 8, 12, 16, 20]

last_action_time = 0

def fingers_up(landmarks):
    fingers = []
    fingers.append(landmarks[4].x < landmarks[3].x)  # Thumb (horizontal)
    for tip, dip in zip([8, 12, 16, 20], [6, 10, 14, 18]):  # Others (vertical)
        fingers.append(landmarks[tip].y < landmarks[dip].y)
    return fingers

def distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def is_snap(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    dist1 = distance(thumb_tip, index_tip)
    dist2 = distance(thumb_tip, middle_tip)
    dist3 = distance(index_tip, middle_tip)
    return dist1 < 0.05 and dist2 < 0.05 and dist3 < 0.05  # Threshold can be tuned

def perform_action(gesture_name):
    global last_action_time
    now = time.time()
    if now - last_action_time < 2:  # Cooldown of 2 seconds
        return
    last_action_time = now

    print(f"Action: {gesture_name}")
    if gesture_name == "screenshot":
        pyautogui.hotkey('win', 'shift', 's')
    elif gesture_name == "spotify":
        pyautogui.press('win')
        time.sleep(0.3)
        pyautogui.write('spotify')
        time.sleep(0.2)
        pyautogui.press('enter')
    elif gesture_name == "chatgpt":
        wb.open("https://chat.openai.com")
    elif gesture_name == "whatsapp":
        pyautogui.press('win')
        time.sleep(0.3)
        pyautogui.write('whatsapp')
        time.sleep(0.2)
        pyautogui.press('enter')
    elif gesture_name == "minimize_all":
        pyautogui.hotkey('win', 'd')
    elif gesture_name == "snap_close":
        pyautogui.hotkey('alt', 'f4')

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
            finger_status = fingers_up(landmarks)

            # Draw white circles on fingertips
            for id in fingertips:
                x = int(landmarks[id].x * frame_width)
                y = int(landmarks[id].y * frame_height)
                cv2.circle(frame, (x, y), 10, (255, 255, 255), 2)

            # Gestures
            if finger_status == [False, True, True, False, False]:
                perform_action("screenshot")
            elif finger_status == [False, True, False, False, True]:
                perform_action("spotify")
            elif finger_status == [True, False, False, False, True]:
                perform_action("whatsapp")
            elif finger_status == [True, True, False, False, False]:
                perform_action("chatgpt")
            elif finger_status == [False, False, False, False, False]:
                perform_action("minimize_all")
            elif is_snap == [True, True, True, False, False]:
                perform_action("snap_close")

    cv2.imshow("Gesture Control", frame)
    cv2.waitKey(1)
