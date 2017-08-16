"""
ERP analysis EEG submodule.
"""
from .eeg_data import eeg_select_sensor_area
from .eeg_data import eeg_to_df

import numpy as np
import pandas as pd
import mne
import matplotlib



# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
def eeg_erp(eeg_data, windows=None, index=None, include="all", exclude=None, hemisphere="both", include_central=True, verbose=True, names="ERP"):
    """
    """
    erp = {}

    data = eeg_to_df(eeg_data, index=index, include=include, exclude=exclude, hemisphere=hemisphere, include_central=include_central)

    windows = ([0.15, 0.25], [0.25, 0.35])
    names=["A", "B"]
    for epoch_index, epoch in data.items():
        # Segment according to window
        if isinstance(windows, list):
            df = epoch[windows[0]:windows[1]]
            value = df.mean().mean()
            erp[epoch_index] = [value]
        elif isinstance(windows, tuple):
            values = {}
            for window_index, window in enumerate(windows):
                df = epoch[window[0]:window[1]]
                value = df.mean().mean()
                values[window_index] = value
            erp[epoch_index] = values
        else:
            df = epoch[0:]
            value = df.mean().mean()
            erp[epoch_index] = [value]

    # Convert to dataframe
    erp = pd.DataFrame.from_dict(erp, orient="index")
    if isinstance(names, str):
        names = [names]
    erp.columns = names

    return(erp)


# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
def plot_eeg_erp(eeg_data, colors=None, include="all", exclude=None, hemisphere="both", include_central=True):
    """
    """
    all_evokeds = {}
    for participant, epochs in eeg_data.items():
        for cond, epoch in epochs.items():
            all_evokeds[cond] = []
    for participant, epochs in eeg_data.items():
        for cond, epoch in epochs.items():
            all_evokeds[cond].append(epoch)


    picks = mne.pick_types(epoch.info, eeg=True, selection=eeg_select_sensor_area(include=include, exclude=exclude, hemisphere=hemisphere, include_central=include_central))

    plot = mne.viz.plot_compare_evokeds(all_evokeds, picks, colors=colors, title="")
    return(plot)





# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
def eeg_topo_erp(evoked, line_colors=("red"), line_width=0.5, background_color="black", font_color="white", save=False, name="topo_erp", dpi=1000):
    """
    Plot butturfly plot.
    """
    fig = mne.viz.plot_evoked_topo(evoked,
                               fig_facecolor=background_color,
                               axis_facecolor=background_color,
                               font_color=font_color,
                               show=False,
                               color=line_colors)

    fig.subplots_adjust(hspace=5)  # Not sure it changes anything though.
    for line in fig.findobj(matplotlib.lines.Line2D):
        line.set_linewidth(line_width)

    fig.show()
    if save == True:
        fig.savefig(name + ".png", format='png', dpi=dpi)





# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
def eeg_average_per_epoch(epochs, include="all", exclude=None, hemisphere="both", include_central=True, time_start=0, time_end=0.4, fill_bads="NA"):
    """
    """
#    epochs.pick_channels(eeg_select_electrodes("CP"))
    epochs = epochs.copy().pick_channels(eeg_select_sensors(include=include, exclude=exclude, hemisphere=hemisphere, include_central=include_central))

    dropped = list(epochs.drop_log)

    dfraw = epochs.to_data_frame(index=["epoch", "time", "condition"])

    dfraw = dfraw.reset_index()
    dfraw = dfraw[(dfraw.time >= time_start*1000) & (dfraw.time <= time_end*1000)]

    average_list = []
    n_epoch = 0
    for event_type in enumerate(dropped):
        if event_type[1] == []:
            subset = dfraw[dfraw.epoch == n_epoch]
            subset = subset.drop(["epoch", "time", "condition"], 1)
            signal = subset.mean(axis=1)
            signal = np.mean(signal)
            average_list.append(signal)
            n_epoch += 1
        else:
            if fill_bads == "NA":
                average_list.append(np.nan)
            else:
                average_list.append(fill_bads)

    return(average_list)
