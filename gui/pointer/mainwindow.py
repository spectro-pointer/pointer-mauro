# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sat Jul 12 14:41:59 2014
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
        MainWindow.resize(738, 666)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame = QtGui.QFrame(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(330, 0))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.groupBox = QtGui.QGroupBox(self.frame)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 331, 51))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.radioButtonDegrees = QtGui.QRadioButton(self.groupBox)
        self.radioButtonDegrees.setGeometry(QtCore.QRect(10, 20, 80, 21))
        self.radioButtonDegrees.setChecked(True)
        self.radioButtonDegrees.setObjectName(_fromUtf8("radioButtonDegrees"))
        self.buttonGroup = QtGui.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.radioButtonDegrees)
        self.radioButtonArcsecs = QtGui.QRadioButton(self.groupBox)
        self.radioButtonArcsecs.setGeometry(QtCore.QRect(180, 20, 75, 21))
        self.radioButtonArcsecs.setObjectName(_fromUtf8("radioButtonArcsecs"))
        self.buttonGroup.addButton(self.radioButtonArcsecs)
        self.radioButtonArcmins = QtGui.QRadioButton(self.groupBox)
        self.radioButtonArcmins.setGeometry(QtCore.QRect(100, 20, 78, 21))
        self.radioButtonArcmins.setObjectName(_fromUtf8("radioButtonArcmins"))
        self.buttonGroup.addButton(self.radioButtonArcmins)
        self.radioButtonSteps = QtGui.QRadioButton(self.groupBox)
        self.radioButtonSteps.setGeometry(QtCore.QRect(260, 20, 64, 21))
        self.radioButtonSteps.setChecked(False)
        self.radioButtonSteps.setObjectName(_fromUtf8("radioButtonSteps"))
        self.buttonGroup.addButton(self.radioButtonSteps)
        self.lineEditSteps = QtGui.QLineEdit(self.frame)
        self.lineEditSteps.setGeometry(QtCore.QRect(260, 50, 60, 26))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditSteps.sizePolicy().hasHeightForWidth())
        self.lineEditSteps.setSizePolicy(sizePolicy)
        self.lineEditSteps.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEditSteps.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.lineEditSteps.setMaxLength(3)
        self.lineEditSteps.setObjectName(_fromUtf8("lineEditSteps"))
        self.gridLayout.addWidget(self.frame, 1, 0, 3, 1)
        self.pushButtonDown = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonDown.sizePolicy().hasHeightForWidth())
        self.pushButtonDown.setSizePolicy(sizePolicy)
        self.pushButtonDown.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButtonDown.setObjectName(_fromUtf8("pushButtonDown"))
        self.gridLayout.addWidget(self.pushButtonDown, 3, 3, 1, 1)
        self.pushButtonLeft = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonLeft.sizePolicy().hasHeightForWidth())
        self.pushButtonLeft.setSizePolicy(sizePolicy)
        self.pushButtonLeft.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButtonLeft.setObjectName(_fromUtf8("pushButtonLeft"))
        self.gridLayout.addWidget(self.pushButtonLeft, 2, 2, 1, 1)
        self.graphicsView = QtGui.QGraphicsView(self.centralWidget)
        self.graphicsView.setMinimumSize(QtCore.QSize(720, 490))
        self.graphicsView.setMouseTracking(False)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.graphicsView.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 5)
        self.pushButtonAbort = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAbort.sizePolicy().hasHeightForWidth())
        self.pushButtonAbort.setSizePolicy(sizePolicy)
        self.pushButtonAbort.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButtonAbort.setObjectName(_fromUtf8("pushButtonAbort"))
        self.gridLayout.addWidget(self.pushButtonAbort, 2, 3, 1, 1)
        self.pushButtonUp = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonUp.sizePolicy().hasHeightForWidth())
        self.pushButtonUp.setSizePolicy(sizePolicy)
        self.pushButtonUp.setMinimumSize(QtCore.QSize(30, 0))
        self.pushButtonUp.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButtonUp.setObjectName(_fromUtf8("pushButtonUp"))
        self.gridLayout.addWidget(self.pushButtonUp, 1, 3, 1, 1)
        self.pushButtonRight = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonRight.sizePolicy().hasHeightForWidth())
        self.pushButtonRight.setSizePolicy(sizePolicy)
        self.pushButtonRight.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButtonRight.setObjectName(_fromUtf8("pushButtonRight"))
        self.gridLayout.addWidget(self.pushButtonRight, 2, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 738, 24))
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
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Step size", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonDegrees.setText(QtGui.QApplication.translate("MainWindow", "degrees", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonArcsecs.setText(QtGui.QApplication.translate("MainWindow", "arcsecs", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonArcmins.setText(QtGui.QApplication.translate("MainWindow", "arcmins", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonSteps.setText(QtGui.QApplication.translate("MainWindow", "steps", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditSteps.setText(QtGui.QApplication.translate("MainWindow", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDown.setText(QtGui.QApplication.translate("MainWindow", "Down", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonLeft.setText(QtGui.QApplication.translate("MainWindow", "Left", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAbort.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonUp.setText(QtGui.QApplication.translate("MainWindow", "Up", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonRight.setText(QtGui.QApplication.translate("MainWindow", "Right", None, QtGui.QApplication.UnicodeUTF8))

