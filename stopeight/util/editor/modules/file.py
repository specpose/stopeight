#!/usr/bin/env python

# Copyright (C) 2009-2016 Specific Purpose Software GmbH
from stopeight.logging import logSwitch
log = logSwitch.logPrint()

from stopeight.util.editor.data import ScribbleData

def save(nothing):
    # this is not a real error but saves us from writing more code
    raise ValueError

def save_GUI(data):
    pass
save_GUI.__annotations__ = {'data': ScribbleData, 'return': str}

def open_GUI(data):
    pass
open_GUI.__annotations__ = {'data': str, 'return': ScribbleData}

from os.path import expanduser,join
def _write(data,timestamp,outdir=join(expanduser("~"))):
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
