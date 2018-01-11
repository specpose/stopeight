#!/usr/bin/env python

# Copyright (C) 2017 Fassio Blatter

from stopeight.util import runnable

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow,QToolBar,QGroupBox,QHBoxLayout
from PyQt5.QtCore import Qt

from stopeight.logging import logSwitch
log = logSwitch.logPrint()

# false if part of stopeight-clibs
_DATA = {'Modules': [('stopeight.legacy', False),
#                            ('stopeight.comparator.matrixTools',True),
                            ('stopeight.util.file', True),
                             ('stopeight.util.file_wave',True),
                            ('stopeight.analyzer', False),
                            ('stopeight.grapher', False)
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
        
from stopeight.util.editor_command import Algorithm_Select,Algorithm_Run,Connector
class ScribbleConnector(Connector):
    def __init__(self,command,scribble):
        super().__init__(command,[ScribbleBackup(),ScribbleData()],scribble)
        self.colors = [Qt.blue, Qt.red]

    def run(self):
        super().run()
        self._output.clearImage()
        #for d,c in self.data,self.colors:
            #self.scribble.plot(d,c)
        self._output.plot(ScribbleBackup(),self.colors[0])
        self._output.plot(ScribbleData(),self.colors[1])
    
if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Editor")

    #list or dict?
    connections = []


    from stopeight.util.wave_area import WaveArea
    wave = WaveArea()

    wbar = QToolBar()
    wgroup = QGroupBox()
    wbox = QtWidgets.QVBoxLayout()
    # Just some button connected to `plot` method
    plotbutton = QtWidgets.QPushButton('Plot')
    from stopeight.util import file_wave
    #wave.data = file_wave._open()
    #plotbutton.clicked.connect(wave.plot)
    # set the layout
    wbox.addWidget(wave.plotbar)
    wbox.addWidget(plotbutton)
    wgroup.setLayout(wbox)
    wbar.addWidget(wgroup)
    window.addToolBar(wbar)

    window.setCentralWidget(wave.canvas)
    #window.addDockWidget(Qt.TopDockWidgetArea,wave)    

    # Find modules
    scribbles = []
    from funcsigs import signature
    for module in _DATA['Modules']:
        #def zoo(a: str)->int:
        #if (signature(zoo).return_annotation!=Signature.empty):
        #if (signature(zoo).return_annotation==ScribbleData):
        scribbles.append(module)

    # Create results area
    from stopeight.util.scribble_area import ScribbleArea
    scribble = ScribbleArea()
    window.addDockWidget(Qt.BottomDockWidgetArea,scribble)

    # Hook up modules
    toolbox = QToolBar()
    #toolbox = QtWidgets.QDockWidget()
    from stopeight.util.editor_data import ScribbleData, ScribbleBackup
    for module in scribbles:
        connections.append(ScribbleConnector(module,scribble))
    for connection in connections:
        group = QGroupBox()
        box = QHBoxLayout()
        box.addWidget(connection.select)
        box.addWidget(connection.button)
        group.setLayout(box)
        toolbox.addWidget(group)
    window.addToolBar(Qt.BottomToolBarArea,toolbox)
    #window.addDockWidget(Qt.BottomDockWidgetArea,toolbox)
    
    window.show()
    sys.exit(app.exec_())
