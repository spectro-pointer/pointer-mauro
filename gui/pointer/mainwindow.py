# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Thu Jul 10 15:59:39 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(739, 707)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.pushButtonUp = QtGui.QPushButton(self.centralWidget)
        self.pushButtonUp.setGeometry(QtCore.QRect(530, 420, 90, 27))
        self.pushButtonUp.setObjectName(_fromUtf8("pushButtonUp"))
        self.pushButtonDown = QtGui.QPushButton(self.centralWidget)
        self.pushButtonDown.setGeometry(QtCore.QRect(530, 480, 90, 27))
        self.pushButtonDown.setObjectName(_fromUtf8("pushButtonDown"))
        self.pushButtonLeft = QtGui.QPushButton(self.centralWidget)
        self.pushButtonLeft.setGeometry(QtCore.QRect(430, 450, 90, 27))
        self.pushButtonLeft.setObjectName(_fromUtf8("pushButtonLeft"))
        self.pushButtonRight = QtGui.QPushButton(self.centralWidget)
        self.pushButtonRight.setGeometry(QtCore.QRect(630, 450, 90, 27))
        self.pushButtonRight.setObjectName(_fromUtf8("pushButtonRight"))
        self.graphicsView = QtGui.QGraphicsView(self.centralWidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, -10, 720, 405))
        self.graphicsView.setMinimumSize(QtCore.QSize(720, 405))
        self.graphicsView.setMouseTracking(False)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.frame = QtGui.QFrame(self.centralWidget)
        self.frame.setGeometry(QtCore.QRect(410, 520, 321, 111))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.groupBox = QtGui.QGroupBox(self.frame)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 321, 111))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.radioButtonDegrees = QtGui.QRadioButton(self.groupBox)
        self.radioButtonDegrees.setGeometry(QtCore.QRect(10, 20, 81, 21))
        self.radioButtonDegrees.setChecked(True)
        self.radioButtonDegrees.setObjectName(_fromUtf8("radioButtonDegrees"))
        self.buttonGroup = QtGui.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.radioButtonDegrees)
        self.radioButtonArcsecs = QtGui.QRadioButton(self.groupBox)
        self.radioButtonArcsecs.setGeometry(QtCore.QRect(170, 20, 71, 21))
        self.radioButtonArcsecs.setObjectName(_fromUtf8("radioButtonArcsecs"))
        self.buttonGroup.addButton(self.radioButtonArcsecs)
        self.radioButtonArcmins = QtGui.QRadioButton(self.groupBox)
        self.radioButtonArcmins.setGeometry(QtCore.QRect(90, 20, 71, 21))
        self.radioButtonArcmins.setObjectName(_fromUtf8("radioButtonArcmins"))
        self.buttonGroup.addButton(self.radioButtonArcmins)
        self.radioButtonSteps = QtGui.QRadioButton(self.groupBox)
        self.radioButtonSteps.setGeometry(QtCore.QRect(250, 20, 61, 21))
        self.radioButtonSteps.setChecked(False)
        self.radioButtonSteps.setObjectName(_fromUtf8("radioButtonSteps"))
        self.buttonGroup.addButton(self.radioButtonSteps)
        self.plainTextSteps = QtGui.QPlainTextEdit(self.groupBox)
        self.plainTextSteps.setGeometry(QtCore.QRect(260, 50, 51, 31))
        self.plainTextSteps.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.plainTextSteps.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhFormattedNumbersOnly)
        self.plainTextSteps.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.plainTextSteps.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.plainTextSteps.setObjectName(_fromUtf8("plainTextSteps"))
        self.pushButtonAbort = QtGui.QPushButton(self.centralWidget)
        self.pushButtonAbort.setGeometry(QtCore.QRect(530, 450, 90, 27))
        self.pushButtonAbort.setObjectName(_fromUtf8("pushButtonAbort"))
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 739, 24))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Pointer Gui", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonUp.setText(QtGui.QApplication.translate("MainWindow", "Up", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDown.setText(QtGui.QApplication.translate("MainWindow", "Down", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonLeft.setText(QtGui.QApplication.translate("MainWindow", "Left", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonRight.setText(QtGui.QApplication.translate("MainWindow", "Right", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Step size", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonDegrees.setText(QtGui.QApplication.translate("MainWindow", "degrees", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonArcsecs.setText(QtGui.QApplication.translate("MainWindow", "arcsecs", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonArcmins.setText(QtGui.QApplication.translate("MainWindow", "arcmins", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonSteps.setText(QtGui.QApplication.translate("MainWindow", "steps", None, QtGui.QApplication.UnicodeUTF8))
        self.plainTextSteps.setPlainText(QtGui.QApplication.translate("MainWindow", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAbort.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))

