# Copyright (C) 2018 Fassio Blatter

from stopeight.util.editor.data import ScribbleData

import stopeight.analyzer
def hello(data):
    return stopeight.analyzer.hello(data)
hello.__annotations__ = {'data': str, 'return': str}

