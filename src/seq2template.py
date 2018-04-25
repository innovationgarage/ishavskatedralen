from math import *
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import random
import clustering_tools
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', type=str, default='sequences/', help='Path to the sequences (single file name or directory of files) to use for clustering')
    parser.add_argument('--dst', type=str, default='templates/', help='Path to the templates (dir)')
    parser.add_argument('--color', type=str, default='g', help='Which color channel to use? (r/g/b)')
    parser.add_argument('--n_cluster', type=int, default=25, help='How many templates do you wish to have')
    parser.add_argument('--n_iter', type=int, default=10, help='How many iterations in clustering?')
    parser.add_argument('--window', type=int, default=11, help='Window size used in calculating similarity between sequences')

    parser.set_defaults()
    args = parser.parse_args()

    if os.path.isdir(args.src):
        for seq_file in os.listdir(args.src):
            filename, file_extension = os.path.splitext(seq_file)
            if filename.split('_')[-1] == args.color:
                i = 0
                print(seq_file)
                if i == 0:
                    data = np.genfromtxt(os.path.join(args.src, seq_file), delimiter=' ')
                else:
                    vid = np.genfromtxt(os.path.join(args.src, seq_file), delimiter=' ')
                    data = np.vstack((data, vid))
                i += 1
    elif os.path.isfile(args.src):
        data = np.genfromtxt(args.src, delimiter=' ')
        
    centroids = clustering_tools.k_means_clust(data, args.n_cluster, args.n_iter, args.window)

    with open(os.path.join(args.dst, 'template_{}.csv'.format(args.color)), 'w+') as f:
        for c in centroids:
            for j in c:
                f.write('{} '.format(int(round(j,0))))
            f.write('\n')

if __name__ == "__main__":
    main()
            
