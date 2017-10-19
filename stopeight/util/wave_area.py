# https://stackoverflow.com/questions/12459811/how-to-embed-matplotlib-in-pyqt-for-dummies
# https://stackoverflow.com/questions/18625085/how-to-plot-a-wav-file

import sys
from PyQt5 import QtGui,QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import random

class WaveArea(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WaveArea, self).__init__(parent)

        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QtWidgets.QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.INPUT = []
        self.OUTPUT = []

    def plot(self):
        ''' plot some random stuff '''
        import matplotlib.pyplot as ax
        import numpy as np
        import wave
        import sys

        print("Opening "+sys.argv[1])
        spf = wave.open(sys.argv[1],'r')

        #Extract Raw Audio from Wav File
        signal = spf.readframes(-1)
        signal = np.fromstring(signal, 'Int16')

        #If Stereo
        if spf.getnchannels() == 2:
            print("Just mono files")
        else:
            # create an axis
            ax = self.figure.add_subplot(111)
            #ax.figure(1)

            # discards the old graph
            #ax.clear()

            #ax.title("Signal Wave...")
            ax.plot(signal)

            #ax.set_ylabel([])
            #ax.set_xlabel([])

            # Turn off tick labels
            #ax.set_yticklabels([])
            #ax.set_xticklabels([])

            #ax.show()
            # refresh canvas
            self.canvas.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = WaveArea()
    main.show()
    sys.exit(app.exec_())
