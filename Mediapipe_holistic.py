import cv2
import os
import mediapipe as mp
import numpy as np
import pandas as pd
import json

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose


WRIST = 0
THUMB_CMC = 1
THUMB_MCP = 2
THUMB_IP = 3
THUMB_TIP = 4
INDEX_FINGER_MCP = 5
INDEX_FINGER_PIP = 6
INDEX_FINGER_DIP = 7
INDEX_FINGER_TIP = 8
MIDDLE_FINGER_MCP = 9
MIDDLE_FINGER_PIP = 10
MIDDLE_FINGER_DIP = 11
MIDDLE_FINGER_TIP = 12
RING_FINGER_MCP = 13
RING_FINGER_PIP = 14
RING_FINGER_DIP = 15
RING_FINGER_TIP = 16
PINKY_MCP = 17
PINKY_PIP = 18
PINKY_DIP = 19
PINKY_TIP = 20

labels = pd.read_csv('data/test/Class.csv')

for i in range(1,10):
    player = 'Video{}'.format(i)
    image_dir = 'data/test/videoframes/Main/{}'.format(player)

    label = labels[labels['Video'] == player]['Class'].values[0]

    for folder in os.listdir(image_dir):

        with mp_holistic.Holistic(
                static_image_mode=False,
                model_complexity=2,
                min_detection_confidence=0.4,
                min_tracking_confidence=0.4) as holistic:

            main_arr = []
            videodir = image_dir+'/' + folder +'/raw'

            for idx, file in enumerate(os.listdir(videodir)):
                # Read an image, flip it around y-axis for correct handedness output (see
                # above).
                Image = cv2.imread(videodir +'/' + file)
                image = cv2.flip(Image, 1)
                #image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
                image_height, image_width, _ = image.shape

                # Convert the BGR image to RGB before processing.
                results = holistic.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

                pose_landmarks = results.pose_landmarks
                lefthand_landmarks = results.left_hand_landmarks
                righthand_landmarks = results.right_hand_landmarks

                if lefthand_landmarks ==  None or righthand_landmarks == None:
                    continue

                arr = []

                #leftshoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                #leftelbow = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
               # leftwristpose = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
                #arr.append([leftshoulder.x, leftshoulder.y, abs(leftwristpose.z) - abs(leftshoulder.z)])
                #arr.append([leftelbow.x, leftelbow.y, abs(leftwristpose.z) - abs(leftelbow.z)])

                leftwrist = ''
                for point in mp_hands.HandLandmark:
                    normalizedLandmark = lefthand_landmarks.landmark[point]
                    if point == mp_hands.HandLandmark.WRIST:
                        leftwrist = normalizedLandmark
                    else:
                        arr.append(normalizedLandmark.x - leftwrist.x)
                        arr.append(normalizedLandmark.y - leftwrist.y)
                        arr.append(normalizedLandmark.z - leftwrist.z)

                # #rightshoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                # #rightelbow = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
                # rightwristpose = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
                # #arr.append([rightshoulder.x, rightshoulder.y, abs(rightwristpose.z) - abs(rightshoulder.z)])
                # #arr.append([rightelbow.x, rightelbow.y, abs(rightwristpose.z) - abs(rightelbow.z)])

                rightwrist = ''
                for point in mp_hands.HandLandmark:
                    normalizedLandmark = righthand_landmarks.landmark[point]
                    if point == mp_hands.HandLandmark.WRIST:
                        rightwrist = normalizedLandmark
                    else:
                        arr.append(normalizedLandmark.x - rightwrist.x)
                        arr.append(normalizedLandmark.y - rightwrist.y)
                        arr.append(normalizedLandmark.z - rightwrist.z)
                #
                main_arr.append(arr)

            main_arr = np.array(main_arr)
            np.save('data/test/coordinates/Main/{}/{}.npy'.format(player,folder), main_arr)
        #
        # annotated_image = image.copy()
        #
        # # 1. Draw face landmarks
        # mp_drawing.draw_landmarks(annotated_image,
        #                           results.face_landmarks,
        #                           mp_holistic.FACEMESH_TESSELATION,
        #                           mp_drawing.DrawingSpec(color=(80, 110, 10),
        #                                                  thickness=1,
        #                                                  circle_radius=1),
        #                           mp_drawing.DrawingSpec(color=(80, 256, 121),
        #                                                  thickness=1,
        #                                                  circle_radius=1)
        #                           )
        #
        # # 2. Right hand
        # mp_drawing.draw_landmarks(annotated_image,
        #                           results.right_hand_landmarks,
        #                           mp_holistic.HAND_CONNECTIONS,
        #                           mp_drawing.DrawingSpec(color=(80, 22, 10),
        #                                                  thickness=2,
        #                                                  circle_radius=4),
        #                           mp_drawing.DrawingSpec(color=(80, 44, 121),
        #                                                  thickness=2,
        #                                                  circle_radius=2)
        #                           )
        #
        # # 3. Left Hand
        # mp_drawing.draw_landmarks(annotated_image,
        #                           results.left_hand_landmarks,
        #                           mp_holistic.HAND_CONNECTIONS,
        #                           mp_drawing.DrawingSpec(color=(121, 22, 76),
        #                                                  thickness=2,
        #                                                  circle_radius=4),
        #                           mp_drawing.DrawingSpec(color=(121, 44, 250),
        #                                                  thickness=2,
        #                                                  circle_radius=2)
        #                           )
        #
        # # 4. Pose Detections
        # mp_drawing.draw_landmarks(annotated_image,
        #                           results.pose_landmarks,
        #                           mp_holistic.POSE_CONNECTIONS,
        #                           mp_drawing.DrawingSpec(color=(245, 117, 66),
        #                                                  thickness=2,
        #                                                  circle_radius=4),
        #                           mp_drawing.DrawingSpec(color=(245, 66, 230),
        #                                                  thickness=2,
        #                                                  circle_radius=2)
        #                           )
        #
        # cv2.imwrite('data/test/videoframes/{}/{}/labelled/annotated_image_{}.png'.format(player,folder,idx),
        #            cv2.flip(annotated_image, 1))
