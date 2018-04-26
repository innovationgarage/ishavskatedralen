from math import *
import cv2
import os
import time
import argparse
import tools

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--vidpath', type=str, default='videos/', help='Path to save videos')    
    parser.add_argument('--year', type=int, default=2018, help='Date of the video (year)')
    parser.add_argument('--month', type=int, default=4, help='Date of the video (month)')
    parser.add_argument('--day', type=int, default=21, help='Date of the video (day)')

    parser.add_argument('--srcpath', type=str, default="inputs/", help='Source of the frames to use the last image added to impath as input)')
    
    parser.set_defaults()
    args = parser.parse_args()

    os.makedirs(args.srcpath, exist_ok=True)
        
    original_video_path = tools.download_video(args.year, args.month, args.day, args.vidpath)
    ovpath, vname = os.path.split(original_video_path)
    video_path = original_video_path
    vpath = ovpath
    
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print("Could not open video")
        sys.exit()
        
    frame_no = 0
    while True:
        ok, frame_original = video.read()
        if not ok:
            break
#        cv2.imwrite(os.path.join(args.srcpath, '{}.jpg'.format(frame_no)), frame_original)
        cv2.imwrite(os.path.join(args.srcpath, 'frame.jpg'), frame_original)        
        print('frame {}'.format(frame_no))
        frame_no += 1
        time.sleep(0.5)

if __name__ == "__main__":
    main()
    
