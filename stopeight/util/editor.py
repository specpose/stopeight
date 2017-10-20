#!/usr/bin/env python

# Copyright (C) 2017 Fassio Blatter

from stopeight.util import runnable

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox,QApplication,QMainWindow,QToolBar,QPushButton,QGroupBox,QHBoxLayout
from stopeight.util.scribble_area import ScribbleArea
from PyQt5.QtCore import Qt

from stopeight.logging import logSwitch
log = logSwitch.logPrint()
_LOGDIR = '.stopeight' # this is not for logging messages; it is for data files

import types
# false if part of stopeight-clibs
_DATA = {'Modules': [('stopeight.legacy', False),
#                            ('stopeight.comparator.matrixTools',True),
                            ('stopeight.util.file', True),
                            ('stopeight.analyzer', False)
                    ]
         }

import importlib
for module in _DATA['Modules']:
    try:
        importlib.import_module(module[0])
        #output class name
        log.info("Successfully imported module "+module[0])
    except:
        log.info("Removing module "+module[0]+"!")
        _DATA['Modules'].remove(module)

class MyScribble(ScribbleArea):
    def __init__(self, parent = None):
        super(MyScribble, self).__init__(parent)

from sys import modules as loader

class Algorithm(QGroupBox):
    def __init__(self, module, **kwargs):
        super(Algorithm,self).__init__(**kwargs)
        hbox = QHBoxLayout()

        self.select = Algorithm_Select(module)
        hbox.addWidget(self.select)
        self.button = Algorithm_Run(self.select)
        hbox.addWidget(self.button)

        self.setLayout(hbox)

class Algorithm_Select(QComboBox):
    def __init__(self, module, **kwargs):
        super(Algorithm_Select,self).__init__(**kwargs)
        self.module = module
        
        module_name = module[0]
        for key in dir(loader[module_name]):
            if not key.startswith('_'):
                if isinstance(loader[module_name].__dict__[key],types.BuiltinFunctionType) or \
                isinstance(loader[module_name].__dict__[key],types.FunctionType):
                    self.addItem(loader[module_name].__dict__[key].__name__)
#        self.addItem(module_name)

class Algorithm_Run(QPushButton):
    def __init__(self, select, **kwargs):
        super(Algorithm_Run,self).__init__(**kwargs)
        log.debug(self.__class__)
        self.setText("Run")
        self.module = select.module

    @staticmethod
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
        return sub

    def run(self,currentText):
        #inspect.signature()[return]
        #if (len(self.select.module[2].OUTPUT)>0):
        #    self.select.module[2].INPUT = self.select.module[2].OUTPUT
        #    self.select.module[2].OUTPUT= []
        #currentText = self.select.currentText()
        import time
        time = time.time()
        backup = ScribbleData()
        print(backup)
        data = ScribbleData()
        try:
            log.debug("Invoking "+currentText+" with "+str(len(ScribbleData()))+" Points...")
            data = loader[self.module[0]].__dict__[currentText](ScribbleData())
            if backup == data:
                raise("Backup not successful or function values unchanged")
        #except:
        except BaseException as e:
            log.error("Error during method invokation: "+self.module[0]+'.'+currentText)

            from stopeight.util import file
            from os.path import expanduser,join
            file._write(backup,time,outdir=join(expanduser("~"),_LOGDIR
                                                ,self._auto_out(self.module[0],self.module[1],currentText)
                                                #,self._identify(_DATA['MyScribble'])
                                                ))

            data.clear()
            if (len(data)>0):
                raise "Data clear failed!"
        #_DATA['MyScribble'].clearImage()
        #_DATA['MyScribble'].plot(backup,Qt.blue)
        #_DATA['MyScribble'].plot(ScribbleData(),Qt.red)
        log.info("Size after call: Input "+str(len(backup))+", Output "+str(len(ScribbleData())))

class Connector:
    def __init__(self,select,button,scribble):
        self.select = select
        self.button = button
        self.scribble = scribble

    def run(self):
        log.debug(self.select.currentText())
        self.button.run(self.select.currentText())
        self.scribble.clearImage()
        #scribble.plot(backup,Qt.blue)
        self.scribble.plot(ScribbleData(),Qt.black)

if __name__ == '__main__':
    from stopeight.util.editor_data import ScribbleData

    import sys
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Editor")

    #list or dict?
    connections = []

    scribbles = []
    import inspect
    from inspect import Signature
    for module in _DATA['Modules']:
        #if (inspect.signature(zoo).return_annotation!=Signature.empty):
        #if (inspect.signature(zoo).return_annotation==ScribbleData):
        scribbles.append(module)

    toolbox = QToolBar()
    scribble = MyScribble()
    print(scribble.data)
    for module in scribbles:
        algo_box = Algorithm(module)
##        group = QGroupBox()
##        box = QHBoxLayout()
##        select = Algorithm_Select(module)
##        box.addWidget(select)
##        button = Algorithm_Run(module)
##        log.debug("Connecting "+select.currentText())
##        #button.clicked.connect(lambda: _run(select,button,scribble))
##        box.addWidget(button)
##        group.setLayout(box)
##        toolbox.addWidget(group)
        
        connector = Connector(algo_box.select,algo_box.button,scribble)
        connections.append(connector)
        algo_box.button.clicked.connect((connections[len(connections)-1]).run)
        
        toolbox.addWidget(algo_box)
    window.addToolBar(toolbox)
    
    window.setCentralWidget(scribble)
    
    window.show()
    sys.exit(app.exec_())
