# Copyright (C) 2017 Fassio Blatter

from PyQt5.QtWidgets import QFileDialog
from stopeight.util.editor.data import WaveData

from stopeight.logging import logSwitch
log = logSwitch.logPrint()

def _convert(spf):
    import numpy as np

    #Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    #If Stereo
    if spf.getnchannels() == 2:
        raise Exception("Just mono files")
    datatype=None
    fconverter=lambda a:a
    if spf.getsampwidth()==1:
        #8bit unsigned
        datatype=np.uint8
        fconverter=lambda a: ((a/255.0) - 0.5) *2
    elif spf.getsampwidth()==2:
        #16bit signed
        datatype=np.int16
        fconverter=lambda a: a / 32767.0
    samples = np.fromstring(signal, datatype)
    return fconverter(np.asarray(samples, dtype=np.float64))

def open_WaveData():
    import matplotlib.pyplot as ax
    import wave
    import sys

    filename = QFileDialog.getOpenFileName()
    log.info("Opening "+str(filename[0]))
    spf = wave.open(filename[0],'r')
    result = _convert(spf)
    spf.close()
    log.debug("wave ndarray is "+str(type(result)))
    log.debug("Length of samples in mono file "+str(len(result)))
    return result.view(WaveData)
open_WaveData.__annotations__ = {'return': WaveData}
