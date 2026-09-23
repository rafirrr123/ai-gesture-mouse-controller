import cv2
import mediapipe as mp
import pyautogui
import time
import math

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.001

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands = 1,min_detection_confidence = 0.7)

#gesture controll

click_start_time = None
click_times = []
click_cooldown = 0.5
scroll_mode = False
freeze_cursor = False
drag_mode = False
is_dragging = False

screen_w, screen_h = pyautogui.size()
prev_screen_x,prev_screen_y = 0,0

cap = cv2.VideoCapture(0)

cv2.namedWindow("Live Video", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Live Video", cv2.WND_PROP_TOPMOST, 1)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret , frame = cap.read()
    if not ret:
        print("Cannot recieve cam")
        break
    frame = cv2.flip(frame,1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)

            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            middle_tip = hand_landmarks.landmark[12]
            ring_tip = hand_landmarks.landmark[16]
            pinky_tip = hand_landmarks.landmark[20]

            fingers = [
                1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y else 0
                for tip in [8,12,16,20]
            ]
            #distance between arm and index
            dist = math.hypot(thumb_tip.x - index_tip.x,thumb_tip.y - index_tip.y)
            if dist < 0.06:
                if not freeze_cursor:
                    freeze_cursor = True
                    click_times.append(time.time())

                    #double click
                    if len(click_times) >= 2 and click_times[-1]-click_times[-2] < 0.4:
                        pyautogui.doubleClick()
                        cv2.putText(frame,"Double Click",(10,50),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0,255,0),2)
                        click_times=[]
                    else:
                        pyautogui.click()
                        cv2.putText(frame,"Single Click",(10,50),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(255,255,0),2)

            else:
                freeze_cursor = False

            if not freeze_cursor:
                screen_x = int(middle_tip.x * screen_w *1.3)
                screen_y = int(middle_tip.y * screen_h *1.3)
                pyautogui.moveTo(screen_x,screen_y)
                prev_screen_x,prev_screen_y = screen_x,screen_y
                

            #scroll

            if sum(fingers)==4:
                scroll_mode = True
            else:
                scroll_mode = False

            if scroll_mode:
                if index_tip.y < 0.4:
                    pyautogui.scroll(60)
                    cv2.putText(frame,"Scroll-up",(10,50),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(255,0,255),2)
                elif index_tip.y > 0.6:
                    pyautogui.scroll(-60)
                    cv2.putText(frame,"Scroll-down",(10,50),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(255,0,255),2)


            ndist = math.hypot(thumb_tip.x - pinky_tip.x, thumb_tip.y - pinky_tip.y)
            if ndist < 0.07:
                if not is_dragging:
                    pyautogui.mouseDown(button='left')
                    is_dragging = True
                cv2.putText(frame, "DRAGGING", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                if is_dragging:
                    pyautogui.mouseUp(button='left')
                    is_dragging = False


    cv2.imshow("Live Video",frame)
    if(cv2.waitKey(1)==ord("q")):
        break
cap.release()
cv2.destroyAllWindows() 