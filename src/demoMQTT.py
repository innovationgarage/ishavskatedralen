from math import *
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import random
import sys
import cv2
import os
import time
import argparse
import tools
import clustering_tools
import glob

import paho.mqtt.client as mqtt
import os
import time
import config as c

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--src', type=str, default="video", help='Source of the images (options: "video" for video frames, [impath] to use the last image added to impath as input)')
    parser.add_argument('--dst', type=str, default="outputs/", help='Destination of the generated sequences')
    
    parser.add_argument('--year', type=int, default=2018, help='Date of the video (year)')
    parser.add_argument('--month', type=int, default=4, help='Date of the video (month)')
    parser.add_argument('--day', type=int, default=21, help='Date of the video (day)')
    
    parser.add_argument('--vidpath', type=str, default='videos/', help='Path to save videos')
    parser.add_argument('--dfpath', type=str, default='dataframes/', help='Path to save dataframe containing measurements')
    parser.add_argument('--seqpath', type=str, default='sequences/', help='Path to save sequences')
    
    parser.add_argument('--red', type=int, default=40, help='Sensitivity of the RED channel')
    parser.add_argument('--green', type=int, default=30, help='Sensitivity of the GREEN channel')
    parser.add_argument('--blue', type=int, default=30, help='Sensitivity of the BLUE channel')
    parser.add_argument('--lower_s', type=float, default=0, help='Lower limit of the S channel')
    parser.add_argument('--lower_v', type=float, default=0, help='Lower limit of the V channel')
    parser.add_argument('--nled', type=int, default=11, help='How many LEDs do you have in your cathedral?')
    parser.add_argument('--boost_green', type=bool, default=False, help='Should I boost the green color?')
    
    parser.set_defaults()
    args = parser.parse_args()

    channels = ['r', 'g', 'b']
    nx = ny = args.nled

    r_chs = ['r{}'.format(i) for i in np.arange(args.nled)]
    g_chs = ['g{}'.format(i) for i in np.arange(args.nled)]
    b_chs = ['b{}'.format(i) for i in np.arange(args.nled)]
    
    filters = tools.get_filters(args)

    original_video_path = tools.download_video(args.year, args.month, args.day, args.vidpath)
    ovpath, vname = os.path.split(original_video_path)

    video_path = original_video_path
    vpath = ovpath

    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    cols = ['vname','frame_no','flux_r','flux_g','flux_b','area_r','area_g','area_b']
    for i in range(args.nled):
        cols.append('r{}'.format(i))
        cols.append('g{}'.format(i))
        cols.append('b{}'.format(i))    
    df = pd.DataFrame(columns = cols)

    client = mqtt.Client()
    
    client.username_pw_set(c.mqttUser, c.mqttPassword)
    client.connect(c.mqttServer, c.mqttPort, 60)
    client.loop_start()

    # history = args.dst
    # open(history, 'wb')
    
    frame_no = 0
    while True:
#    while frame_no<20:
        ok, frame_original = video.read()
        if not ok:
            break
        
        # Start timer
        timer = cv2.getTickCount()
        
        frame_bgr = frame_original[0:500, 180:680] # specific to this dataset
        frame_bgr = frame_bgr[50:450, 50:450] # specific to this dataset
        
        frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        
        frame_no += 1

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
        
        if os.path.isdir(args.dst):
            if args.boost_green:
                seq_rgb = tools.img2seq(res_g_rgb, shape, args)
            else:
                seq_rgb = tools.img2seq(res_all_rgb, shape, args)

            led_values = bytearray(seq_rgb)
            client.publish(c.mqttPublishTo, led_values)
            time.sleep(0.5)
            
            
        # write all measurements to a dataframe
        df_line = [vname, frame_no, flux_r, flux_g, flux_b, area_r, area_g, area_b]
        for i in range(len(seq_rgb)):
            df_line.append(seq_rgb[i])
        df.loc[frame_no] = df_line
            
        cv2.putText(frame_bgr, "frame {}".format(frame_no), (150,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,250), 2)
        cv2.imshow("BGR", frame_bgr)
        if args.boost_green:
            cv2.putText(res_g_bgr, "frame {}".format(frame_no), (150,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,250), 2)
            cv2.imshow("res G", res_g_bgr)
        else:
            cv2.putText(res_all_bgr, "frame {}".format(frame_no), (150,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,250), 2)
            cv2.imshow("res all", res_all_bgr)
        
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            df.to_csv(os.path.join(args.dfpath, vname.replace('.mp4', '.csv'), index=False))
            # write the nonzero sequences into separate files /per channel)
            for channel in channels:
                print('writing sequences of channel {}'.format(channel))
                outpath = os.path.join(args.seqpath, 'seq_{}.csv'.format(channel))
                Channelmax = tools.write_sequences(df['frame_no'].min(), df['frame_no'].max(), df, channel, outpath)
            break
        
    df['r_seq'] = df['frame_no'].apply(lambda fno: np.array([df.loc[df.frame_no==fno, ch].values[0] for ch in r_chs]))
    df['g_seq'] = df['frame_no'].apply(lambda fno: np.array([df.loc[df.frame_no==fno, ch].values[0] for ch in g_chs]))
    df['b_seq'] = df['frame_no'].apply(lambda fno: np.array([df.loc[df.frame_no==fno, ch].values[0] for ch in b_chs]))
    df.to_csv(os.path.join(args.dfpath, vname.replace('.mp4', '.csv')), index=False)
    
    # write the nonzero sequences into separate files /per channel)
    for channel in channels:
        print('writing sequences of channel {}'.format(channel))
        outpath = os.path.join(args.seqpath, '{}_{}.csv'.format(vname.replace('.mp4', ''), channel))
        with open(outpath, 'w+') as f:
            tools.write_sequences(df['frame_no'].min(), df['frame_no'].max(), df, channel, f)
        
if __name__ == "__main__":
    main()
