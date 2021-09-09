import cv2

import os
import mediapipe as mp
import numpy as np
import pandas as pd

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For static images:
image_dir = 'C:/Users/admin/PycharmProjects/EsportsProject/data/test/videoframes/raw'

left_hand_arr = []
right_hand_arr =  []

with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.4) as hands:

    for idx, file in enumerate(os.listdir(image_dir)):
        # Read an image, flip it around y-axis for correct handedness output (see
        # above).
        image = cv2.flip(cv2.imread('C:/Users/admin/PycharmProjects/EsportsProject/data/test/videoframes/raw/'+file), 1)
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
            # if i == 0:
            #     print('----- LEFT HAND -----', )
            # else:
            #     print('----- RIGHT HAND -----', )

            hand_arr = []

            for point in mp_hands.HandLandmark:
                normalizedLandmark = hand_landmarks.landmark[point]
                pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,
                                                                                          normalizedLandmark.y,
                                                                                          image_width, image_height)

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

            cv2.imwrite('data/test/videoframes/labelled/annotated_image_{}.png'.format(idx),
                        cv2.flip(annotated_image, 1))

    left_hand_arr = np.array(left_hand_arr)
    right_hand_arr = np.array(right_hand_arr)

    np.save('data/test/coordinates/lefthand.npy',left_hand_arr)
    np.save('data/test/coordinates/righthand.npy', right_hand_arr)

# # For webcam input:
# cap = cv2.VideoCapture(0)
# with mp_hands.Hands(
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5) as hands:
#   while cap.isOpened():
#     success, image = cap.read()
#     if not success:
#       print("Ignoring empty camera frame.")
#       # If loading a video, use 'break' instead of 'continue'.
#       continue
#
#     # Flip the image horizontally for a later selfie-view display, and convert
#     # the BGR image to RGB.
#     image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
#     # To improve performance, optionally mark the image as not writeable to
#     # pass by reference.
#     image.flags.writeable = False
#     results = hands.process(image)
#
#     # Draw the hand annotations on the image.
#     image.flags.writeable = True
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#     if results.multi_hand_landmarks:
#       for hand_landmarks in results.multi_hand_landmarks:
#         mp_drawing.draw_landmarks(
#             image,
#             hand_landmarks,
#             mp_hands.HAND_CONNECTIONS,
#             mp_drawing_styles.get_default_hand_landmarks_style(),
#             mp_drawing_styles.get_default_hand_connections_style())
#     cv2.imshow('MediaPipe Hands', image)
#     if cv2.waitKey(5) & 0xFF == 27:
#       break
# cap.release()