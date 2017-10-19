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
# false/true as in pkgutil.iter_modules
_DATA = {'Scribble_Module': [('stopeight.legacy',False),
#                            ('stopeight.comparator.matrixTools',true),
                            ('stopeight.util.file',True),
                            ('stopeight.analyzer',False)
                                                    ]}
for module in _DATA['Scribble_Module']:
    try:
        importlib.import_module(module[0])
        log.info("Successfully imported module "+module[0])
    except:
        log.info("Removing module "+module[0]+"!")
        _DATA['Scribble_Module'].remove(module)
from sys import modules as loader

class MyScribble(ScribbleArea):
    def __init__(self, parent = None):
        super(MyScribble,self).__init__(parent)
        _DATA['MyScribble'] = self

class Algorithm(QGroupBox):
    def __init__(self, module, **kwargs):
        super(Algorithm,self).__init__(**kwargs)
        hbox = QHBoxLayout()

        select = Algorithm_Select(module)
        hbox.addWidget(select)
        button = Algorithm_Run(select)
        hbox.addWidget(button)

        self.setLayout(hbox)

class Algorithm_Select(QComboBox):
    def __init__(self, module_name, **kwargs):
        super(Algorithm_Select,self).__init__(**kwargs)
        self.module_name = module[0]
        self.package_type = module[1]
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

    def _auto_out(module_name,package_type,function_name):
        top = module_name+'.'+function_name
        import os
        from subprocess import check_output
        sub = 'HEAD'
        if (package_type==True):
            #get head from current directory (os.getcwd()).endswith('stopeight')
            try:
                sub = check_output(['git','rev-parse','--short','HEAD']).decode('utf-8').rstrip()
            except:
                sub = check_output(['git','rev-parse','--short','HEAD']).rstrip()
        else:
            #get head from stopeight-clibs
            try:
                sub = check_output(['git','rev-parse','--short','HEAD'],cwd=os.path.join('stopeight-clibs')).decode('utf-8').rstrip()
            except:
                sub = check_output(['git','rev-parse','--short','HEAD'],cwd=os.path.join('stopeight-clibs')).rstrip()
        top = os.path.join(top,sub)
        return top
    
    def _identify(self,scribblearea):
        import os
            
        #if (os.getcwd()).endswith('stopeight'):
        #    if (self.select.module_name=='stopeight.util.file'):
        if hasattr(scribblearea,'tablet_id'):
            sub = str(scribblearea.tablet_id)
        else:
            sub = 'MouseData'
        top = os.path.join(Algorithm_Run._auto_out(self.select.module_name,self.select.package_type,self.select.currentText()),sub)
        return top

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
            log.error("Error during method invokation: "+self.select.module_name+'.'+self.select.currentText())

            from stopeight.util import file
            from os.path import expanduser,join
            file._write(_DATA['MyScribble'].INPUT,time,outdir=join(expanduser("~"),_LOGDIR,self._identify(_DATA['MyScribble']))  )

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
