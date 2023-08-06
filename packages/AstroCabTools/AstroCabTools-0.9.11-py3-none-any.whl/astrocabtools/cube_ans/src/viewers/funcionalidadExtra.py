import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from pubsub import pub

from .canvas_interaction.imageRangeCanvas.panZoom import figure_pz

import astrocabtools.cube_ans.src.ui.ui_funcionalidadExtra

__all__=["FuncionalidadExtra"]

class FuncionalidadExtra(QDialog, astrocabtools.cube_ans.src.ui.ui_funcionalidadExtra.Ui_funcionalidadExtra):
    rangeData = pyqtSignal(str, str, list, name='getRangeData')

    def __init__(self, parent=None):
        super(FuncionalidadExtra, self).__init__(parent)
        self.setupUi(self)

        self.create_spectrum_range_plot()

    def create_spectrum_range_plot(self):

        self.spectrumFigure, self.spectrumFigure.canvas = figure_pz()
        self.spectrumFigure.pan_zoom.connect_zoom()
        self.spectrumFigure.pan_zoom.connect_pan()
        self.ax = self.spectrumFigure.add_subplot(111)
        self.ax.set_visible(False)

        self.functionalidad_vbox.addWidget(self.spectrumFigure.canvas)

    def get_rectangle_data(self, centerX, centerY, width, height):
        self.spectrumFigure.pan_zoom.hide_ellipse()
        self.spectrumFigure.pan_zoom.show_rectangle()
        self.spectrumFigure.pan_zoom.draw_rectangle(centerX, centerY, width, height)

    def get_ellipse_data(self, centerX, centerY, aAxis, bAxis):
        self.spectrumFigure.pan_zoom.hide_rectangle()
        self.spectrumFigure.pan_zoom.show_ellipse()
        self.spectrumFigure.pan_zoom.draw_ellipse(centerX, centerY, aAxis, bAxis)

    def draw_image(self, iw, ew, data):
        """Draw the image after operations have been applied
        :param int iw: left x wavelength value
        :param int ew: right x wavelength value
        :param np.ndarray data: sum of the data across all the slices
        """
        range_text = "Initial wavelength: "+iw+" - End wavelength:"+ew
        self.rangeLabel.setText(range_text)
        self.ax.set_visible(True)
        self.ax.clear()
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.ax.imshow(data)

        self.spectrumFigure.canvas.draw()

    def show_file_extension_alert(self):
        alert = QMessageBox()
        alert.setText("Error")
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()
