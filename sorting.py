from sorting_functions import * 
import numpy as np

stim_sig, cortex_sig = load_stim_data("C:\\Users\\ghakc\\Desktop\\Spike Sorting\\17AUG23_TEKAMAH\\ExperimentBL-230817-160221")
# stim_sig, cortex_sig = load_stim_data("C:\\Users\\ghakc\\Desktop\\Spike Sorting\\17AUG23_TEKAMAH\\ExperimentBL-230817-142403")
cortex_sig = cortex_sig[:16, :]
#%% Filter cortical data
cortex_sig_filt = butt_filter_the_data(cortex_sig, 5, 300, 3000)

#%% get stimulation onset times
stim_times = np.zeros((16, int(np.ceil(np.count_nonzero(stim_sig)/160))))
stim_amps = np.zeros((16, int(np.ceil(np.count_nonzero(stim_sig)/160))))

nzi = np.nonzero(stim_sig)[0][0::10]
nzt = np.nonzero(stim_sig)[1][0::10]

nzc = np.concatenate((nzi[:, np.newaxis], nzt[:, np.newaxis]), axis = 1)
counter = 0
for i in range(16):
    for j in range(np.unique(nzi, return_counts=True)[1][i]):
        stim_times[np.unique(nzi)[i], j] =  nzt[counter]
        counter += 1

for i in range(16):
    stim_amps[i, :] = stim_sig[i, stim_times[i,:].astype(np.int64)]

#%%
z, spikes, spike_times, spike_waveforms = detect_spikes(cortex_sig_filt, stim_times)

#%%
# plt.plot(cortex_sig[0, :])
plt.plot(cortex_sig_filt[0, :])
plt.vlines(stim_times[0, :], -stim_amps[0, :]*1000, stim_amps[0, :]*1000, colors='red')
# plt.xticks(np.arange(0, round(cortex_sig.shape[1]/2441.4), 1))
plt.show()





