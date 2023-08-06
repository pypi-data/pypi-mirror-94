import numpy as np
import math

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot

from pubsub import pub

import astrocabtools.cube_ans.src.ui.ui_backgroundSubstraction

__all__=["BackgroundSubstraction"]

class BackgroundSubstraction(QDialog, astrocabtools.cube_ans.src.ui.ui_backgroundSubstraction.Ui_backgroundSubstraction):

    def __init__(self, parent=None):
        super(BackgroundSubstraction, self).__init__(parent)
        self.setupUi(self)

        self.firstRadiusLineEdit.setValidator(QtGui.QDoubleValidator())
        self.secondRadiusLineEdit.setValidator(QtGui.QDoubleValidator())

        self.firstCircleButton.clicked.connect(self.send_data_first_wedge)
        self.secondCircleButton.clicked.connect(self.send_data_second_wedge)

    @pyqtSlot()
    def send_data_first_wedge(self):
        pub.sendMessage('firstWedgeSelected', centerX = float(self.xCenterLineEdit.text()),
                       centerY = float(self.yCenterLineEdit.text()), radius = float(self.firstRadiusLineEdit.text()))

    @pyqtSlot()
    def send_data_second_wedge(self):
        pub.sendMessage('secondWedgeSelected', centerX = float(self.xCenterLineEdit.text()),
                       centerY = float(self.yCenterLineEdit.text()), radius = float(self.firstRadiusLineEdit.text()))

    def update_center_data(self, centerX, centerY):
        self.xCenterLineEdit.setText(str(centerX))
        self.yCenterLineEdit.setText(str(centerY))

    def generic_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.setDetailedText(traceback.format_exc())
        alert.exec_()
