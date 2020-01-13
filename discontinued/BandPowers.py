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

