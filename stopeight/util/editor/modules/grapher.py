# Copyright (C) 2018 Fassio Blatter

import stopeight.grapher
from stopeight.util.editor.data import ScribbleData, WaveData
from stopeight.util.editor.scribble import ScribbleArea

from stopeight.logging import logSwitch
log = logSwitch.logPrint()

def samples_To_VG(data):
    log.debug("samples_To_VG datatype "+str(type(data)))
    log.debug("Loading with "+str(len(data)))
    log.debug(str(data))
    #from stopeight.grapher import VectorInt16
    #algo = VectorInt16(data)
    #from stopeight.grapher import VectorTCInt16
    #result = VectorTCInt16()
    from stopeight.grapher import create_vector_graph
    result = create_vector_graph(data)
    #from stopeight.grapher import Samples_To_VG
    #algo = stopeight.grapher.Samples_To_VG(1,1.0,[1.0,2.0,1.0])
    log.debug("Instantiated object type "+str(type(result)))
    log.debug("Length "+str(len(result)))
    return result
samples_To_VG.__annotations__ = {'data':WaveData,'return':ScribbleData}

def home(data):
    objecttype = type(data)
    log.debug("Object type is "+str(objecttype))
    return None
home.__annotations__ = {'data':ScribbleArea,'return':None}
