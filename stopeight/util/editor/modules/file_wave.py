# Copyright (C) 2017 Fassio Blatter

from PyQt5.QtWidgets import QFileDialog
from stopeight.util.editor.data import WaveData

from stopeight.logging import logSwitch
log = logSwitch.logPrint()

def open_GUI():
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
    result = np.fromstring(signal, 'Int16')
    log.debug("wave ndarray is "+str(type(result)))
    log.debug("Length of samples in mono file "+str(len(result)))
    return result.view(WaveData)
open_GUI.__annotations__ = {'return': WaveData}
