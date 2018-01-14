# https://stackoverflow.com/questions/12459811/how-to-embed-matplotlib-in-pyqt-for-dummies
# https://stackoverflow.com/questions/18625085/how-to-plot-a-wav-file

import sys
import numpy

from PyQt5 import QtGui,QtWidgets
from PyQt5.QtWidgets import QGroupBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from stopeight.util.editor.data import WaveData

class WaveArea(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(WaveArea, self).__init__(parent)

        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.plotbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        #self.button = QtWidgets.QPushButton('Plot')
        #self.button.clicked.connect(self.plot)

        # set the layout
        #layout = QtWidgets.QVBoxLayout()
        #layout.addWidget(self.toolbar)
        #layout.addWidget(self.canvas)
        #layout.addWidget(self.button)
        #self.setLayout(layout)

    def __call__(self,data:WaveData,clear=True):
        if clear:
            self.clearImage()
        self.plot(data)


    def clearImage(self):
        # discards the old graph
        self.ax.clear()

    def plot(self, samples, **kwargs):
        ''' plot some random stuff '''
        # create an axis
        self.ax = self.figure.add_subplot(111)
        #self.ax.figure(1)

        #ax.title("Signal Wave...")
        self.ax.plot(samples)

        #self.ax.set_ylabel([])
        #self.ax.set_xlabel([])

        # Turn off tick labels
        #self.ax.set_yticklabels([])
        #self.ax.set_xticklabels([])

        #self.ax.show()
        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = WaveArea()
    main.show()
    sys.exit(app.exec_())
