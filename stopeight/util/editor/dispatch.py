#!/usr/bin/env python

# Copyright (C) 2017 Fassio Blatter

from stopeight.util import runnable

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow,QToolBar,QGroupBox,QHBoxLayout

from stopeight.logging import logSwitch
log = logSwitch.logNone()

# false if part of stopeight-clibs
_DATA = {'Modules': [('stopeight.util.editor.modules.legacy', False),
#                            ('stopeight.comparator.matrixTools',True),
                            ('stopeight.util.editor.modules.file', True),
                             ('stopeight.util.editor.modules.file_wave',True),
                            ('stopeight.util.editor.modules.analyzer', False),
                            ('stopeight.util.editor.modules.grapher', False)
                    ]
         }

import importlib
for module in _DATA['Modules']:
    try:
        importlib.import_module(module[0])
        #output class name
        log.warning("Successfully imported module "+module[0])
    except ImportError as ie:
        log.warning(ie)
        log.warning("Install stopeight-clibs and reinstall stopeight afterwards to use module "+module[0])
        _DATA['Modules'].remove(module)
    except:
        log.warning("Module "+module[0]+" not loaded!")
        _DATA['Modules'].remove(module)
                
if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Editor")

    #list or dict?
    connections = []

    outputs = []
    from stopeight.util.editor.wave import WaveArea
    wave = WaveArea()
    outputs.append(wave)
    
    wbar = QToolBar()
    wgroup = QGroupBox()
    wbox = QtWidgets.QVBoxLayout()
    # Just some button connected to `plot` method
    plotbutton = QtWidgets.QPushButton('Plot')
    #from stopeight.util.editor.modules import file_wave
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

    # Create results area
    from stopeight.util.editor.scribble import ScribbleArea
    scribble = ScribbleArea()
    outputs.append(scribble)
    from PyQt5.QtCore import Qt
    window.addDockWidget(Qt.BottomDockWidgetArea,scribble)

    # Find modules
    callables = []
    for module in _DATA['Modules']:
        callables.append(module)

    # Hook up modules
    toolbox = QToolBar()
    #toolbox = QtWidgets.QDockWidget()
    from stopeight.util.editor.command import Connector
    for module in callables:
        connections.append(Connector(module,outputs))
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
