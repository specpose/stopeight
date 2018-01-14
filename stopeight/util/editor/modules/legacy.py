# Copyright (C) 2018 Fassio Blatter

import stopeight.legacy
from stopeight.util.editor.data import ScribbleData

def stroke_parallel(data:ScribbleData)->ScribbleData:
    return stopeight.legacy.stroke_parallel(data)

def stroke_sequential(data:ScribbleData)->ScribbleData:
    return stopeight.legacy.stroke_sequential(data)

def parse_file(data:str)->ScribbleData:
    return stopeight.legacy.parse_file(data)

def TCT_to_bezier(data:ScribbleData)->ScribbleData:
    return stopeight.legacy.TCT_to_bezier(data)
