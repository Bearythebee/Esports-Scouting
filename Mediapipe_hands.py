import cv2
import os
import mediapipe as mp
import numpy as np
import pandas as pd

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For static images:
camera = 'ROC_1.mp4'
image_dir = 'data/test/videoframes/{}/raw'.format(camera)

left_hand_arr = []
right_hand_arr =  []

with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.2) as hands:

    for idx, file in enumerate(os.listdir(image_dir)):
        # Read an image, flip it around y-axis for correct handedness output (see
        # above).
        Image = cv2.imread(
            'data/test/videoframes/{}/raw/'.format(
                camera) + file)
        image = cv2.flip(Image, 1)
        # Convert the BGR image to RGB before processing.
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

       # Print handedness and draw hand landmarks on the image.
 #       print('Handedness:', results.multi_handedness)

        if not results.multi_hand_landmarks:
            continue

        image_height, image_width, _ = image.shape

        annotated_image = image.copy()

        for i in range(0,2):
            hand_landmarks = results.multi_hand_landmarks[i]
            print(hand_landmarks)
            # if i == 0:
            #     print('----- LEFT HAND -----', )
            # else:
            #     print('----- RIGHT HAND -----', )

            hand_arr = []

            for point in mp_hands.HandLandmark:
                normalizedLandmark = hand_landmarks.landmark[point]
                # pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,
                #                                                                           normalizedLandmark.y,
                #                                                                           image_width, image_height)

                hand_arr.append([normalizedLandmark.x, normalizedLandmark.y,normalizedLandmark.z])

            if i == 0:
                left_hand_arr.append(hand_arr)
            else:
                right_hand_arr.append(hand_arr)

            mp_drawing.draw_landmarks(
                annotated_image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

            cv2.imwrite(
                'data/test/videoframes/{}/labelled/annotated_image_{}.png'.format(
                    camera, idx),
                cv2.flip(annotated_image, 1))