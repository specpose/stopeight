#!/usr/bin/env python

# Copyright (C) 2009-2016 Specific Purpose Software GmbH

def save(nothing):
    # this is not a real error but saves us from writing more code
    raise ValueError

def save_GUI(points):
    pass

def open_GUI(nothing):
    pass

def _write(data,basedir,identity,timestamp):
    import datetime
    time = (datetime.datetime.utcfromtimestamp(timestamp))
    time = time.strftime('%Y%m%dT%H%M%S')
    name = time+"."+type(data).__name__
    import os
    from os import path
    identity_dir = path.join(basedir,identity[0],identity[1])
    if not os.path.exists(identity_dir):
        os.makedirs(identity_dir)
    path = path.join(identity_dir,name)
    print("Writing method input data to: "+path)


    #import pickle
    #picl = pickle.Pickler(open(path+'.pickle','wb'),pickle.HIGHEST_PROTOCOL)
    #picl.dump(_DATA['MyScribble'].INPUT)

    import json
    f = open(path+'.json','w')
    json.dump(data,f)