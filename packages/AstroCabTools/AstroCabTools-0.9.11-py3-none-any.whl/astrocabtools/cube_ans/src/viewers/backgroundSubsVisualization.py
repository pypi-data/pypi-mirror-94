import numpy as np
import math

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5 import QtGui

from pubsub import pub

import matplotlib.pyplot as plt

import astrocabtools.cube_ans.src.ui.ui_backgroundSubsVisualization

__all__=["BackgroundSubsVisualization"]

class BackgroundSubsVisualization(QDialog, astrocabtools.cube_ans.src.ui.ui_backgroundSubsVisualization.Ui_backgroundSubsVisualization):

    def __init__(self, parent=None):
        super(BackgroundSubsVisualization, self).__init__(parent)
        self.setupUi(self)
        self.create_axes()
        self.saveButton.clicked.connect(self.save)


    @pyqtSlot()
    def save(self):
        """ Save the image as a .png file"""
        try:
            fileSave = QFileDialog()
            name = fileSave.getSaveFileName(self, 'Save File')

            self.spectrumFigure.savefig(name[0], dpi = 600)
        except Exception as e:
            self.generic_alert()

    def create_axes(self):
        """Create the layout that will show the slice selected of a cube"""
        #self.backgroundFigure, self.backgroundFigure.cavas = figure_pz()
        self.backgroundFigure, self.ax = plt.subplots()
        self.backgroundFigure.constrained_layout = True
        self.ax = self.backgroundFigure.add_subplot(111)
        self.ax.set_visible(False)

        print(self.backgroundFigure.canvas)
        self.backgroundSubs_vbox.addWidget(self.backgroundFigure.canvas)

    def draw_cube(self,image, x_lim = None, y_lim = None):

        self.ax.set_visible(True)
        self.ax.clear()
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.ax.imshow(image)

        #Set x and y limits in case the previous figure had been zoomed or moved
        if x_lim is not None:
            self.ax.set_xlim(x_lim)
            self.ax.set_ylim(y_lim)

        self.backgroundFigure.canvas.draw()

    def generic_alert(self):
        alert = QMessageBox()
        alert.setText("Error")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()
