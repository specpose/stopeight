# Copyright (C) 2017 Fassio Blatter

from PyQt5.QtWidgets import QFileDialog
from stopeight.util.editor.data import WaveData

from stopeight.logging import logSwitch
log = logSwitch.logPrint()

def open_GUI()->WaveData:
    import matplotlib.pyplot as ax
    import numpy as np
    import wave
    import sys

    filename = QFileDialog.getOpenFileName()
    log.info("Opening "+str(filename[0]))
    spf = wave.open(filename[0],'r')

    #Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    #If Stereo
    if spf.getnchannels() == 2:
        raise Exception("Just mono files")
    return np.fromstring(signal, 'Int16')
