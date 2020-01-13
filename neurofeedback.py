# -*- coding: utf-8 -*-
"""
Estimate Relaxation from Band Powers
This example shows how to buffer, epoch, and transform EEG data from a single
electrode into values for each of the classic frequencies (e.g. alpha, beta, theta)
Furthermore, it shows how ratios of the band powers can be used to estimate
mental state for neurofeedback.
The neurofeedback protocols described here are inspired by
*Neurofeedback: A Comprehensive Review on System Design, Methodology and Clinical Applications* by Marzbani et. al
Adapted from https://github.com/NeuroTechX/bci-workshop
"""

import numpy as np  # Module that simplifies computations on matrices
import matplotlib.pyplot as plt  # Module used for plotting
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
import utils  # Our own utility functions
import csv 
from datetime import datetime

# enumeration to make code more readable

class Band:
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3
    LowBeta = 4
    HighBeta = 5
    Gamma = 6


""" EXPERIMENTAL PARAMETERS """
# Modify these to change aspects of the signal processing

# Length of the EEG data buffer (in seconds)
# This buffer will hold last n seconds of data and be used for calculations
BUFFER_LENGTH = 5

# Length of the epochs used to compute the FFT (in seconds)
EPOCH_LENGTH = 1

# Amount of overlap between two consecutive epochs (in seconds)
OVERLAP_LENGTH = 0.8

# Amount to 'shift' the start of each next consecutive epoch
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH

# Index of the channel(s) (electrodes) to be used
# 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
INDEX_CHANNEL = [0]

if __name__ == "__main__":

    """ 1. CONNECT TO EEG STREAM """

    # Search for active LSL streams
    print('Looking for an EEG stream...')
    streams = resolve_byprop('type', 'EEG', timeout=2)
    if len(streams) == 0:
        raise RuntimeError('Can\'t find EEG stream.')

    # Set active EEG stream to inlet and apply time correction
    print("Start acquiring data")
    inlet = StreamInlet(streams[0], max_chunklen=12)
    eeg_time_correction = inlet.time_correction()

    # Get the stream info and description
    info = inlet.info()
    description = info.desc()

    # Get the sampling frequency
    # This is an important value that represents how many EEG data points are
    # collected in a second. This influences our frequency band calculation.
    # for the Muse 2016, this should always be 256
    fs = int(info.nominal_srate())

    """ 2. INITIALIZE BUFFERS """

    # Initialize raw EEG data buffer
    eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
    filter_state = None  # for use with the notch filter

    # Compute the number of epochs in "buffer_length"
    n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) /
                              SHIFT_LENGTH + 1))

    # Initialize the band power buffer (for plotting)
    # bands will be ordered: [delta, theta, alpha, beta, low beta, high beta, gamma]
    band_buffer = np.zeros((n_win_test, 7))

    """ 3. GET DATA """

    # The try/except structure allows to quit the while loop by aborting the
    # script with <Ctrl-C>
    print('Press Ctrl-C in the console to break the while loop.')

    try:
        # Setting up a new csv
        # datetime object containing current date and time


        csvtitle = 'Data/Neurofeedback.csv'  # title

        # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers

        while True:

            """ 3.1 ACQUIRE DATA """
            # Obtain EEG data from the LSL stream
            eeg_data, timestamp = inlet.pull_chunk(
                timeout=1, max_samples=int(SHIFT_LENGTH * fs))

            # Only keep the channel we're interested in
            ch_data = np.array(eeg_data)#[:, INDEX_CHANNEL]
            avg_data = np.mean(ch_data, axis=0)

            # Update EEG buffer with the new data
            eeg_buffer, filter_state = utils.update_buffer(
                eeg_buffer, avg_data, notch=True,
                filter_state=filter_state)

            """ 3.2 COMPUTE BAND POWERS """
            # Get newest samples from the buffer
            data_epoch = utils.get_last_data(eeg_buffer,
                                             EPOCH_LENGTH * fs)

            # Compute band powers
            band_powers = utils.compute_band_powers(data_epoch, fs)
            band_buffer, _ = utils.update_buffer(band_buffer,
                                                 np.asarray([band_powers]))

            # Compute the average band powers for all epochs in buffer
            # This helps to smooth out noise
            smooth_band_powers = np.mean(band_buffer, axis=0)

            print('Delta: ', smooth_band_powers[Band.Delta], ' Theta: ', smooth_band_powers[Band.Theta], \
                   ' Alpha: ', smooth_band_powers[Band.Alpha], ' Beta: ', band_powers[Band.Beta], \
                   ' LowBeta: ', smooth_band_powers[Band.LowBeta], ' HighBeta: ', smooth_band_powers[Band.HighBeta], \
                   ' Gamma: ', smooth_band_powers[Band.Gamma])

            """ 3.3 COMPUTE NEUROFEEDBACK METRICS """
            # These metrics could also be used to drive brain-computer interfaces

            # Alpha Protocol:
            # Simple redout of alpha power, divided by delta waves in order to rule out noise
            alpha_metric = smooth_band_powers[Band.Alpha] / \
                smooth_band_powers[Band.Delta]
            print('Alpha Relaxation: ', alpha_metric)

            # Beta Protocol:
            # Beta waves have been used as a measure of mental activity and concentration
            # This beta over theta ratio is commonly used as neurofeedback for ADHD
            beta_metric = smooth_band_powers[Band.Beta] / \
                smooth_band_powers[Band.Theta]
            print('Beta Concentration: ', beta_metric)

            # Alpha/Theta Protocol:
            # This is another popular neurofeedback metric for stress reduction
            # Higher theta over alpha is supposedly associated with reduced anxiety
            theta_metric = smooth_band_powers[Band.Theta] / \
                smooth_band_powers[Band.Alpha]
            print('Theta Relaxation: ', theta_metric)

            # Overactive Stress (Overthinking) Metric (source: Versus Headset):
            # Versus Headset 'Overarousal' training program description - overthinking metric
            # Higher beta over alpha and theta
            overthinking_metric = smooth_band_powers[Band.Beta] / \
                (smooth_band_powers[Band.Theta] + smooth_band_powers[Band.Alpha])
            print('Overactive Stress: ', overthinking_metric)

            # Distraction Vulnerability (Low executive attention) Metric (source: Versus Headset):
            # Higher alpha and high beta, inhibited low beta
            distraction_vulnerability_metric = (smooth_band_powers[Band.Alpha] + smooth_band_powers[Band.HighBeta])/ \
                smooth_band_powers[Band.LowBeta]
            print('Distraction Vulnerability: ', distraction_vulnerability_metric)

            # Task Engagement (high attention activation) Metric (source: Versus Headset):
            # Higher low beta over alpha, theta and gamma
            engagement_metric = smooth_band_powers[Band.LowBeta]/ \
                (smooth_band_powers[Band.Alpha] + smooth_band_powers[Band.Theta] + smooth_band_powers[Band.Gamma])
            print('Task Engagement: ', engagement_metric)

            # Productive Focus (concentration on productive aspect of the moment, ruling out distraction) Metric (source: Versus Headset):
            # Higher low beta over theta and gamma
            productive_focus_metric = smooth_band_powers[Band.LowBeta]/ \
                (smooth_band_powers[Band.Theta] + smooth_band_powers[Band.Gamma])
            print('Productive Focus: ', productive_focus_metric)

            # Impulse Control (inhibit strong impulses and make effective decisions) Metric (source: Versus Headset)
            # High low beta, low theta, low gamma
            impulse_control_metric = smooth_band_powers[Band.LowBeta]/ \
                (smooth_band_powers[Band.Theta] + smooth_band_powers[Band.Gamma])
            print('Impulse control: ', impulse_control_metric)

            # Under-arousal (low cortical activation, inhibited information processing and engagement) Metric (source: Versus Headset)
            # High alpha, high gamma, low low beta
            under_arousal_metric = (smooth_band_powers[Band.Alpha] + smooth_band_powers[Band.Gamma])/ \
                smooth_band_powers[Band.LowBeta] 
            print('Under-arousal: ', under_arousal_metric)
            

            # Write data on csv file

            with open(csvtitle, 'a', newline = '') as csvFile:
                writer = csv.writer(csvFile)
                last_timestamp = timestamp[-1]

                dt_object = datetime.fromtimestamp(last_timestamp)  

                row = [last_timestamp, dt_object, alpha_metric, beta_metric, theta_metric, \
                    overthinking_metric, distraction_vulnerability_metric, engagement_metric, \
                    impulse_control_metric, under_arousal_metric]

                writer.writerow(row)
                

    except KeyboardInterrupt:
        csvFile.close()
   

