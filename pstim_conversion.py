import os
import tdt
import numpy as np
from scipy.signal import butter, sosfilt
from scipy import signal
from scipy import stats
import matplotlib.pyplot as plt


def convert(cblocks, names):
    for cblock, name in zip(cblocks, names):
        data = tdt.read_block("./" + blocklist[cblock]) #LH: 21, 43 | RH: 66, 87
        
        cort = data.streams.Wav2.data.astype(float)
        stim = data.streams.sSig.data
        
        def butter_bandpass(lowcut, highcut, fs, order=5):
                nyq = 0.5 * fs
                low = lowcut / nyq
                high = highcut / nyq
                sos = butter(order, [low, high], analog=False, btype='band', output='sos')
                return sos
        
        def butter_bandpass_filter(data, lowcut, highcut, fs = 24414.0625, order=6):
                sos = butter_bandpass(lowcut, highcut, fs, order=order)
                y = sosfilt(sos, data)
                return y
        
        
        for i in range(16):    
            b_notch, a_notch = signal.iirnotch(60, 30, 24414.0625)
            cort[i, :] = signal.filtfilt(b_notch, a_notch, cort[i, :])
            cort[i, :] = butter_bandpass_filter(cort[i, :], 2, 1000, 24414.0625)
            cort[i, :] = stats.zscore(cort[i, :])
            
        import copy
        
        
        
        stimChans = np.where(stim)[0][::10]
        stimTimes = np.where(stim)[1][::10]
        
        deletion_array = []
        for i in range(stimTimes.shape[0] - 1):
            if stimTimes[i+1] - stimTimes[i] < 200 and stimChans[i+1] == stimChans[i]:
                deletion_array.append(i)
        
        stimTimes = np.delete(stimTimes, deletion_array)
        
        
        vchans = []
        
        for i in range(len(stimTimes)):
            vchans.append(np.where(stim[:, stimTimes[i]])[0])
        
        vChans = []
        
        for i in range(len(vchans)):
            vChans.append(hash(str(vchans[i][0])) + hash(str(vchans[i][1])))
        
        
        mapMask = np.arange(15)
        stimChans = vChans
        
        uniq = np.unique(stimChans)
        for i in range(len(stimChans)):
            for j in range(15):
                if stimChans[i] == uniq[j]:
                    stimChans[i] = mapMask[j]
        
        
        unique_first_val = np.unique(stimTimes, return_index=True)[1]
        
        stimTimes = np.delete(stimTimes, unique_first_val)
        stimChans = np.delete(stimChans, unique_first_val)
        ogstimChans = np.where(stim[:, stimTimes])[0]
        
        ogstimChans = np.delete(ogstimChans, unique_first_val)
        
        
        
        lc = np.zeros((15, 5)).astype(int)
        pstim = np.zeros((15, 5, 50, 16, 7500)) #15 virtual stim channels, 5 amplitudes, 50 trials, 16 cortical channels, 5000 samples (~200ms)
        for i in range(stimChans.shape[0]):
            if np.abs(stim[ogstimChans[i], stimTimes[i]]) == 7:
                pstim[stimChans[i], 0, lc[stimChans[i], 0], :, :] = cort[:, stimTimes[i]-2500:stimTimes[i]+5000]
                lc[stimChans[i], 0] += 1
            elif np.abs(stim[ogstimChans[i], stimTimes[i]]) == 12:
                pstim[stimChans[i], 1, lc[stimChans[i], 1], :, :] = cort[:, stimTimes[i]-2500:stimTimes[i]+5000]
                lc[stimChans[i], 1] += 1
            elif np.abs(stim[ogstimChans[i], stimTimes[i]]) == 20:
                pstim[stimChans[i], 2, lc[stimChans[i], 2], :, :] = cort[:, stimTimes[i]-2500:stimTimes[i]+5000]
                lc[stimChans[i], 2] += 1
            elif np.abs(stim[ogstimChans[i], stimTimes[i]]) == 30:
                pstim[stimChans[i], 3, lc[stimChans[i], 3], :, :] = cort[:, stimTimes[i]-2500:stimTimes[i]+5000]
                lc[stimChans[i], 3] += 1
            elif np.abs(stim[ogstimChans[i], stimTimes[i]]) == 40:
                pstim[stimChans[i], 4, lc[stimChans[i], 4], :, :] = cort[:, stimTimes[i]-2500:stimTimes[i]+5000]
                lc[stimChans[i], 4] += 1
        
        for vchan in range(pstim.shape[0]):
            for amp in range(pstim.shape[1]):
                for trial in range(pstim.shape[2]):
                    if np.sum(pstim[vchan, amp, trial, :, :] ) == 0:
                          
                        print(vchan)
                        print(trial)
                        print()
                        pstim[vchan, amp, trial, :, :] = pstim[vchan, amp, 5, :, :]
        
        
        pstim = signal.decimate(pstim, 10, axis = -1, zero_phase=True)
        np.save(r"C:\Users\ghakc\Desktop\Analysis\pstims/" + name + str(cblock, ), pstim)




os.chdir(r"C:\Users\ghakc\Desktop\Analysis\2OCT23")
blocklist = []
for _, blocks, _ in os.walk("./"):
    for block in blocks:
        blocklist.append(block)
blocklist.sort()
# blocklist.pop(0)

convert([4, 5], ["703_", "703_"])
convert ([35], ["177_"])



os.chdir(r"C:\Users\ghakc\Desktop\Analysis\12DEC23")
blocklist = []
for _, blocks, _ in os.walk("./"):
    for block in blocks:
        blocklist.append(block)
blocklist.sort()
blocklist.pop(0)

convert([7, 18], ["177_", "177_"])
convert([20], ["703_"])



os.chdir(r"C:\Users\ghakc\Desktop\Analysis\18DEC23")
blocklist = []
for _, blocks, _ in os.walk("./"):
    for block in blocks:
        blocklist.append(block)
blocklist.sort()
blocklist.pop(0)

convert([21, 43], ["703_", "703_"])
convert([66], ["177_"])



os.chdir(r"C:\Users\ghakc\Desktop\Analysis\20DEC23")
blocklist = []
for _, blocks, _ in os.walk("./"):
    for block in blocks:
        blocklist.append(block)
blocklist.sort()
# blocklist.pop(0)

convert([10], ["177_"])
convert([45], ["703_"])







