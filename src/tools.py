from math import *
import random
import cv2
import sys
import numpy as np
import os
import subprocess
import matplotlib.pyplot as plt
import serial
import time
from scipy.signal import savgol_filter

def pad(n):
    if n<10:
        return "0{}".format(n)
    else:
        return "{}".format(n)

def download_video(year, month, day, dlpath):
    vidpath = os.path.join(dlpath,"auroramaxHD_{}{}{}_480p.mp4".format(year, pad(month), pad(day)))
    url = "http://data.phys.ucalgary.ca/sort_by_project/AuroraMAX/rt-movies/mp4/{}/{}/{}/yknf_slr-12/auroramaxHD_{}{}{}_480p.mp4".format(year, pad(month), pad(day), year, pad(month), pad(day))
    if not os.path.exists(vidpath):
        try:
            subprocess.call("wget -O {} {}".format(vidpath, url), shell=True)
        except:
            print("{} does not exist!".format(url))
        else:
            print("{} exists!".format(vidpath))
    return vidpath

def speedup_video(input_path, output_path, conversion_factor=0.05):
    if not os.path.exists(output_path):
        try:
            subprocess.call("mencoder -speed {} -o {} -ovc lavc {}".format(conversion_factor, output_path, input_path),
                            shell=True, stdout=open(os.devnull, 'wb'))
        except:
            print("{} does not exist!".format(input_path))
        else:
            print("{} exists!".format(output_path))
    
    
def read_video(video_path):
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print("Could not open video")
        sys.exit()
    return video

def get_filters(args):
    """
    OpenCV's HSV ranges are:
    H: 0-179
    S: 0:255
    V: 0-255
    Along both S and V axes, anything less than 256/4 are essentially 
    while and black, respectively.    
    """
    filters = {
        'red': {
            'lower': np.array([0 - args.red, args.lower_s, args.lower_v]),
            'upper': np.array([0 + args.red, 255, 255])
        },
        'green':{
            'lower': np.array([60 - args.green, args.lower_s, args.lower_v]),
            'upper': np.array([60 + args.green, 255, 255])
        },
        'blue': {
            'lower': np.array([120 - args.blue, args.lower_s, args.lower_v]),
            'upper': np.array([120 + args.blue, 255, 255])
        },
        'all': {
            'lower': np.array([0, args.lower_s, args.lower_v]),
            'upper': np.array([180, 255, 255])
        }        
    }
    return filters

def apply_filter_to(frame_hsv, use_filter): #kind of an arbitrary limit, but see https://en.wikipedia.org/wiki/HSL_and_HSV#HSV for the logic
    mask = cv2.inRange(frame_hsv, use_filter['lower'], use_filter['upper'])
    res = cv2.bitwise_and(frame_hsv,frame_hsv, mask=mask)
    flux = np.sum(res[:,:,2])*1.
    area = len(np.nonzero(res[:,:,2])[0])
    return mask, res, flux, area

def split_frame(frame_bgr, shape):
    frames = []
    nx, ny = shape
    W, H = frame_bgr[:,:,0].shape
    w = W//nx
    h = H//ny
    for i in np.arange(nx):
        for j in np.arange(ny):
            frames.append(frame_bgr[i*w:(i+1)*w, j*h:(j+1)*h])
    return frames

def img2seq(frame_rgb, shape, args):
    split_frames = split_frame(frame_rgb, shape)
    r = np.zeros((shape[0]*shape[1]))
    g = np.zeros((shape[0]*shape[1]))
    b = np.zeros((shape[0]*shape[1]))
    for i, frame in enumerate(split_frames):
        r[i] = np.median(frame[:,:,0])
        g[i] = np.median(frame[:,:,1])
        b[i] = np.median(frame[:,:,2])        
    r = r.reshape(shape)
    g = g.reshape(shape)
    b = b.reshape(shape)
    seq = []    
    for row in range(shape[0]):
        if args.boost_green:
            rgb = np.uint8([[[np.median(r[row,:]), g[row,:].sum(), np.median(b[row,:])]]])[0][0]
        else:
            rgb = np.uint8([[[np.median(r[row,:]), np.median(g[row,:]), np.median(b[row,:])]]])[0][0]

        for e in rgb:
            seq.append(e)
    return seq
    
def color_scale(col, df, inplace=True):
    if not inplace:
        res = df[col].copy()
        res -= res.min()
        res /= res.max()
        res *= 255
        return res        
    else:
        df[col] -= df[col].min()
        df[col] /= df[col].max()
        df[col] *= 255 
    
def minmax_scale(col, df, inplace=True):
    if not inplace:
        res = df[col].copy()
        res -= res.min()
        res /= res.max()
        return res        
    else:
        df[col] -= df[col].min()
        df[col] /= df[col].max()

def write_sequences(frame_start, frame_stop, data, channel, outpath):
    Channelmax = 0
    for i in range(frame_start, frame_stop):
        with open(outpath, 'r+') as f:
            a = data['{}_seq'.format(channel)].values[i]
            if not all([ v == 0 for v in a ]):
                f.write('{} {} {} {} {} {} {} {} {} {} {}'.format(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10]))
            Channelmax = max(Channelmax, max(data['{}_seq'.format(channel)].values[i]))
    return Channelmax

def write_sequences(frame_start, frame_stop, data, channel, f):
    for i in range(frame_start, frame_stop):
        a = data['{}_seq'.format(channel)].values[i]
        if not all([ v == 0 for v in a ]):
            f.write('{} {} {} {} {} {} {} {} {} {} {}\n'.format(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10]))

def load_templates(filepath):
    return np.genfromtxt(filepath, delimiter=' ', dtype='int')
            
