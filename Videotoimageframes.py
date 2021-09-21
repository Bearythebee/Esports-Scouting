import cv2
import os

videoname = 'test3'

cap = cv2.VideoCapture('data/test/video/'+videoname+'.mp4')
success,image = cap.read()
count = 0
destination_folder = 'data/test/videoframes/' + videoname
CHECK_FOLDER = os.path.isdir(destination_folder)

# If folder doesn't exist, then create it.
if not CHECK_FOLDER:
    os.makedirs(destination_folder)
    os.makedirs(destination_folder + '/labelled')
    os.makedirs(destination_folder+ '/raw')
    print("created folder : ", destination_folder)

else:
    print(destination_folder, "folder already exists.")

while success:
    cv2.imwrite(destination_folder + '/raw/test_.{}.png'.format(str(count).zfill(5)), image)    # save frame as JPEG file
    success,image = cap.read()
    count += 1

print(videoname + ' Done: {} frames'.format(count))