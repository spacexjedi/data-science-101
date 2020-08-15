import os.path as op

import mne

"""how epoch array works
https://mne.tools/0.14/auto_tutorials/plot_visualize_epochs.html
"""

data_path = op.join(mne.datasets.sample.data_path(), 'MEG', 'sample')
raw = mne.io.read_raw_fif(op.join(data_path, 'sample_audvis_raw.fif'))
raw.set_eeg_reference()  # set EEG average reference
event_id = {'auditory/left': 1, 'auditory/right': 2, 'visual/left': 3,
            'visual/right': 4, 'smiley': 5, 'button': 32}
events = mne.read_events(op.join(data_path, 'sample_audvis_raw-eve.fif'))
epochs = mne.Epochs(raw, events, event_id=event_id, tmin=-0.2, tmax=1.)
