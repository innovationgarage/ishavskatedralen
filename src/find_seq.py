from math import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import savgol_filter
import os
import sys

def plot_sequences(frame_start, frame_stop, data):
    fig, axs = plt.subplots(3,1, sharex=True, sharey=True)
    axs = axs.flatten()    
    for i in range(frame_start, frame_stop):
        axs[0].plot(range(11), data.r_seq.values[i], '-', lw=1)
        gs = axs[1].plot(range(11), data.g_seq.values[i], '-', label=i, lw=3)
        axs[2].plot(range(11), data.b_seq.values[i], '-', lw=2)
        plt.suptitle('{}:{}'.format(frame_start, frame_stop))
        plt.savefig(os.path.join('sequences', '{}-{}.jpg'.format(frame_start, frame_stop)))

def write_sequences(frame_start, frame_stop, data, channel):
    Rmax = 0
    Gmax = 0
    Bmax = 0
    for i in range(frame_start, frame_stop):
        # print('{}'.format(i))
        a = data['{}_seq'.format(channel)].values[i]
        if not all([ v == 0 for v in a ]):
            print('{} {} {} {} {} {} {} {} {} {} {}'.format(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10]))
        # print('R: {}'.format(data.r_seq.values[i]))
        # print('G: {}'.format(data.g_seq.values[i]))
        # print('B: {}'.format(data.b_seq.values[i]))
        Rmax = max(Rmax, max(data.r_seq.values[i]))
        Gmax = max(Gmax, max(data.g_seq.values[i]))
        Bmax = max(Bmax, max(data.b_seq.values[i]))
    return Rmax, Gmax, Bmax

#date = '20180403'
date = sys.argv[1]
channel = sys.argv[2]
mpath = './dataframes/auroramaxHD_{}_480p.csv'.format(date)

original = pd.read_csv(mpath)

n = 11
r_chs = ['r{}'.format(i) for i in np.arange(n)]
g_chs = ['g{}'.format(i) for i in np.arange(n)]
b_chs = ['b{}'.format(i) for i in np.arange(n)]

original['flux_total'] = original.flux_r + original.flux_g + original.flux_b
original['area_total'] = original.area_r + original.area_g + original.area_b
original['r_seq'] = original['frame_no'].apply(lambda fno: np.array([original.loc[original.frame_no==fno, ch].values[0] for ch in r_chs]))
original['g_seq'] = original['frame_no'].apply(lambda fno: np.array([original.loc[original.frame_no==fno, ch].values[0] for ch in g_chs]))
original['b_seq'] = original['frame_no'].apply(lambda fno: np.array([original.loc[original.frame_no==fno, ch].values[0] for ch in b_chs]))

data = original.copy()

frame_length = 10
Rmax = 0
Gmax = 0
Bmax = 0
for frame_start in np.arange(0, data.frame_no.max()-frame_length, frame_length):
    frame_stop = frame_start + frame_length
    Rtmp, Gtmp, Btmp = write_sequences(frame_start, frame_stop, data, channel)
    Rmax = max(Rmax, Rtmp)
    Gmax = max(Gmax, Gtmp)
    Bmax = max(Bmax, Btmp)

    # print(Rmax, Gmax, Bmax)
