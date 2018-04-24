from math import *
import random
import cv2
import numpy as np
import pandas as pd
import os
import subprocess
import matplotlib.pyplot as plt
import serial
import time
import argparse
import tools

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--year', type=int, default=2018, help='Date of the video (year)')
    parser.add_argument('--month', type=int, default=4, help='Date of the video (month)')
    parser.add_argument('--day', type=int, default=21, help='Date of the video (day)')
    
    parser.add_argument('--serial', type=str, default='/dev/ttyACM0', help='Serial port to use')
    parser.add_argument('--vidpath', type=str, default='videos/', help='Path to save videos')
    parser.add_argument('--dfpath', type=str, default='dataframes/', help='Path to save dataframe containing measurements')
    parser.add_argument('--seqpath', type=str, default='sequences/', help='Path to save sequences')
    
    parser.add_argument('--red', type=int, default=30, help='Sensitivity of the RED channel')
    parser.add_argument('--green', type=int, default=30, help='Sensitivity of the GREEN channel')
    parser.add_argument('--blue', type=int, default=30, help='Sensitivity of the BLUE channel')
    parser.add_argument('--lower_s', type=float, default=0, help='Lower limit of the S channel')
    parser.add_argument('--lower_v', type=float, default=0, help='Lower limit of the V channel')
    parser.add_argument('--nled', type=int, default=11, help='How many LEDs do you have in your cathedral?')
    parser.add_argument('--boost_green', type=bool, default=False, help='Should I boost the green color?')
    
    parser.set_defaults()
    args = parser.parse_args()

    nx = ny = args.nled
    
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

    r_chs = ['r{}'.format(i) for i in np.arange(args.nled)]
    g_chs = ['g{}'.format(i) for i in np.arange(args.nled)]
    b_chs = ['b{}'.format(i) for i in np.arange(args.nled)]

    frame_no = 0
    while True:
        ok, frame_original = video.read()
        if not ok:
            break
        
        # Start timer
        timer = cv2.getTickCount()

        frame_bgr = frame_original[0:500, 180:680] # specific to this dataset
        frame_bgr = frame_bgr[50:450, 50:450] # specific to this dataset

        # # increase contrast
        # lab = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2LAB)
        # l, a, b = cv2.split(lab)
        # clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        # cl = clahe.apply(l)
        # limg = cv2.merge((cl,a,b))
        # frame_bgr = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        
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
        
        with serial.Serial(args.serial, 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE) as ser:
            if args.boost_green:
                col_seq_rgb, row_seq_rgb = tools.img2seq(res_g_rgb, shape)
                seq_rgb = row_seq_rgb
            else:
                col_seq_rgb, row_seq_rgb = tools.img2seq(res_all_rgb, shape)
                seq_rgb = row_seq_rgb
            
            values = bytearray(seq_rgb)
            ser.write(values)

        # write all measurements to a dataframe
        df_line = [vname, frame_no, flux_r, flux_g, flux_b, area_r, area_g, area_b]
        for i in range(len(seq_rgb)):
            df_line.append(seq_rgb[i])
        df.loc[frame_no] = df_line
                
        # output the original and filtered frames
        # cv2.putText(res_r_bgr, "frame {}".format(frame_no), (150,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,250), 2)
        # cv2.imshow("red", res_r_bgr)
        # cv2.putText(res_g_bgr, "frame {}".format(frame_no), (150,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,250), 2)
        # cv2.imshow("green", res_g_bgr)
        # cv2.putText(res_b_bgr, "frame {}".format(frame_no), (150,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,250), 2)
        # cv2.imshow("blue", res_b_bgr)
        cv2.putText(frame_bgr, "frame {}".format(frame_no), (150,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,250), 2)
        cv2.imshow("BGR", frame_bgr)
        cv2.putText(res_all_bgr, "frame {}".format(frame_no), (150,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,250), 2)
        cv2.imshow("res all", res_all_bgr)
        
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            df.to_csv(os.path.join(args.dfpath, vname.replace('.mp4', '.csv'), index=False))
            break
        
    df['r_seq'] = df['frame_no'].apply(lambda fno: np.array([df.loc[df.frame_no==fno, ch].values[0] for ch in r_chs]))
    df['g_seq'] = df['frame_no'].apply(lambda fno: np.array([df.loc[df.frame_no==fno, ch].values[0] for ch in g_chs]))
    df['b_seq'] = df['frame_no'].apply(lambda fno: np.array([df.loc[df.frame_no==fno, ch].values[0] for ch in b_chs]))
    df.to_csv(os.path.join(args.dfpath, vname.replace('.mp4', '.csv')), index=False)

    # write the nonzero sequences into separate files /per channel)
    for channel in ['r', 'g', 'b']:
        print('writing sequences of channel {}'.format(channel))
        outpath = os.path.join(args.seqpath, 'seq_{}.csv'.format(channel))
        Channelmax = tools.write_sequences(df['frame_no'].min(), df['frame_no'].max(), df, channel, outpath)
        
if __name__ == "__main__":
    main()
