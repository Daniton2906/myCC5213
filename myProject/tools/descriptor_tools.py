import os

import numpy as np
from librosa import dtw
from scipy.fftpack import dct
from scipy.spatial import distance


class DescriptorManager:

    def __init__(self, sample_rate, signal, name):
        self.signal_name = name
        self.sample_rate = sample_rate
        self.signal = signal

    def get_mfcc(self, start=0, seconds=1.0):
        # os.remove(output_wav)

        # print(sample_rate)

        # print(signal.shape)  # //int(3.5 * sample_rate)
        # width, height = signal.shape
        # signal = signal.reshape(width * height)
        # print(signal.shape)  # //int(3.5 * sample_rate)
        start_frame = int(start * self.sample_rate)
        end_frame = int((start + seconds) * self.sample_rate)
        if end_frame > len(self.signal):
            return None
        signal = self.signal[start_frame:end_frame]  # Keep the first 3.5 seconds

        pre_emphasis = 0.97

        emphasized_signal = np.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])

        frame_size = 0.025
        frame_stride = 0.01

        frame_length, frame_step = frame_size * self.sample_rate, frame_stride * self.sample_rate  # Convert from seconds to samples
        signal_length = len(emphasized_signal)
        frame_length = int(round(frame_length))
        frame_step = int(round(frame_step))
        num_frames = int(np.ceil(
            float(np.abs(signal_length - frame_length)) / frame_step))  # Make sure that we have at least 1 frame

        pad_signal_length = num_frames * frame_step + frame_length
        z = np.zeros((pad_signal_length - signal_length))
        pad_signal = np.append(emphasized_signal,
                               z)  # Pad Signal to make sure that all frames have equal number of samples without truncating any samples from the original signal
        # print(pad_signal.shape)

        indices = np.tile(np.arange(0, frame_length), (num_frames, 1)) + np.tile(
            np.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
        frames = pad_signal[indices.astype(np.int32, copy=False)]

        frames *= np.hamming(frame_length)

        NFFT = 512

        mag_frames = np.absolute(np.fft.rfft(frames, NFFT))  # Magnitude of the FFT
        pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))  # Power Spectrum

        nfilt = 40

        low_freq_mel = 0
        high_freq_mel = (2595 * np.log10(1 + (self.sample_rate / 2) / 700))  # Convert Hz to Mel
        mel_points = np.linspace(low_freq_mel, high_freq_mel, nfilt + 2)  # Equally spaced in Mel scale
        hz_points = (700 * (10 ** (mel_points / 2595) - 1))  # Convert Mel to Hz
        bin = np.floor((NFFT + 1) * hz_points / self.sample_rate)

        fbank = np.zeros((nfilt, int(np.floor(NFFT / 2 + 1))))
        for m in range(1, nfilt + 1):
            f_m_minus = int(bin[m - 1])  # left
            f_m = int(bin[m])  # center
            f_m_plus = int(bin[m + 1])  # right

            for k in range(f_m_minus, f_m):
                fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
            for k in range(f_m, f_m_plus):
                fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
        filter_banks = np.dot(pow_frames, fbank.T)
        filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)  # Numerical Stability
        filter_banks = 20 * np.log10(filter_banks)  # dB

        num_ceps = 12

        mfcc = dct(filter_banks, type=2, axis=1, norm='ortho')[:, 1: (num_ceps + 1)]  # Keep 2-13

        return mfcc

    def get_mean_mfcc(self, start=0):
        seconds = 0.5
        pass

    def save_mfcc(self, path=None, delim=' '):
        filename = self.signal_name + ".txt"
        if path is not None:
            filename = os.path.join(path, filename)
        print(filename)
        np.savetxt(filename, self.signal.flatten(), delimiter=delim)

    @staticmethod
    def load_mfcc(name, path=None, delim=' '):
        filename = name + ".txt"
        if path is not None:
            filename = os.path.join(path, filename)
        print(filename)
        signal = np.reshape(np.loadtxt(filename, delimiter=delim, dtype=type), (-1, 12))
        return DescriptorManager(16000, signal, name)

    @staticmethod
    def mfcc_distance(mfcc1, mfcc2, dist='dtw'):
        if dist == 'dtw':
            return DescriptorManager.dtw_distance(mfcc1, mfcc2)
        if dist == 'manhattan':
            return DescriptorManager.norm_distance(mfcc1, mfcc2)
        elif dist == 'euclidean':
            return DescriptorManager.norm2_distance(mfcc1, mfcc2)
        else:
            raise ValueError('No existe distancia dada')

    @staticmethod
    def dtw_distance(mfcc1, mfcc2, dist='euclidean'):
        D, wp = dtw(mfcc1.T, mfcc2.T, metric='euclidean', backtrack=True)
        # D, wp = dtw(mfcc1.T, mfcc2.T, dist=lambda x, y: euclidean(x - y))

        # print(D.shape)
        # print(wp.shape)
        dist = 0
        for i, j in wp:
            dist += D[i, j]
        return D[-1, -1]

    @staticmethod
    def norm_distance(mfcc1, mfcc2):
        return distance.cityblock(np.ndarray.flatten(mfcc1), np.ndarray.flatten(mfcc2))

    @staticmethod
    def norm2_distance(mfcc1, mfcc2):
        return distance.euclidean(np.ndarray.flatten(mfcc1), np.ndarray.flatten(mfcc2))

    @staticmethod
    def get_match(descrip, sub_descrip, prev_vect=None):
        s = 0
        dist_vector = prev_vect if prev_vect is not None else []
        mfcc1 = descrip.get_mfcc(start=0, seconds=0.5)
        while mfcc1 is not None:
            i = 0
            mfcc2 = sub_descrip.get_mfcc(start=0, seconds=0.5)
            while mfcc2 is not None:
                dist = DescriptorManager.norm2_distance(mfcc1, mfcc2)
                if len(dist_vector) == i:
                    dist_vector.append((s, dist))
                elif dist < dist_vector[i][-1]:
                    dist_vector[i] = (s, dist)
                i += 1
                # print(i*0.5, end=" ")
                mfcc2 = sub_descrip.get_mfcc(start=i * 0.5, seconds=0.5)
            s += 0.5
            print(s)
            mfcc1 = descrip.get_mfcc(start=s, seconds=0.5)
        print()
        return dist_vector
