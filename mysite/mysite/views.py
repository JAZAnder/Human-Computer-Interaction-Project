import base64
import json
from io import BytesIO

import plotly.graph_objs
from django.shortcuts import render
import mne
import os
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import numpy as np
from mne.conftest import event_id, tmin, tmax

from plotly.offline import plot
import plotly.io as pio
from mne.viz import plot_topomap, ica


def landing_view(request):
    return render(request, "upload.html")

def graph_1(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        temp_file_path = "raw.fif"
        with open(temp_file_path, 'wb+') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

        # Load the .fif file using MNE-Python
        raw = mne.io.read_raw_fif(temp_file_path)

        # Select EEG channels for plotting (you can customize this list)
        eeg_channels = ['MEG 001', 'MEG 002', 'MEG 003', 'MEG 004', 'MEG 005', 'MEG 006', 'MEG 007', 'MEG 008',
                        'MEG 009','MEG 010', 'MEG 0113', 'MEG 0111', 'MEG 0113', 'MEG 0122', 'MEG 0123', 'EEG 016', 'EEG 017',
                        'EEG 018']

        # Extract data from the selected EEG channels
        eeg_data, times = raw.copy().pick_channels(ch_names=eeg_channels).get_data(return_times=True)

        # Transpose the EEG data to match Plotly's expectations (channels x time)
        eeg_data = eeg_data.T

        # Create traces for each EEG channel
        traces = []
        for i, channel in enumerate(eeg_channels):
            traces.append(go.Scatter(x=times, y=eeg_data[i], mode='lines', name=channel))

        # Create a layout for the EEG plot
        layout = go.Layout(title='Dynamic EEG Plot', xaxis=dict(title='Time (s)'),
                           yaxis=dict(title='EEG Amplitude (uV)'), width=1300, height=600,)

        # Generate an HTML representation of the EEG plot
        plot_div = plot({'data': traces, 'layout': layout}, output_type='div', include_plotlyjs=True)
        os.remove(temp_file_path)

        return render(request, 'graph1.html',
                      {'plot_div': plot_div})
    return render(request, 'graph1_upload.html')


def graph_2(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        temp_file_path = "raw.fif"
        with open(temp_file_path, 'wb+') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

        # Load the .fif file using MNE-Python
        raw = mne.io.read_raw_fif(temp_file_path)

        # Extract events from the raw data
        events = mne.find_events(raw)

        # Create an event dictionary for labeling and coloring events

        # Calculate aud_evoked using MNE-Python
        epochs = mne.Epochs(raw, events, event_id, tmin, tmax, baseline=None, picks='eeg')
        aud_evoked = epochs.average()

        # Plot aud_evoked using Plotly
        aud_evoked_plot_data = []
        for i, ch_name in enumerate(aud_evoked.info['ch_names']):
            aud_evoked_plot_data.append(
                go.Scatter(x=aud_evoked.times, y=aud_evoked.data[i], mode='lines', name=ch_name))

        aud_evoked_layout = go.Layout(title='Auditory Evoked', xaxis=dict(title='Time (s)'),
                                      yaxis=dict(title='Amplitude'),width=1300,height=600)

        # Generate an HTML representation of the aud_evoked plot
        aud_evoked_plot_div = plot({'data': aud_evoked_plot_data, 'layout': aud_evoked_layout}, output_type='div',
                                   include_plotlyjs=True)
        os.remove(temp_file_path)

        return render(request, 'graph2.html',
                      {'aud_evoked_plot_div': aud_evoked_plot_div})
    return render(request, 'graph1_upload.html')

def graph_3(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        temp_file_path = "raw.fif"
        with open(temp_file_path, 'wb+') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

        # Load the .fif file using MNE-Python
        raw = mne.io.read_raw_fif(temp_file_path)

        # Extract events from the raw data
        events = mne.find_events(raw, stim_channel="STI 014")
        event_dict = {
            "auditory/left": 1,
            "auditory/right": 2,
            "visual/left": 3,
            "visual/right": 4,
            "smiley": 5,
            "buttonpress": 32,
        }
        fig = mne.viz.plot_events(
            events, event_id=event_dict, sfreq=raw.info["sfreq"], first_samp=raw.first_samp
        )
        os.remove(temp_file_path)

        return render(request, 'graph3.html',
                      {'event_data': fig})
    return render(request, 'graph1_upload.html')

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        temp_file_path = "raw.fif"
        with open(temp_file_path, 'wb+') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

        # Load the .fif file using MNE-Python
        raw = mne.io.read_raw_fif(temp_file_path)



        # Select EEG channels for plotting (you can customize this list)
        eeg_channels = ['MEG 001', 'MEG 002', 'MEG 003', 'MEG 004', 'MEG 005', 'MEG 006', 'MEG 007', 'MEG 008',
                        'MEG 009','MEG 010', 'MEG 0113', 'MEG 0111', 'MEG 0113', 'MEG 0122', 'MEG 0123', 'EEG 016', 'EEG 017',
                        'EEG 018']

        # Extract data from the selected EEG channels
        eeg_data, times = raw.copy().pick_channels(ch_names=eeg_channels).get_data(return_times=True)

        # Transpose the EEG data to match Plotly's expectations (channels x time)
        eeg_data = eeg_data.T

        # Create traces for each EEG channel
        traces = []
        for i, channel in enumerate(eeg_channels):
            traces.append(go.Scatter(x=times, y=eeg_data[i], mode='lines', name=channel))

        # Create a layout for the EEG plot
        layout = go.Layout(title='Dynamic EEG Plot', xaxis=dict(title='Time (s)'),
                           yaxis=dict(title='EEG Amplitude (uV)'))

        # Generate an HTML representation of the EEG plot
        plot_div = plot({'data': traces, 'layout': layout}, output_type='div', include_plotlyjs=True)

        # Create 3D Brain Data for the second graph (you can customize this data)
        # Example: A random 3D scatter plot representing brain activity
        num_points = 100
        brain_x = np.random.rand(num_points)
        brain_y = np.random.rand(num_points)
        brain_z = np.random.rand(num_points)

        # Create a trace for the 3D brain chart
        brain_trace = go.Scatter3d(x=brain_x, y=brain_y, z=brain_z, mode='markers', marker=dict(size=3, color='red'))

        # Create a layout for the 3D brain chart
        brain_layout = go.Layout(title='Dynamic 3D Brain Chart', scene=dict(aspectmode='cube'))

        # Generate an HTML representation of the 3D brain chart
        brain_plot_div = plot({'data': [brain_trace], 'layout': brain_layout}, output_type='div', include_plotlyjs=True)

        # Extract events from the raw data
        events = mne.find_events(raw)

        # Create an event dictionary for labeling and coloring events


        # Calculate aud_evoked using MNE-Python
        epochs = mne.Epochs(raw, events, event_id, tmin, tmax, baseline=None, picks='eeg')
        aud_evoked = epochs.average()

        # Plot aud_evoked using Plotly
        aud_evoked_plot_data = []
        for i, ch_name in enumerate(aud_evoked.info['ch_names']):
            aud_evoked_plot_data.append(
                go.Scatter(x=aud_evoked.times, y=aud_evoked.data[i], mode='lines', name=ch_name))

        aud_evoked_layout = go.Layout(title='Auditory Evoked', xaxis=dict(title='Time (s)'),
                                      yaxis=dict(title='Amplitude'))

        # Generate an HTML representation of the aud_evoked plot
        aud_evoked_plot_div = plot({'data': aud_evoked_plot_data, 'layout': aud_evoked_layout}, output_type='div',
                                   include_plotlyjs=True)

        epochs_2 = mne.Epochs(raw, events, event_id, tmin, tmax, baseline=None, picks='meg')
        aud_evoked_2 = epochs_2.average()

        # Plot aud_evoked using Plotly
        aud_evoked_plot_data_2 = []
        for i, ch_name in enumerate(aud_evoked_2.info['ch_names']):
            aud_evoked_plot_data.append(
                go.Scatter(x=aud_evoked_2.times, y=aud_evoked_2.data[i], mode='lines', name=ch_name))

        aud_evoked_layout = go.Layout(title='Auditory Evoked', xaxis=dict(title='Time (s)'),
                                      yaxis=dict(title='Amplitude'))

        # Generate an HTML representation of the aud_evoked plot
        aud_evoked_plot_div_2 = plot({'data': aud_evoked_plot_data, 'layout': aud_evoked_layout}, output_type='div',
                                   include_plotlyjs=True)

        os.remove(temp_file_path)

        return render(request, 'graph.html',
                      { 'brain_plot_div': brain_plot_div,'plot_div':plot_div,
                       'aud_evoked_plot_div': aud_evoked_plot_div, 'aud_evoked_plot_div_2':aud_evoked_plot_div_2})
    return render(request, 'upload.html')
