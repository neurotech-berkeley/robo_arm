import numpy as np
import pandas as pd 
import mne
import ipdb
import matplotlib.pyplot as plt


path = './data/'
# fname = path + '2023-02-24_01:20:34'
fname = path + '2023_03_05_19_21_01'
ch_names = ['Ch. 2', 'Marker']

df = pd.read_csv(fname+'.csv', skiprows=0, usecols=ch_names)


plt.figure(figsize=(100,8), dpi=180)
plt.plot(df['Ch. 2'])
plt.plot(df['Marker']*10, color='red')
plt.savefig(fname+'.png')



