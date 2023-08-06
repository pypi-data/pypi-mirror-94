# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'backgroundSubsVisualization.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_backgroundSubsVisualization(object):
    def setupUi(self, backgroundSubsVisualization):
        backgroundSubsVisualization.setObjectName("backgroundSubsVisualization")
        backgroundSubsVisualization.resize(657, 577)
        self.gridLayout_2 = QtWidgets.QGridLayout(backgroundSubsVisualization)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(backgroundSubsVisualization)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.backgroundSubs_vbox = QtWidgets.QVBoxLayout()
        self.backgroundSubs_vbox.setObjectName("backgroundSubs_vbox")
        self.verticalLayout_2.addLayout(self.backgroundSubs_vbox)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.saveButton = QtWidgets.QPushButton(backgroundSubsVisualization)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(backgroundSubsVisualization)
        QtCore.QMetaObject.connectSlotsByName(backgroundSubsVisualization)

    def retranslateUi(self, backgroundSubsVisualization):
        _translate = QtCore.QCoreApplication.translate
        backgroundSubsVisualization.setWindowTitle(_translate("backgroundSubsVisualization", "backgroundSubstractionVisualization"))
        self.saveButton.setText(_translate("backgroundSubsVisualization", "Save as png"))

