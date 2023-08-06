"""
(C) 2018-2020 Automated Design Corp. All Rights Reserved.

:author Thomas C. Bitsky Jr.



"""

from scipy import signal
import numpy as np
import typing

def butter_lowpass(cutoff:float, sample_rate_hz:int, order:int=2):
    """
    Create a low-pass butterworth filter configuration.

    Args:
        cutoff (float): cutoff frequency
        sample_rate_hz (int): the sample rate of the data, in Hz
        order (int): The order of the filter.

    Returns:
        b (ndarray) : numerator of the polynomial        
        a (ndarray) : denominator of the polynomial
    """    
    nyq = 0.5 * sample_rate_hz

    normal_cutoff = cutoff / nyq
    
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data:typing.Any, cutoff:float, sample_rate_hz:int, order:int=2):
    """
    Returns the result of a low-pass filter on the incoming data.

    Args:
        data (array_like) : The data to filter
        cutoff (float): cutoff frequency
        sample_rate_hz (int): the sample rate of the data, in Hz
        order (int): The order of the filter.

    Returns:
        b (ndarray) : numerator of the polynomial        
        a (ndarray) : denominator of the polynomial
    """        
    b, a = butter_lowpass(cutoff, sample_rate_hz, order=order)
    y = signal.lfilter(b, a, data)
    return y

def cfc_cutoff_frequency(sample_rate_hz:int) -> int:

    if sample_rate_hz >= 10000: #CFC1000
        return 1650
    elif sample_rate_hz >= 6000: #CFC600
        return 1000
    elif sample_rate_hz >= 1800: #CFC180
        return 300
    elif sample_rate_hz >= 600: #CFC60
        return 100
    
    raise "Sample rate is too low." 



def sae_butterworth(data:typing.Any, cutoff:float, sample_rate_hz:int) -> np.ndarray:
    """
    Returns an array of data processed using an SAE J211 Butterworth filter. 

    Args:
    data (array-like): The data to be filtered.
    cutoff (float) : the cutoff frequency. Use cfc_cutoff_frequency to calculate.
    sample_rate_hz (int) : sample rate of data, in Hz


    Returns:
    ndarray of filtered data
    """
 
    # attenuation seems to change based on frequency.
 
    
    
    # Set 6dB attenuation frequency 
    # Why? I have no idea. Taken from example code published by a university.
    # However, it does work.
    atten = cutoff * 1.2465

     
    
    """
    The SAE butterworth filter is a two-pole filter.
    To make it a 4-pole filter, the data is passed through the filter twice.
    """
    
    b, a = butter_lowpass(atten, sample_rate_hz, order=2)

    
    # Apply the filter to the data.  Use lfilter_zi to choose the initial condition
    # of the filter.
    zi = signal.lfilter_zi(b, a)
    z, _ = signal.lfilter(b, a, data, zi=(zi * data[0]) )
    
    # Apply the filter again, to have a result filtered at an order
    # the same as filtfilt.
    z2, _ = signal.lfilter(b, a, z, zi=(zi * z[0]) )
    
    # Use filtfilt to apply the filter.
    y = signal.filtfilt(b, a, data)
    
    return y