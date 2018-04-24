from math import *
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import random
from clustering_tools import *
        
# vid1 = np.genfromtxt('datasets/20180406.csv', delimiter=' ')
# vid2 = np.genfromtxt('datasets/20180420.csv', delimiter=' ')
# vid3 = np.genfromtxt('datasets/20180420.csv', delimiter=' ')
# vid4 = np.genfromtxt('datasets/20180412.csv', delimiter=' ')
# vid5 = np.genfromtxt('datasets/20180422.csv', delimiter=' ')
# vid6 = np.genfromtxt('datasets/20180321.csv', delimiter=' ')

# data = np.vstack((vid1[:,:],vid2[:,:],vid3[:,:],vid4[:,:],vid5[:,:],vid6[:,:]))

data = np.genfromtxt('datasets/20180421g.csv', delimiter=' ')

num_clust = 250
num_iter = 10
w = 1

centroids = k_means_clust(data,num_clust,num_iter,w)

fig, axs = plt.subplots(ceil(num_clust/4), 4, sharex=True, sharey=True)
axs = axs.flatten()

with open('templates_g.csv', 'w+') as f:
    for c in centroids:
        for j in c:
            f.write('{} '.format(int(round(j,0))))
        f.write('\n')

for i in range(num_clust):
    axs[i].plot(centroids[i])
    axs[i].set_title('{}'.format(ceil(max(centroids[i]))))
        
plt.show()
