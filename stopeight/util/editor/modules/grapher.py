# Copyright (C) 2018 Fassio Blatter

import stopeight.grapher
from stopeight.util.editor.data import ScribbleData, WaveData

from stopeight.logging import logSwitch
log = logSwitch.logPrint()

def samples_To_VG(data):
    log.debug("samples_To_VG datatype "+str(type(data)))
    log.info("Loading with "+str(len(data)))
    from stopeight.grapher import VectorInt16
    algo = VectorInt16()
    #from stopeight.grapher import Samples_To_VG
    #algo = stopeight.grapher.Samples_To_VG(1,1.0,[1.0,2.0,1.0])
    log.debug("Instantiated object type "+str(type(algo)))
    return [[1,1],[2,2]]
samples_To_VG.__annotations__ = {'data':WaveData,'return':ScribbleData}
