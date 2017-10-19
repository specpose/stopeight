#!/usr/bin/env python

# Copyright (C) 2017 Fassio Blatter

from stopeight.util import runnable

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox,QApplication,QMainWindow,QToolBar,QPushButton,QGroupBox,QHBoxLayout
from stopeight.util.scribble_area import ScribbleArea
from PyQt5.QtCore import Qt

from stopeight.logging import logSwitch
log = logSwitch.logPrint()

import types
    
_LOGDIR = '.stopeight'
import importlib
_DATA = {'Scribble_Module': ['stopeight.legacy',
#                            'stopeight.comparator.matrixTools',
                            'stopeight.util.file',
                            'stopeight.analyzer'
                                                    ]}
for module in _DATA['Scribble_Module']:
    try:
        importlib.import_module(module)
        log.info("Successfully imported module "+module)
    except:
        log.info("Removing module "+module+"!")
        _DATA['Scribble_Module'].remove(module)
from sys import modules as loader

class MyScribble(ScribbleArea):
    def __init__(self, parent = None):
        super(MyScribble,self).__init__(parent)
        _DATA['MyScribble'] = self

class Algorithm(QGroupBox):
    def __init__(self, module_name, **kwargs):
        super(Algorithm,self).__init__(**kwargs)
        hbox = QHBoxLayout()

        select = Algorithm_Select(module_name)
        hbox.addWidget(select)
        button = Algorithm_Run(select)
        hbox.addWidget(button)

        self.setLayout(hbox)

class Algorithm_Select(QComboBox):
    def __init__(self, module_name, **kwargs):
        super(Algorithm_Select,self).__init__(**kwargs)
        self.module_name = module_name
        for key in dir(loader[self.module_name]):
            if not key.startswith('_'):
                if isinstance(loader[self.module_name].__dict__[key],types.BuiltinFunctionType) or \
                isinstance(loader[self.module_name].__dict__[key],types.FunctionType):
                    self.addItem(loader[self.module_name].__dict__[key].__name__)

class Algorithm_Run(QPushButton):
    def __init__(self, select, **kwargs):
        super(Algorithm_Run,self).__init__(**kwargs)
        self.setText("Run")
        self.select = select
        self.clicked.connect(self.run)

    def _identify(self,scribblearea):
        top = self.select.module_name+"."+self.select.currentText()
        try:
            if (os.getcwd()).endswith('stopeight'):
                if (self.select.module_name=='stopeight.util.file'):
                    if hasattr(scribblearea,'tablet_id'):
                        sub = str(scribblearea.tablet_id)
                        return (top,sub)
                    else:
                        return (top,'MouseData')
                else:
                    from dulwich.repo import Repo
                    clibs_repo = Repo('../stopeight/')
                    if (self.select.module_name == ('stopeight.legacy')) or (self.select.module_name == ('stopeight.analyzer')):
                        clibs_repo = Repo('../stopeight-clibs/')
                    sub = (clibs_repo.head().decode('utf-8'))
                    return (top,sub)
        except:
            return (top)

    def run(self):
        if (len(_DATA['MyScribble'].OUTPUT)>0):
            _DATA['MyScribble'].INPUT = _DATA['MyScribble'].OUTPUT
            _DATA['MyScribble'].OUTPUT= []
        import time
        time = time.time()
        try:
            log.debug("Invoking "+self.select.currentText()+" with "+str(len(_DATA['MyScribble'].INPUT))+" Points...")
            _DATA['MyScribble'].OUTPUT = loader[self.select.module_name].__dict__[self.select.currentText()](_DATA['MyScribble'].INPUT)
        #except:
        except BaseException as e:
            print("Error")

            from stopeight.util import file
            from os.path import expanduser,join
            file._write(_DATA['MyScribble'].INPUT,join(expanduser("~"),_LOGDIR),self._identify(_DATA['MyScribble']),time)

            _DATA['MyScribble'].INPUT= []
            _DATA['MyScribble'].OUTPUT= []
        _DATA['MyScribble'].clearImage()
        _DATA['MyScribble'].plot(_DATA['MyScribble'].INPUT,Qt.blue)
        _DATA['MyScribble'].plot(_DATA['MyScribble'].OUTPUT,Qt.red)
        log.info("Size after call: Input "+str(len(_DATA['MyScribble'].INPUT))+", Output "+str(len(_DATA['MyScribble'].OUTPUT)))
            

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Editor")
    toolbox = QToolBar()

    for module in _DATA['Scribble_Module']:
        algo_box = Algorithm(module)
        toolbox.addWidget(algo_box)

    window.addToolBar(toolbox)
    window.setCentralWidget(MyScribble())
    window.show()
    sys.exit(app.exec_())
