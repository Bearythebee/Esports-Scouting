import cv2
import os

CHECK_FOLDER = os.path.isdir('data/test/videoframes/Main')
if not CHECK_FOLDER:
    os.makedirs('data/test/videoframes/Main')

for i in range(1,10):

    video_folder = 'data/Main/Split/Video{}/'.format(i)
    CHECK_FOLDER = os.path.isdir('data/test/videoframes/Main/Video{}'.format(i))
    if not CHECK_FOLDER:
        os.makedirs('data/test/videoframes/Main/Video{}'.format(i))

    for videoname in os.listdir(video_folder):
        cap = cv2.VideoCapture(video_folder+videoname)
        success,image = cap.read()
        count = 0
        print(videoname)
        destination_folder = 'data/test/videoframes/Main/Video{}/'.format(i) + videoname[:-4]
        print(destination_folder)
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