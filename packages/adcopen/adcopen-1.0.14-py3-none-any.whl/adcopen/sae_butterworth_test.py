import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from adcopen import sae_butterworth

fs = 1000  # Sampling frequency
time_increment = 1 / fs


# Generate the time vector properly
t = np.arange(1000) / fs
signala = np.sin(2*np.pi*100*t) # with frequency of 100
plt.plot(t, signala, label='a')

signalb = np.sin(2*np.pi*20*t) # frequency 20
plt.plot(t, signalb, label='b')

signalc = signala + signalb
plt.plot(t, signalc, label='c')

yf = sae_butterworth(signalc,100, fs)

plt.plot(t, yf, label='filtered')
plt.legend()
plt.show()