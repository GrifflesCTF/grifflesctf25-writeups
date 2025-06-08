# Challenge Solution

1. Search key phrases such as "multiplied [input] by a carrier" and "metallic [output]" to determine the encryption method was some form of modulation. The title "Rings" implies it was ring modulation.

2. Plot a frequency analysis of "two_freq_encrypted.wav" to see peak frequencies. Some calculation leads to the carrier signal being composed of either 900 and 2900 Hz or 200, 300, and 500 Hz pure tones. The file name "two_freq_carrier..." implies the former.

3. Now the carrier signal and carrier frequencies are known, undo the ring modulation with a script. The file name "hundred_times_encrypted.wav" and the overall extreme static in it implies it was not modulated once, but 100 times. Undo 100 ring modulations.

4. Use https://www.aha-music.com/ or similar sites to find the song title and its video on YouTube.

# Comments

1. The challenge description can be modified to make the process of determining it was ring modulation easier or harder.

2. The math behind ring modulation is well-documented - on Wikipedia, for example - hence calculating the carrier frequencies and writing a reversal script should be doable.

3. The higher frequency in the carrier signal (2900 Hz) can be increased to make the distinction between two sets of data in the frequency analysis clearer.

4. The choice of encrypted music can be modified if the chosen one is too popular / recognisable without decrypting.

5. Music sourced from https://youtu.be/al1BNB8bKaE.