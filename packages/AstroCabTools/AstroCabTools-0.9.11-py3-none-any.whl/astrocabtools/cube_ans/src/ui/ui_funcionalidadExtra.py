# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'funcionalidadExtra.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_funcionalidadExtra(object):
    def setupUi(self, funcionalidadExtra):
        funcionalidadExtra.setObjectName("funcionalidadExtra")
        funcionalidadExtra.setWindowModality(QtCore.Qt.NonModal)
        funcionalidadExtra.resize(600, 600)
        funcionalidadExtra.setMinimumSize(QtCore.QSize(600, 600))
        self.gridLayout_2 = QtWidgets.QGridLayout(funcionalidadExtra)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(funcionalidadExtra)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.functionalidad_vbox = QtWidgets.QVBoxLayout()
        self.functionalidad_vbox.setObjectName("functionalidad_vbox")
        self.verticalLayout_3.addLayout(self.functionalidad_vbox)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.rangeLabel = QtWidgets.QLabel(funcionalidadExtra)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rangeLabel.sizePolicy().hasHeightForWidth())
        self.rangeLabel.setSizePolicy(sizePolicy)
        self.rangeLabel.setText("")
        self.rangeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.rangeLabel.setObjectName("rangeLabel")
        self.gridLayout.addWidget(self.rangeLabel, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(funcionalidadExtra)
        QtCore.QMetaObject.connectSlotsByName(funcionalidadExtra)

    def retranslateUi(self, funcionalidadExtra):
        _translate = QtCore.QCoreApplication.translate
        funcionalidadExtra.setWindowTitle(_translate("funcionalidadExtra", "funcionalidadExtra"))

