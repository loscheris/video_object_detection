from extract_frames import extract
from process_image import process
import os.path
import sys

#extract frames from video
video_path = '/Users/banzhiyong/final_project/data/MSVD/YouTubeClips'
# video_path = '/Users/banzhiyong/Desktop/video'
video_file_name = '5OuYhq6Zl0g_0_10.avi'
video_full_path = os.path.join(video_path, video_file_name)

frame_path = './input_videos/frames'
remove_files = [i for i in os.listdir(frame_path) if i.endswith('.jpg')]
for i in remove_files:
    os.remove(os.path.join(frame_path, i))
extract_fps = 4

frame_name, frame_indices, frame_count, fps, duration = extract(video_full_path, frame_path, extract_fps)

#object detection for each frames
model_name = 'ssd_inception_v2_coco_11_06_2017'
result = process(frame_path, frame_name, model_name)

print '==================================================================='
print 'All labels for each frame'
print result
#print frame_indices/float(frame_count) * duration


# Select labels for each second of the video
total_no_frame = extract_fps*duration

objects = {}
retain_prob = 70
for i in range(int(duration)):
    base = i*extract_fps
    objects[i] = {}
    for key in result[base]:
        objects[i][key] = result[base][key]
        for offeset in range(1, extract_fps):
            if key in result[base+offeset]:
                objects[i][key]+= result[base+offeset][key]
            else:
                objects[i].pop(key, None)
                break
        if key in objects[i]:
            if objects[i][key]/extract_fps < retain_prob:
                objects[i].pop(key, None)

print '==================================================================='
print 'Final result'
for i in range(int(duration)):
    print str(i) + '-' + str(i+1) + 's: ',
    for key in objects[i]:
        print key,
    print ' '
