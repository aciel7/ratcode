import spikeinterface.full as si
import spikeinterface.extractors as se
import spikeinterface.preprocessing as spre
import spikeinterface.sorters as ss
import spikeinterface.postprocessing as spost
import spikeinterface.qualitymetrics as sqm
import spikeinterface.comparison as sc
import spikeinterface.exporters as sexp
import spikeinterface.curation as scur
import spikeinterface.widgets as sw
import tdt
import matplotlib.pyplot as plt
print("test")
recording = si.read_tdt("/home/lambda/Desktop/Rats/Acute_052323-230523-171410/", stream_name="b'Wav2'")
recording = si.read_tdt("/home/lambda/Desktop/Rats/Acute_052323-230523-171410/", stream_name="b'Wav2'")

#%%
data = tdt.read_block("/home/lambda/Desktop/Rats/Acute_052323-230523-171410/Exp_BL-230523-213247")

#%%

w_ts = sw.plot_timeseries(recording, time_range=(0, 100), segment_index = 8)

