# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'backgroundSubstraction.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_backgroundSubstraction(object):
    def setupUi(self, backgroundSubstraction):
        backgroundSubstraction.setObjectName("backgroundSubstraction")
        backgroundSubstraction.resize(400, 129)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(backgroundSubstraction.sizePolicy().hasHeightForWidth())
        backgroundSubstraction.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtWidgets.QGridLayout(backgroundSubstraction)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.innerRadiusLineEdit = QtWidgets.QLineEdit(backgroundSubstraction)
        self.innerRadiusLineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.innerRadiusLineEdit.setObjectName("innerRadiusLineEdit")
        self.gridLayout.addWidget(self.innerRadiusLineEdit, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(backgroundSubstraction)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.applyButton = QtWidgets.QPushButton(backgroundSubstraction)
        self.applyButton.setObjectName("applyButton")
        self.gridLayout.addWidget(self.applyButton, 3, 0, 1, 3)
        self.label_2 = QtWidgets.QLabel(backgroundSubstraction)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.innerCircleButton = QtWidgets.QPushButton(backgroundSubstraction)
        self.innerCircleButton.setObjectName("innerCircleButton")
        self.gridLayout.addWidget(self.innerCircleButton, 1, 2, 1, 1)
        self.outerRadiusLineEdit = QtWidgets.QLineEdit(backgroundSubstraction)
        self.outerRadiusLineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.outerRadiusLineEdit.setObjectName("outerRadiusLineEdit")
        self.gridLayout.addWidget(self.outerRadiusLineEdit, 2, 1, 1, 1)
        self.outerCircleButton = QtWidgets.QPushButton(backgroundSubstraction)
        self.outerCircleButton.setObjectName("outerCircleButton")
        self.gridLayout.addWidget(self.outerCircleButton, 2, 2, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(backgroundSubstraction)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.xCenterLineEdit = QtWidgets.QLineEdit(backgroundSubstraction)
        self.xCenterLineEdit.setReadOnly(True)
        self.xCenterLineEdit.setObjectName("xCenterLineEdit")
        self.horizontalLayout.addWidget(self.xCenterLineEdit)
        self.label_4 = QtWidgets.QLabel(backgroundSubstraction)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.yCenterLineEdit = QtWidgets.QLineEdit(backgroundSubstraction)
        self.yCenterLineEdit.setObjectName("yCenterLineEdit")
        self.horizontalLayout.addWidget(self.yCenterLineEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 3)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(backgroundSubstraction)
        QtCore.QMetaObject.connectSlotsByName(backgroundSubstraction)

    def retranslateUi(self, backgroundSubstraction):
        _translate = QtCore.QCoreApplication.translate
        backgroundSubstraction.setWindowTitle(_translate("backgroundSubstraction", "backgroundSubstraction"))
        self.label.setText(_translate("backgroundSubstraction", "Radius of inner circle"))
        self.applyButton.setText(_translate("backgroundSubstraction", "Apply background substraction"))
        self.label_2.setText(_translate("backgroundSubstraction", "Radius of outer circle"))
        self.innerCircleButton.setText(_translate("backgroundSubstraction", "Create inner circle"))
        self.outerCircleButton.setText(_translate("backgroundSubstraction", "Create outer circle"))
        self.label_3.setText(_translate("backgroundSubstraction", "X Center"))
        self.label_4.setText(_translate("backgroundSubstraction", "Y Center"))

