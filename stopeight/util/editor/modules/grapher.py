# Copyright (C) 2018 Fassio Blatter

import stopeight.grapher
from stopeight.util.editor.data import ScribbleData, WaveData

from stopeight.logging import logSwitch
log = logSwitch.logPrint()

def samples_To_VG(data):
    log.info("Loading with "+str(len(data)))
    algo = stopeight.grapher.VectorGraph(1,1.0,[])
    return algo(data)
samples_To_VG.__annotations__ = {'data':WaveData,'return':ScribbleData}
