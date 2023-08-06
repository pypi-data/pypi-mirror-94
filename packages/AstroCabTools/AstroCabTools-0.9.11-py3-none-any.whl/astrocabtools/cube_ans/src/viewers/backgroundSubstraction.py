import numpy as np
import math

import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5 import QtGui

from pubsub import pub

from ..utils.ellipse_xy_transformations import background_substraction

import astrocabtools.cube_ans.src.ui.ui_backgroundSubstraction

__all__=["BackgroundSubstraction"]

class BackgroundSubstraction(QDialog, astrocabtools.cube_ans.src.ui.ui_backgroundSubstraction.Ui_backgroundSubstraction):

    innerWedgeSelected = pyqtSignal(float, float, float, name='innerEmit')
    outerWedgeSelected = pyqtSignal(float, float, float, name='outerEmit')
    annulus_data = pyqtSignal()

    def __init__(self, parent=None):
        super(BackgroundSubstraction, self).__init__(parent)
        self.setupUi(self)

        self.innerRadiusLineEdit.setValidator(QtGui.QDoubleValidator())
        self.outerRadiusLineEdit.setValidator(QtGui.QDoubleValidator())

        self.innerCircleButton.clicked.connect(self.send_data_inner_wedge)
        self.outerCircleButton.clicked.connect(self.send_data_outer_wedge)

        self.applyButton.clicked.connect(self.get_background)

    @pyqtSlot()
    def send_data_inner_wedge(self):

        radius_value = float(self.innerRadiusLineEdit.text())
        self.innerWedgeSelected.emit(self.xCenter, self.yCenter,radius_value)

    @pyqtSlot()
    def send_data_outer_wedge(self):
        radius_value = float(self.outerRadiusLineEdit.text())
        self.outerWedgeSelected.emit(self.xCenter, self.yCenter,radius_value)

    @pyqtSlot()
    def get_background(self):
        try:
            self.annulus_mask = background_substraction(self.xCenter, self.yCenter, float(self.innerRadiusLineEdit.text()) + self.xCenter,
                                                float(self.outerRadiusLineEdit.text()) + self.xCenter,
                                                float(self.innerRadiusLineEdit.text())+ self.yCenter,
                                                float(self.outerRadiusLineEdit.text())+ self.yCenter)
            self.annulus_data.emit()
        except Exception as e:
            self.generic_alert("Error")

    def update_center_data(self, center_point):
        self.xCenter = center_point[1][0]
        self.yCenter = center_point[1][1]

        self.aAxis = center_point[0][2]/2
        self.bAxis = center_point[0][3]/2
        self.xCenterLineEdit.setText(str(round(center_point[1][0],4)))
        self.yCenterLineEdit.setText(str(round(center_point[1][1],4)))

    def return_mask(self):
        return self.annulus_mask

    def generic_alert(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.ssetDetailedText(traceback.format_exc())
        alert.exec_()
