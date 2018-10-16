# Copyright (C) 2018 Fassio Blatter

import stopeight.legacy
from stopeight.util.editor.data import ScribbleData

def stroke_parallel(data):
    return stopeight.legacy.stroke_parallel(data)
stroke_parallel.__annotations__ = {'data': ScribbleData, 'return': ScribbleData}

def stroke_sequential(data):
    # type: (ScribbleData) -> ScribbleData
    return stopeight.legacy.stroke_sequential(data)
stroke_sequential.__annotations__ = {'data': ScribbleData, 'return': ScribbleData}

def parse_file(data):
    return stopeight.legacy.parse_file(data)
parse_file.__annotations__ = {'data': str, 'return': ScribbleData}


def TCT_to_bezier(data):
    return stopeight.legacy.TCT_to_bezier(data)
TCT_to_bezier.__annotations__ = {'data': ScribbleData, 'return': ScribbleData}

import stopeight.finders
from stopeight.logging import logSwitch
log = logSwitch.logPrint()

def findTurns(data):
    log.info("Invoking findTurns...")
    turns = stopeight.finders.findTurns(data)
    return ScribbleData()
findTurns.__annotations__ = {'data': ScribbleData, 'return': ScribbleData}