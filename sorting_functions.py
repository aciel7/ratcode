


import tdt
import numpy as np
import scipy
import matplotlib.pyplot as plt

def load_stim_data(path):
    data = tdt.read_block(path)
    stim_sig = data.streams.sSig.data
    cortex_sig = data.streams.Wav2.data
    return stim_sig, cortex_sig


def butt_filter_the_data(rawCortex, order, low, high):
    sos = scipy.signal.butter(order, [low, high], btype="bandpass", output='sos', fs = 24414)
    filtered_signal = scipy.signal.sosfilt(sos, rawCortex)
    return filtered_signal

def detect_spikes(cortex_sig, stim_times):
    sigma = np.median(np.abs(cortex_sig)/.6745, axis = 1, keepdims=True) * 2
#     sigma = np.array([49.3289,
# 48.9159,
# 49.4135,
# 50.5105,
# 52.241,
# 51.5511,
# 57.0806,
# 70.4903,
# 92.258,
# 84.6244,
# 82.2446,
# 76.3133,
# 53.5464,
# 55.5925,
# 89.7998,
# 63.3863,], ndmin=2)
    spikes = np.where(cortex_sig>sigma, cortex_sig, 0)
    
    spike_times = [[], [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],]
    spike_waveforms = [[], [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],]
    
    
    for i in range(spikes.shape[0]):
        print(i)
        for j in range(spikes[i, :].shape[0]-1):
            if spikes[i, j] == 0 and spikes[i, j+1] != 0:
                spike_times[i].append(j+1)
                
    for i in range(len(spike_times)):
        for j in range(len(spike_times[i])):
            spike_waveforms[i].append(cortex_sig[i, spike_times[i][j]-40:spike_times[i][j]+60])
    z = np.zeros((1))
    for i in range(100):
        z = np.concatenate((z,  np.array(spike_times[5])[np.logical_and(np.array(spike_times[5])<stim_times[10, i]+2400, np.array(spike_times[5])>stim_times[10, i]-2400)]-stim_times[10, i]))
    
    return z, spikes, spike_times, spike_waveforms 
    