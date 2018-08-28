# Copyright (C) 2018 Fassio Blatter

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
    assert type(data.data) is list, "Wrong input data.data type: %r" % type(data.data)
    from stopeight.grapher import Vectors,Vector,Stack
    vectors = Vectors()
    for element in data.data:
        vectors.push_back(Vector(element.first,element.second))
    stack = Stack()
    stack.identity()
    from numpy.core.umath import arctan2
    angle = arctan2(vectors.np()[-1][1],vectors.np()[-1][0])
    log.debug("Rotating "+str(angle))
    stack.rotate(angle)
    vectors.apply(stack)
    log.debug("First "+str(vectors.np()[1][0])+","+str(vectors.np()[1][1])+" Last "+str(vectors.np()[-1][0])+","+str(vectors.np()[-1][1]))
    stack = Stack()
    stack.identity()
    #from stopeight.util.editor.data import ScribblePoint
    #testvec = []
    #test=ScribblePoint(0.0,data.height()/2)
    #testvec.append(test)
    #test=ScribblePoint(data.width()/2,data.height()/2)
    #testvec.append(test)
    #print(testvec)
    data(vectors.np())
    return None
home.__annotations__ = {'data':ScribbleArea,'return':None}
