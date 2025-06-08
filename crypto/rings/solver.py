import numpy as np
from scipy.io import wavfile as wv

sample_rate, data = wv.read("hundred_times_encrypted.wav")

t = np.linspace(0, data.size / sample_rate, data.size)

carrier_freqs = [900, 2900]
carrier_signal = np.zeros(data.size)
for freq in carrier_freqs:
    carrier_signal += np.sin(2 * np.pi * freq * t)

carrier_signal /= carrier_signal.max()
output_signal = data / (carrier_signal ** 100)

wv.write("decrypted.wav", sample_rate, output_signal.astype(np.int16))