#!/usr/bin/env python

# Copyright (C) 2009-2016 Specific Purpose Software GmbH
from stopeight.logging import logSwitch
log = logSwitch.logNone()

from stopeight.util.editor.data import ScribbleData,ScribblePoint
from stopeight.util.editor.scribble import ScribbleArea
from PyQt5.QtWidgets import QFileDialog

def save_ScribbleData(data):
    # this is not a real error but saves us from writing more code
    raise ValueError
save_ScribbleData.__annotations__ = {'data': ScribbleArea, 'return': type(None)}

def save_as_ScribbleData(data):
    assert type(data.data) is ScribbleData, "Could not save object type: %r" % type(data.data)
    filename = QFileDialog.getSaveFileName(None,"QFileDialog.getSaveFileName()","","JSON Files (*.json)")
    log.debug("Saving to File "+str(filename[0]))
    import json
    f = open(filename[0],'w')
    json.dump(data.data,f)
    return filename
save_as_ScribbleData.__annotations__ = {'data': ScribbleArea, 'return': type(None)}

def open_ScribbleData():
    filename = QFileDialog.getOpenFileName()
    log.debug("Reading from File "+str(filename[0]))
    data = _read(filename[0])
    assert type(data) is list, "Could not read file: %r" % filename
    #data.__class__= ScribbleData
    #Hack copy
    data2 = ScribbleData()
    for element in data:
        data2.append(ScribblePoint((element[0],element[1])))
    return data2
open_ScribbleData.__annotations__ = {'return': ScribbleData}

def _read(path):
    import json
    f = open(path,'r')
    return json.load(f)

def _write(data,timestamp,outdir=None):
    if outdir==None:
        from os.path import expanduser,join
        outdir=join(expanduser("~"))
    import datetime
    time = (datetime.datetime.utcfromtimestamp(timestamp))
    time = time.strftime('%Y%m%dT%H%M%S')
    name = time+"."+type(data).__name__
    import os
    from os import path
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    path = path.join(outdir,name)
    log.info("Writing method input data to: "+path)


    #import pickle
    #picl = pickle.Pickler(open(path+'.pickle','wb'),pickle.HIGHEST_PROTOCOL)
    #picl.dump(_DATA['MyScribble'].INPUT)

    import json
    f = open(path+'.json','w')
    json.dump(data,f)
