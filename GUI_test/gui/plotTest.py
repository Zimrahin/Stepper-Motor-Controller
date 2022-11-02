import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import random

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on ·container"
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas_wdg = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar_wdg = NavigationToolbar(self.canvas_wdg)

        # Just some button connected to `plot` method
        self.button_wdg = QPushButton('Plot')
        self.button_wdg.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar_wdg)
        layout.addWidget(self.canvas_wdg)
        layout.addWidget(self.button_wdg)
        self.setLayout(layout)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # plt.style.use('dark_background')
        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.clear()
        # plt.cla()
        # plt.figure.patch.set_facecolor('#000000')

        # ax.figure.gca().set_ylim(0, 3.2)

        

        # plot data
        ax.plot(data, '*-')
        ax.set_ylabel('Voltage')
        ax.grid()
        ax.figure.tight_layout()

        # refresh canvas
        self.canvas_wdg.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())