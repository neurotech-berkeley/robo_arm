import numpy as np
import pandas as pd 
import mne
import ipdb

path = './data/'
fname = path + '2023-02-24_01:20:34'
ch_names = ['Ch. 2']
# data = pd.read_csv(path + '2023-02-24_01:20:34.csv', skiprows=0, usecols=['Sample', 'Ch. 1', 'Ch. 2', 'Ch. 3', 'Ch. 4', 'Time', 'Marker']) 
# data = pd.read_csv(path + '2023-02-24_01:20:34.csv', skiprows=0, usecols=['Sample', 'Ch. 2', 'Time', 'Marker']) 
data = pd.read_csv(fname + '.csv', skiprows=0, usecols=['Ch. 2', 'Marker']) 
data = pd.read_csv(fname + '.csv', skiprows=0, usecols=['Ch. 2']) 
# ch_names = ['Ch. 2', 'Marker']

sfreq = 200

# ipdb.set_trace()

data['Ch. 2'] = data['Ch. 2'] * 1e-6
# data["Marker"] = data["Marker"] * 10
info = mne.create_info(ch_names = ch_names, sfreq = sfreq)
raw = mne.io.RawArray(data.T, info)
# raw.filter(1,50, method='iir')

mne.viz.plot_raw_psd(raw)

raw[0].compute_psd().plot()

# fig = raw.plot_psd()

# raw.plot(color=dict(misc='r', eeg='k'))
# raw.export(fname + ".edf")