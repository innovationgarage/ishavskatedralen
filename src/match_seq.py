from math import *
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import random
from clustering_tools import *
import sys

def load_templates(filepath):
    return np.genfromtxt(filepath,delimiter=' ')

def match_template(seq, centroids, w=5):
    min_dist = float('inf')
    closest_clust_ind = None
    closest_clust_arr = None
    for c_ind,j in enumerate(centroids):
        if LB_Keogh(seq,j,w)<min_dist:
            cur_dist = DTWDistance(seq,j,w)
            if cur_dist<min_dist:
                min_dist = cur_dist
                closest_clust_ind = c_ind
                closest_clust_arr = j
    return closest_clust_ind, closest_clust_arr

def main(seq, w=5):
    templates = load_templates('templates_g.csv')
    closest_clust_ind, closest_clust_arr = match_template(seq, templates, w=5)
    plt.figure()
    plt.plot(seq, label='original sequence')
    plt.plot(closest_clust_arr, label='closest template')
    plt.title(closest_clust_ind)
    plt.legend()
    plt.show()

alts = load_templates('datasets/20180406g.csv')
for seq in alts:
    main(seq, w=11)

    
