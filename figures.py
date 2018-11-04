#!/usr/bin/env python
#activate mne
import mne
import mne.channels
import mne.viz
import matplotlib.pyplot as plt
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




antelope = LinearSegmentedColormap('Antelope', cdict3)
plt.register_cmap(cmap = antelope)


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
        fig, axs = plt.subplots(1, 1, figsize=(5, 5))
        f=mne.viz.plot_topomap(data = subsub.correlation, 
                               axes=axs,
                               pos=info,
                               mask=np.array([True for x in data]),
                               vmin=-0.25,
                               vmax=+0.5,
                               sensors=True,
                               show=False,
                               show_names=True,
                               res=1000,
                               names=subsub.Channel,
                               outlines="head",
                               contours=10,
                               image_interp="nearest",
                               #cmap=plt.get_cmap("jet"),  # seismic
                               cmap=antelope,  # seismic
                               mask_params=dict(marker='o', markerfacecolor='white',
                                                markeredgecolor='k', linewidth=0,
                                                markersize=15))

        fig.colorbar(f[0], cmap='GreyRed2')
        bname = band.replace("_", "")
        plt.title("%s\n%s band, %s" % (task,
                                       expand_camel(bname),
                                       bands[bname]))
        plt.savefig("antelope_%s_%s.png" % (task, band))
        


