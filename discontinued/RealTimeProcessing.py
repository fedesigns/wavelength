

"""
Utilities for real-time processing
"""

from collections import OrderedDict
from threading import Thread, Event

import numpy as np
from scipy import signal


BAND_FREQS = OrderedDict()
BAND_FREQS['delta'] = (1, 4)
BAND_FREQS['theta'] = (4, 8)
BAND_FREQS['alpha'] = (7.5, 13)
BAND_FREQS['beta'] = (13, 30)
BAND_FREQS['gamma'] = (30, 44)

RATIOS = OrderedDict()
RATIOS['beta/alpha'] = (3, 2)
RATIOS['theta/alpha'] = (4, 2)

BLINKWAVE = np.asarray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        -17.683,-31.44,-44.534,-56.351,-66.451,-74.543,-80.462,
                        -84.142,-85.604,-84.934,-82.271,-77.79,-71.697,-64.214,
                        -55.574,-46.011,-35.757,-25.037,-14.061,-3.028,7.882,
                        18.507,28.704,38.352,47.346,55.605,63.064,69.678,
                        75.418,80.272,84.239,87.336,89.588,91.031,91.709,
                        91.673,90.981,89.691,87.868,85.577,82.882,79.848,
                        76.538,73.011,69.325,65.534,61.686,57.826,53.994,
                        50.223,46.544,42.981,39.552,36.273,33.154,30.198,
                        27.408,24.782,22.313,19.993,17.813,15.758,13.815,
                        11.969, 10.204,8.5049,6.8558,5.2423,3.6505,2.0681])


HEARTWAVE = np.asarray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,21.623,36.971,59.776,98.036,132.82,175.89,185.95,115.3,-24.952,-202.51,-364.39,-450.96,-412.91,-324.91,-304.24,-333.27,-347.46,-342.08,-261.02,-81.866,84.638,190.3,250.39,279.78,281.17,266.42,256.18,254.9,245.22,229.63,217.99,210.21,197.21,177.98,168.21,161.73,145.03,131.1,121.96,110.82,101.6,88.15,86.381,86.017,72.336,63.964,61.159,51.928,43.105,44.441,42.399,32.123])


def sigmoid(x, a=1, b=0, c=0):
    """Sigmoid function.
    Args:
        x (array_like): values to map
        a (float): control the steepness of the curve
        b (float): control the shift in x
        c (float): control the shift in y
    Returns:
        (numpy.ndarray) output of the sigmoid
    """
    return 1 / (1 + np.exp(-(a*x + b))) + c


def get_filter_coeff(fs, N, l_freq=None, h_freq=None, method='butter'):
    """Get filter coefficients.
    Args:
        fs (float): sampling rate of the signal to filter
        N (int): order of the filter
    Keyword Args:
        l_freq (float or None): lower cutoff frequency in Hz. If provided
            without `h_freq`, returns a highpass filter. If both `l_freq`
            and `h_freq` are provided and `h_freq` is larger than `l_freq`,
            returns a bandpass filter, otherwise returns a bandstop filter.
        h_freq (float or None): higher cutoff frequency in Hz. If provided
            without `l_freq`, returns a lowpass filter.
        method (string): method to compute the coefficients ('butter', etc.)
    Returns:
        (numpy.ndarray): b coefficients of the filter
        (numpy.ndarray): a coefficients of the filter
    Examples:
        Get a 5th order lowpass filter at 30 Hz for a signal sampled at 256 Hz
        >>> b, a = get_filter_coeff(256, 5, h_freq=30)
    """

    if l_freq is not None and h_freq is not None:
        if l_freq < h_freq:
            btype = 'bandpass'
            Wn = [l_freq/(float(fs)/2), h_freq/(float(fs)/2)]
        elif l_freq > h_freq:
            btype = 'bandstop'
            Wn = [h_freq/(float(fs)/2), l_freq/(float(fs)/2)]
    elif l_freq is not None:
        Wn = l_freq/(float(fs)/2)
        btype = 'highpass'
    elif h_freq is not None:
        Wn = h_freq/(float(fs)/2)
        btype = 'lowpass'

    if method == 'butter':
        b, a = signal.butter(N, Wn, btype=btype)
    else:
        raise(ValueError('Method ''{}'' not supported.'.format(method)))

    return b, a


def fft_continuous(data, n=None, psd=False, log='log', fs=None,
                   window='hamming'):
    """Apply the Fast Fourier Transform on continuous data.
    Apply the Fast Fourier Transform algorithm on continuous data to get
    the spectrum.
    Steps:
        1- Demeaning
        2- Apply hamming window
        3- Compute FFT
        4- Grab lower half
    Args:
        data (numpy.ndarray): shape (`n_samples`, `n_channels`). Data for
            which to get the FFT
    Keyword Args:
        n (int): length of the FFT. If longer than `n_samples`, zero-padding
            is used; if smaller, then the signal is cropped. If None, use
            the same number as the number of samples
        psd (bool): if True, return the Power Spectral Density
        log (string): can be 'log' (log10(x)), 'log+1' (log10(x+1)) or None
        fs (float): Sampling rate of `data`.
        window (string): if 'no_window' do not use a window before
            applying the FFT. Otherwise, use as the window function.
            Currently only supports 'hamming'.
    Returns:
        (numpy.ndarray) Fourier Transform of the original signal
        (numpy.ndarray): array of frequency bins
    """
    if data.ndim == 1:
        data = data.reshape((-1, 1))
    [n_samples, n_channels] = data.shape

    data = data - data.mean(axis=0)
    if window.lower() == 'hamming':
        H = np.hamming(n_samples).reshape((-1, 1))
    elif window.lower() == 'no_window':
        H = np.ones(n_samples).reshape((-1, 1))
    else:
        raise ValueError('window value {} is not supported'.format(window))
    L = np.min([n_samples, n]) if n else n_samples
    Y = np.fft.fft(data * H, n, axis=0) / L
    freq_bins = (fs * np.arange(0, Y.shape[0] / 2 + 1) / Y.shape[0]) \
        if fs is not None else None

    out = Y[0:int(Y.shape[0] / 2) + 1, :]
    out[:, 0] = 2 * out[:, 0]

    if psd:
        out = np.abs(out) ** 2
    if log == 'log':
        out = np.log10(out)
    elif log == 'log+1':
        out = np.log10(out + 1)

    return out, freq_bins


def compute_band_powers(psd, f, relative=False, band_freqs=BAND_FREQS):
    """Compute the standard band powers from a PSD.
    Compute the standard band powers from a PSD.
    Args:
        psd (numpy.ndarray): array of shape (n_freq_bins, n_channels)
            containing the PSD of each channel
        f (array_like): array of shape (n_freq_bins,) containing the
            frequency of each bin in `psd`
    Keyword Args:
        relative (bool): if True, compute relative band powers
        band_freqs (OrderedDict): dictionary containing the band names as
            keys, and tuples of frequency boundaries as values. See
            BAND_FREQS.
    Returns:
        (numpy.ndarray): array of shape (n_bands, n_channels) containing
            the band powers
        (list): band names
    """
    band_powers = np.zeros((len(band_freqs), psd.shape[1]))
    for i, bounds in enumerate(band_freqs.values()):
        mask = (f >= bounds[0]) & (f <= bounds[1])
        band_powers[i, :] = np.mean(psd[mask, :], axis=0)

    if relative:
        band_powers /= band_powers.sum(axis=0)

    return band_powers, list(band_freqs.keys())


def compute_band_ratios(band_powers, ratios=RATIOS):
    """Compute ratios of band powers.
    Args:
        band_powers (numpy.ndarray): array of shape (n_bands, n_channels)
            containing the band powers
    Keyword Args:
        ratios (tuple of tuples): contains the indices of band powers to
            compute ratios from. E.g., ((3, 2)) is beta/alpha.
            See BAND_FREQS and RATIOS.
        ratios (OrderedDict): dictionary containing the ratio names as keys
            and tuple of indices of the bands to used for each ratio. See
            RATIOS.
    Returns:
        (numpy.ndarray): array of shape (n_rations, n_channels)
            containing the ratios of band powers
        (list): ratio names
    """
    ratio_powers = np.zeros((len(ratios), band_powers.shape[1]))
    for i, ratio in enumerate(ratios.values()):
        ratio_powers[i, :] = band_powers[ratio[0], :] / band_powers[ratio[1], :]

    return ratio_powers, list(ratios.keys())

