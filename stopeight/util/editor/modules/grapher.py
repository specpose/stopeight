# Copyright (C) 2018 Fassio Blatter

import stopeight.grapher
from stopeight.util.editor.data import ScribbleData, WaveData
from stopeight.util.editor.scribble import ScribbleArea

from stopeight.logging import logSwitch
log = logSwitch.logPrint()

def _append(data):
    for id,vector in enumerate(data):
        if id!=0:
            data[id]+=data[id-1]
    return data

def samples_To_VG(data):
    log.debug("Loading with "+str(len(data)))
    from stopeight.grapher import create_vector_graph
    result = create_vector_graph(data)
    result = _append(result)
    log.debug("Return Length "+str(len(result)))
    return result
samples_To_VG.__annotations__ = {'data':WaveData,'return':ScribbleData}

def home(data):
    #doesnt work: sip.wrappertype
    #log.warning("data "+str(type(data)))
    #log.warning("ScribbleArea "+str(ScribbleArea.__class__))
    #assert type(data) is type(ScribbleArea), "Wrong input data type: %r" % data
    return None
home.__annotations__ = {'data':ScribbleArea,'return':None}
