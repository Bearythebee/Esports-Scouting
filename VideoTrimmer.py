from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import pandas as pd
main_video = 'data/Main/original/CameraFeed/Video9.mp4'
dest_folder = 'data/Main/Split/Video9/'

timings = pd.read_csv("data/Main/Video9.csv")

video_timings = []

for i in range(timings.shape[0]):
    pd_start, pd_end = timings.iloc[i,0], timings.iloc[i,1]
    video_timings.append([str(pd_start),str(pd_end)])

def convert_timestring_to_seconds(tup):
    start, end = tup[0], tup[1]
    start_min, start_sec = start.split(':')
    end_min, end_sec = end.split(':')
    start_time = 60*(int(start_min))+int(start_sec)
    end_time = 60 * (int(end_min)) + int(end_sec)

    return start_time, end_time

count = 1
for times in video_timings:
    start_time, end_time = convert_timestring_to_seconds(times)
    ffmpeg_extract_subclip(main_video,  start_time, end_time, targetname=dest_folder+"{}.mp4".format(count))
    count+=1
