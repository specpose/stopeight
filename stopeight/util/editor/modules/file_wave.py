# Copyright (C) 2017 Fassio Blatter

from PyQt5.QtWidgets import QFileDialog
from stopeight.util.editor.data import WaveData

def open_GUI()->WaveData:
    import matplotlib.pyplot as ax
    import numpy as np
    import wave
    import sys

    filename = QFileDialog.getOpenFileName()
    print("Opening "+filename)
    spf = wave.open(filename,'r')

    #Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    #If Stereo
    if spf.getnchannels() == 2:
        raise Exception("Just mono files")
    return np.fromstring(signal, 'Int16')
