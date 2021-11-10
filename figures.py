#!/usr/bin/env python
#activate mne
import mne
import mne.channels
import mne.viz
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import gridspec
import numpy as np
import pandas as pd
import string

from matplotlib.colors import LinearSegmentedColormap, ListedColormap, Colormap


bands = {"Delta" : "0 - 3.5Hz",
         "Theta" : "4 - 7.5Hz",
         "Alpha" : "8 - 12.5Hz",
         "LowBeta" : "13 - 14.5Hz",
         "UpperBeta" : "15 - 17.5Hz",
         "HighBeta" : "18 - 29.5Hz",
         "Gamma" : "30 - 40Hz",
         "CombinedBeta" : "13-30Hz"}

def expand_camel(str):
    "Expands a camel notation string"
    word = str[0]
    for char in str[1:]:
        if char in string.ascii_lowercase:
            word += char
        else:
            word += " "
            word += char
    return word


# Read the data
data = pd.read_csv("Forgetting_Rate_CorResults_updated.csv")
data['Channel'] = [x.split("_")[1] for x in data['id']]



#mne.viz.plot_topomap(data, info, vmin=-1, vmax=+1, show_names=True, names=channels)

cdict1 = {'red':  ((0.0, 0.0, 0.0),
                   (0.8, 1.0, 1.0),
                   (1.0, 1.0, 1.0)),

         'green': ((0.0, 0.0, 0.0),
                   (0.8, 1.0, 1.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 0.0, 0.0),
                   (0.8, 1.0, 1.0),
                   (1.0, 0.0, 0.0))
        }


cdict2 = {'red':  ((0.0, 1.0, 1.0),
                   (0.7, 0.3, 0.3),
                   (1.0, 1.0, 1.0)),

         'green': ((0.0, 1.0, 1),
                   (0.7, 0.3, 0.3),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 1.0, 1.0),
                   (0.7, 0.3, 0.3),
                   (1.0, 0.0, 0.0))
        }

cdict3 = {'red':  ((0.0, 1, 0),
                   (0.33, 1.0, 1.0),
                   (0.66, 1.0, 1.0),
                   (0.86, 1.0, 1.0),
                   (1.0, 1.0, 1.0)),

         'green': ((0.0, 1, 1),
                   (0.33, 1.0, 1),
                   (0.66, 1.0, 1),
                   (0.86, 0.7, 0.7),  
                   (1.0, 0.2, 0.2)),

         'blue':  ((0.0, 1, 1),
                   (0.33, 1.0, 1),
                   (0.66, 1.0, 1),
                   (0.86, 0.2,  0.2),
                   (1.0, 0.2, 0.2))
        }

cdict4 = {'red':  ((0.0, 0, 1),
                   (0.7, 1.0, 1.0),
                   (0.86, 1.0, 1.0),
                   (1.0, 1.0, 1.0)),

         'green': ((0.0, 1, 1),
                   (0.7, 1.0, 1),
                   (0.86, 0.7, 0.2),  
                   (1.0, 0.2, 0.2)),

         'blue':  ((0.0, 1, 1),
                   (0.7, 1.0, 0.2),
                   (0.86, 0.2,  0.2),
                   (1.0, 0.2, 0.2))
        }



font = {'fontname' : 'FreeSans',
        'fontweight' : 'normal',
        'fontsize' : 12}


antelope = LinearSegmentedColormap('Antelope', cdict3)
plt.register_cmap(cmap = antelope)


## Generate individual figures

for task in set(data['task']):
    sub = data.loc[lambda x: x.task == task]
    print(task)
    
    for band in set(data['band']):
        subsub = sub.loc[lambda x: x.band == band]
        print("..." + band)
        montage = mne.channels.read_montage(kind="standard_1020")
        info = mne.create_info(ch_names=list(subsub.Channel),
                               sfreq=128,
                               ch_types="eeg",
                               montage=montage)
        fig, axs = plt.subplots(1, 1, figsize=(3, 3))
        
        f=mne.viz.plot_topomap(data = subsub.correlation, 
                               axes=axs,
                               pos=info,
                               mask=np.array([True for x in data]),
                               vmin=-0.25,
                               vmax=+0.5,
                               sensors=True,
                               show=False,
                               show_names=True,
                               res=100,
                               names=subsub.Channel,
                               outlines="head",
                               contours=10,
                               image_interp="nearest",
                               #cmap=plt.get_cmap("jet"),  # seismic
                               cmap=antelope,  # seismic
                               mask_params=dict(marker='o', markerfacecolor='white',
                                                markeredgecolor='k', linewidth=0,
                                                markersize=15))

        #fig.colorbar(f[0], cmap='GreyRed2')
        bname = band.replace("_", "")
        plt.title("%s\n%s band, %s" % (task,
                                       expand_camel(bname),
                                       bands[bname]),
                  **font)
        plt.savefig("antelope_%s_%s.png" % (task, band))

        
## Generate mix figure
        
fig = plt.figure(figsize=(16, 5))

i = 1

for task in set(data['task']):
    sub = data.loc[lambda x: x.task == task]
    print(task)
    gs = gridspec.GridSpec(2, 7, width_ratios=[1, 1, 1, 1, 1, 1, 0.15]) 
    for band in ['Theta', 'Alpha', 'LowBeta', 'UpperBeta', 'HighBeta', 'Gamma']:
        subsub = sub.loc[lambda x: x.band == band]
        print("..." + band)
        montage = mne.channels.read_montage(kind="standard_1020")
        info = mne.create_info(ch_names=list(subsub.Channel),
                               sfreq=128,
                               ch_types="eeg",
                               montage=montage)
        #fig, axs = plt.subplots(1, 1, figsize=(3, 3))
        #i=i+1
        if (i == 7):
            i = i + 1

        axs = plt.subplot(gs[i-1])

        f=mne.viz.plot_topomap(data = subsub.correlation, 
                               axes=axs,
                               pos=info,
                               mask=np.array([True for x in data]),
                               vmin=-0.25,
                               vmax=+0.5,
                               sensors=True,
                               show=False,
                               show_names=True,
                               res=100,
                               names=subsub.Channel,
                               outlines="head",
                               contours=10,
                               image_interp="nearest",
                               #cmap=plt.get_cmap("jet"),  # seismic
                               cmap=antelope,  # seismic
                               mask_params=dict(marker='o', markerfacecolor='white',
                                                markeredgecolor='k', linewidth=0,
                                                markersize=15))
            
        bname = band.replace("_", "")
        plt.title("%s\n%s band, %s" % (task,
                                       expand_camel(bname),
                                       bands[bname]),
                  **font)

        i = i + 1

    axs = plt.subplot(gs[6])
    #plt.subplots_adjust(left=0.1, right=0.2)
    norm = mpl.colors.Normalize(vmin=-0.2, vmax=0.5)
    cb1 = mpl.colorbar.ColorbarBase(axs, cmap=antelope,
                                    norm=norm,
                                    orientation='vertical')
    cb1.set_label(r"""Correlation (Spearman's ${\it r}$)""", **font)
    #plt.title("Correlation",
    #          **font)
            
        
fig.savefig("full6.png")

font = {'fontname' : 'FreeSans',
        'fontweight' : 'normal',
        'fontsize' : 15}


fontbold = {'fontname' : 'FreeSans',
            'fontweight' : 'bold',
            'fontsize' : 16}


plt.rcParams['font.sans-serif'] = ['FreeSans']

fig = plt.figure(figsize=(13, 5))

i = 1

for task in ["Vocabulary", "Location"]:
    sub = data.loc[lambda x: x.task == task]
    print(task)
    gs = gridspec.GridSpec(2, 6, width_ratios=[1, 1, 1, 1, 1, 0.15]) 
    for band in ['Theta', 'Alpha', 'LowBeta', 'UpperBeta', 'HighBeta']:
        subsub = sub.loc[lambda x: x.band == band]
        print("..." + band)
        montage = mne.channels.read_montage(kind="standard_1020")
        info = mne.create_info(ch_names=list(subsub.Channel),
                               sfreq=128,
                               ch_types="eeg",
                               montage=montage)
        #fig, axs = plt.subplots(1, 1, figsize=(3, 3))
        #i=i+1
        if (i == 6):
            i = i + 1

        axs = plt.subplot(gs[i-1])
        f=mne.viz.plot_topomap(data = subsub.correlation, 
                               axes=axs,
                               pos=info,
                               mask=np.array([True for x in data]),
                               vmin=-0.5,
                               vmax=+0.5,
                               sensors=True,
                               show=False,
                               show_names=True,
                               res=100,
                               names=subsub.Channel,
                               outlines="head",
                               contours=10,
                               image_interp="nearest",
                               cmap=plt.get_cmap("RdBu_r"),  # seismic
                               #cmap=antelope,  # seismic
                               mask_params=dict(marker='o', markerfacecolor='white',
                                                markeredgecolor='k', linewidth=0,
                                                markersize=15))
        f[0].set_background("blue")
            
        bname = band.replace("_", "")
        if i < 6:
            #plt.title(expand_camel(bname), **font)
            if i == 3:
                plt.title("Vocabulary", **fontbold)
        
        elif i > 6:
            if i == 9:
                plt.title("Maps", **fontbold)
            axs.set_xlabel(expand_camel(bname), **font)
            
        # Step forward
        i = i + 1

    axs = plt.subplot(gs[5])
    #plt.subplots_adjust(left=0.1, right=0.2)
    norm = mpl.colors.Normalize(vmin=-0.5, vmax=0.5)
    cb1 = mpl.colorbar.ColorbarBase(axs, cmap=plt.get_cmap("RdBu_r"), #antelope,
                                    norm=norm,
                                    orientation='vertical')
    cb1.set_label(r"""Correlation with $\alpha$""", **font)
    plt.tight_layout()        
    
fig.savefig("full5.png")

