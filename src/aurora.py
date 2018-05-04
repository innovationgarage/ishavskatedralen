from math import *
import numpy as np
import sys
import cv2
import os
import serial
import time
import argparse
import tools
import clustering_tools
import glob
from datetime import datetime
import subprocess

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--srcpath', type=str, default="inputs/", help='Source of the frames to use the last image added to impath as input)')
    parser.add_argument('--dstpath', type=str, default="outputs/", help='Destination of the generated sequences to add the template number for each channel to the end of the dstpath file)')    
    parser.add_argument('--temppath', type=str, default='templates/', help='Path to available tempaltes')
    
    parser.add_argument('--red', type=int, default=40, help='Sensitivity of the RED channel')
    parser.add_argument('--green', type=int, default=30, help='Sensitivity of the GREEN channel')
    parser.add_argument('--blue', type=int, default=30, help='Sensitivity of the BLUE channel')
    parser.add_argument('--lower_s', type=float, default=0, help='Lower limit of the S channel')
    parser.add_argument('--lower_v', type=float, default=0, help='Lower limit of the V channel')
    parser.add_argument('--nled', type=int, default=11, help='How many LEDs do you have in your cathedral?')
    parser.add_argument('--boost_green', type=bool, default=False, help='Should I boost the green color?')
    parser.add_argument('--window', type=int, default=11, help='Window size used in template matching')
    
    parser.set_defaults()
    args = parser.parse_args()

    nx = ny = args.nled
    
    channels = ['r', 'g', 'b']
    r_chs = ['r{}'.format(i) for i in np.arange(args.nled)]
    g_chs = ['g{}'.format(i) for i in np.arange(args.nled)]
    b_chs = ['b{}'.format(i) for i in np.arange(args.nled)]
    
    filters = tools.get_filters(args)

    templates = {}
    for channel in channels:
        templates[channel] = tools.load_templates(os.path.join(args.temppath, 'template_{}.csv'.format(channel)))

    #check if the input and output paths exist
    os.makedirs(args.dstpath, exist_ok=True)
        
    # make sure there is a new history file for each day
    history = os.path.join(args.dstpath, '{}'.format(str(datetime.now().date())))
    if not os.path.isfile(history):
        open(history, 'wb')

    live = os.path.join(args.dstpath, 'live')

    if not os.path.isfile(live):
        open(live, 'wb')
        
    # find the latest input frame added to srcpath
    list_of_files = glob.glob(os.path.join(args.srcpath, '*'))
    latest_file = max(list_of_files, key=os.path.getctime)

    # load the frame
    frame_original = cv2.imread(latest_file)
        
    # Start timer
    timer = cv2.getTickCount()
        
    # frame_bgr = frame_original[0:500, 180:680] # specific to this dataset
    # frame_bgr = frame_bgr[50:450, 50:450] # specific to this dataset

    frame_bgr = frame_original
    
    frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        
    shape = (nx, ny)
        
    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        
    # Measure flux and area for each color
    _, res_r, flux_r, area_r = tools.apply_filter_to(frame_hsv, filters['red'])
    _, res_g, flux_g, area_g = tools.apply_filter_to(frame_hsv, filters['green'])
    _, res_b, flux_b, area_b = tools.apply_filter_to(frame_hsv, filters['blue'])
    _, res_all, flux_all, area_all = tools.apply_filter_to(frame_hsv, filters['all'])        
    
    # Resample and flatten the image into a 1D sequence
    res_r_rgb = cv2.cvtColor(res_r, cv2.COLOR_HSV2RGB)
    res_g_rgb = cv2.cvtColor(res_g, cv2.COLOR_HSV2RGB)
    res_b_rgb = cv2.cvtColor(res_b, cv2.COLOR_HSV2RGB)
    res_all_rgb = cv2.cvtColor(res_all, cv2.COLOR_HSV2RGB)
    
    res_r_bgr = cv2.cvtColor(res_r, cv2.COLOR_HSV2BGR)
    res_g_bgr = cv2.cvtColor(res_g, cv2.COLOR_HSV2BGR)
    res_b_bgr = cv2.cvtColor(res_b, cv2.COLOR_HSV2BGR)
    res_all_bgr = cv2.cvtColor(res_all, cv2.COLOR_HSV2BGR)

    with open(live, 'wb') as f_live:
        with open(history, 'ab') as f_history:
            if args.boost_green:
                seq_rgb = tools.img2seq(res_g_rgb, shape, args)
            else:
                seq_rgb = tools.img2seq(res_all_rgb, shape, args)

            seq_dict = {}
            temp_seq = np.zeros((args.nled*3,), dtype='int')
            for i, channel in enumerate(channels):
                seq_dict[channel] = {}
                seq_dict[channel]['original'] = [seq_rgb[j] for j in range(len(seq_rgb)) if j%3==i]
                seq_dict[channel]['temp_idx'], seq_dict[channel]['temp_seq'] = clustering_tools.match_template(
                    seq_dict[channel]['original'], templates[channel], args.window
                )
                # print(temp_seq)
                # print(seq_dict[channel]['temp_seq'])
                # print([j for j in range(len(seq_rgb)) if j%3==i])
                
                temp_seq[[j for j in range(len(seq_rgb)) if j%3==i]] = seq_dict[channel]['temp_seq']

                single_byte = seq_dict[channel]['temp_idx'].to_bytes(1, byteorder='little', signed=False)
                f_history.write(single_byte)
                f_live.write(single_byte)

    # update the remote file
    rsynccmd = "rsync --progress -e 'ssh -p  31338' outputs/live root@wiki.innovationgarage.no:/var/www/auroreal/status"
    rsyncproc = subprocess.Popen(rsynccmd,
                                 shell=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 )
    
    # print([seq_dict[x]['temp_idx'] for x in channels])
        
    cv2.imshow("BGR", frame_bgr)
    if args.boost_green:
        cv2.imshow("res G", res_g_bgr)
    else:
        cv2.imshow("res all", res_all_bgr)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(2)
        
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:        break
        
