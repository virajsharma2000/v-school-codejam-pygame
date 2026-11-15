import cv2
import mediapipe as mp
import socket

cam = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands

with mp_hands.Hands(
    static_image_mode = False,
    max_num_hands = 2,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5) as hands:
 

 orignal_x = None

 while True:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  ret, frame = cam.read()
  s.connect(('127.0.0.1', 8080))

  frame = cv2.resize(frame, (700,frame.shape[1]))
  rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

  results = hands.process(rgb_frame) 
  
  if results.multi_hand_landmarks:
   x = results.multi_hand_landmarks[0].landmark[8].x

   if orignal_x is None:
    pass

   elif orignal_x - x > 0.02:
    s.send(b'right')
    print('right')

   elif orignal_x - x < -0.02:
    s.send(b'left')
    print('left')

   orignal_x = x