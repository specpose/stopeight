#!/usr/bin/env python

# Copyright (C) 2009-2016 Specific Purpose Software GmbH

from PyQt5.QtWidgets import QComboBox,QApplication,QMainWindow,QToolBar,QPushButton,QGroupBox,QHBoxLayout
from scribble2 import ScribbleArea
from PyQt5.QtCore import Qt


_DATA = {'Module_Name':'stopeight_clibs_legacy'}
__import__(_DATA['Module_Name'])
from sys import modules as loader

from stopeight.logging import logSwitch
log = logSwitch.logPrint()

class MyScribble(ScribbleArea):
    def __init__(self, parent = None):
        super(MyScribble,self).__init__(parent)
        _DATA['Input']= []
        _DATA['Output']= []
        _DATA['MyScribble'] = self

    def _input(self, event):
        #if len(_DATA['Input']) == 0: self.clearImage()
        _DATA['Input'].append((event.pos().x(),event.pos().y()))

    def mousePressEvent(self, event):
        super(MyScribble,self).mousePressEvent(event)
        self.clearImage()
        _DATA['Input']= []
        _DATA['Output']= []

    def mouseMoveEvent(self, event):
        super(MyScribble,self).mouseMoveEvent(event)
        self._input(event)

    def mouseReleaseEvent(self, event):
        super(MyScribble,self).mouseReleaseEvent(event)
        self._input(event)

class Algorithm(QGroupBox):
    def __init__(self, **kwargs):
        super(Algorithm,self).__init__(**kwargs)
        hbox = QHBoxLayout()
        select = Algorithm_Select()
        _DATA['Algorithm_Box']=select
        hbox.addWidget(select)
        button = Algorithm_Run()
        hbox.addWidget(button)
        self.setLayout(hbox)

class Algorithm_Select(QComboBox):
    def __init__(self, **kwargs):
        super(Algorithm_Select,self).__init__(**kwargs)
        for key in (loader[_DATA['Module_Name']].__dict__.keys()):
            print(key)
            if isinstance(loader[_DATA['Module_Name']].__dict__[key],callable.__class__):
                self.addItem(loader[_DATA['Module_Name']].__dict__[key].__name__)

class Algorithm_Run(QPushButton):
    def __init__(self, **kwargs):
        super(Algorithm_Run,self).__init__(**kwargs)
        self.setText("Run")
        self.clicked.connect(self.run)

    def run(self):
        if (len(_DATA['Output'])>0):
            _DATA['Input'] = _DATA['Output']
            _DATA['Output']= []
        try:
            log.debug("Invoking "+_DATA['Algorithm_Box'].currentText()+" with "+str(len(_DATA['Input']))+" Points...")
            log.info(_DATA['Input'])
            _DATA['Output'] = loader[_DATA['Module_Name']].__dict__[_DATA['Algorithm_Box'].currentText()](_DATA['Input'])
        #except:
        except BaseException as e:
            print(e)
            _DATA['Input']= []
            _DATA['Output']= []
        _DATA['MyScribble'].clearImage()
        _DATA['MyScribble'].drawData(_DATA['Input'],Qt.blue)
        _DATA['MyScribble'].drawData(_DATA['Output'],Qt.red)
        log.info("Size after call: Input "+str(len(_DATA['Input']))+", Output "+str(len(_DATA['Output'])))
            

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Editor")
    toolbox = QToolBar()

    algo_box = Algorithm()
    toolbox.addWidget(algo_box)

    window.addToolBar(toolbox)
    window.setCentralWidget(MyScribble())
    window.show()
    sys.exit(app.exec_())