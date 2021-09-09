import cv2

cap = cv2.VideoCapture('data/test/video/test_video.mp4')
success,image = cap.read()
count = 0
while success:
    cv2.imwrite('data/test/videoframes/raw/testvideo_.{}.png'.format(str(count).zfill(5)), image)    # save frame as JPEG file
    success,image = cap.read()
    print('Read a new frame: ', success)
    count += 1