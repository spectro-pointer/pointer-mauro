# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Wed Jan  7 14:54:29 2015
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
        MainWindow.resize(928, 672)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.graphicsView = QtGui.QGraphicsView(self.centralWidget)
        self.graphicsView.setMinimumSize(QtCore.QSize(720, 490))
        self.graphicsView.setMouseTracking(False)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.graphicsView.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 6)
        self.frame = QtGui.QFrame(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(340, 0))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.groupBox = QtGui.QGroupBox(self.frame)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 321, 71))
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
        self.radioButtonSteps.setGeometry(QtCore.QRect(260, 20, 61, 21))
        self.radioButtonSteps.setChecked(False)
        self.radioButtonSteps.setObjectName(_fromUtf8("radioButtonSteps"))
        self.buttonGroup.addButton(self.radioButtonSteps)
        self.lineEditSteps = QtGui.QLineEdit(self.groupBox)
        self.lineEditSteps.setGeometry(QtCore.QRect(270, 40, 51, 31))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditSteps.sizePolicy().hasHeightForWidth())
        self.lineEditSteps.setSizePolicy(sizePolicy)
        self.lineEditSteps.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEditSteps.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.lineEditSteps.setMaxLength(3)
        self.lineEditSteps.setObjectName(_fromUtf8("lineEditSteps"))
        self.gridLayout.addWidget(self.frame, 1, 0, 6, 1)
        self.label = QtGui.QLabel(self.centralWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.centralWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)
        self.pushButtonZoomIn = QtGui.QPushButton(self.centralWidget)
        self.pushButtonZoomIn.setObjectName(_fromUtf8("pushButtonZoomIn"))
        self.gridLayout.addWidget(self.pushButtonZoomIn, 1, 4, 2, 1)
        self.pushButtonUp = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonUp.sizePolicy().hasHeightForWidth())
        self.pushButtonUp.setSizePolicy(sizePolicy)
        self.pushButtonUp.setMinimumSize(QtCore.QSize(30, 0))
        self.pushButtonUp.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButtonUp.setObjectName(_fromUtf8("pushButtonUp"))
        self.gridLayout.addWidget(self.pushButtonUp, 1, 6, 2, 1)
        self.lineEditAz = QtGui.QLineEdit(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditAz.sizePolicy().hasHeightForWidth())
        self.lineEditAz.setSizePolicy(sizePolicy)
        self.lineEditAz.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEditAz.setMaxLength(11)
        self.lineEditAz.setReadOnly(True)
        self.lineEditAz.setObjectName(_fromUtf8("lineEditAz"))
        self.gridLayout.addWidget(self.lineEditAz, 2, 1, 2, 1)
        self.lineEditEl = QtGui.QLineEdit(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditEl.sizePolicy().hasHeightForWidth())
        self.lineEditEl.setSizePolicy(sizePolicy)
        self.lineEditEl.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEditEl.setMaxLength(11)
        self.lineEditEl.setReadOnly(True)
        self.lineEditEl.setObjectName(_fromUtf8("lineEditEl"))
        self.gridLayout.addWidget(self.lineEditEl, 2, 2, 2, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 3, 2, 1)
        self.pushButtonLeft = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonLeft.sizePolicy().hasHeightForWidth())
        self.pushButtonLeft.setSizePolicy(sizePolicy)
        self.pushButtonLeft.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButtonLeft.setObjectName(_fromUtf8("pushButtonLeft"))
        self.gridLayout.addWidget(self.pushButtonLeft, 3, 5, 2, 1)
        self.pushButtonAbort = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAbort.sizePolicy().hasHeightForWidth())
        self.pushButtonAbort.setSizePolicy(sizePolicy)
        self.pushButtonAbort.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButtonAbort.setObjectName(_fromUtf8("pushButtonAbort"))
        self.gridLayout.addWidget(self.pushButtonAbort, 3, 6, 2, 1)
        self.pushButtonRight = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonRight.sizePolicy().hasHeightForWidth())
        self.pushButtonRight.setSizePolicy(sizePolicy)
        self.pushButtonRight.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButtonRight.setObjectName(_fromUtf8("pushButtonRight"))
        self.gridLayout.addWidget(self.pushButtonRight, 3, 7, 2, 1)
        self.label_4 = QtGui.QLabel(self.centralWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 1, 2, 1)
        self.label_3 = QtGui.QLabel(self.centralWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 4, 2, 2, 1)
        self.pushButtonZoomOut = QtGui.QPushButton(self.centralWidget)
        self.pushButtonZoomOut.setObjectName(_fromUtf8("pushButtonZoomOut"))
        self.gridLayout.addWidget(self.pushButtonZoomOut, 5, 4, 2, 1)
        self.pushButtonDown = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonDown.sizePolicy().hasHeightForWidth())
        self.pushButtonDown.setSizePolicy(sizePolicy)
        self.pushButtonDown.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButtonDown.setObjectName(_fromUtf8("pushButtonDown"))
        self.gridLayout.addWidget(self.pushButtonDown, 5, 6, 2, 1)
        self.lineEditRA = QtGui.QLineEdit(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditRA.sizePolicy().hasHeightForWidth())
        self.lineEditRA.setSizePolicy(sizePolicy)
        self.lineEditRA.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEditRA.setMaxLength(11)
        self.lineEditRA.setReadOnly(True)
        self.lineEditRA.setObjectName(_fromUtf8("lineEditRA"))
        self.gridLayout.addWidget(self.lineEditRA, 6, 1, 1, 1)
        self.lineEditDec = QtGui.QLineEdit(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditDec.sizePolicy().hasHeightForWidth())
        self.lineEditDec.setSizePolicy(sizePolicy)
        self.lineEditDec.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEditDec.setMaxLength(11)
        self.lineEditDec.setReadOnly(True)
        self.lineEditDec.setObjectName(_fromUtf8("lineEditDec"))
        self.gridLayout.addWidget(self.lineEditDec, 6, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 928, 24))
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
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Pointer Gui-colimacion", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Step size", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonDegrees.setText(QtGui.QApplication.translate("MainWindow", "degrees", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonArcsecs.setText(QtGui.QApplication.translate("MainWindow", "arcsecs", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonArcmins.setText(QtGui.QApplication.translate("MainWindow", "arcmins", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonSteps.setText(QtGui.QApplication.translate("MainWindow", "steps", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditSteps.setText(QtGui.QApplication.translate("MainWindow", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Azimuth", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Elevation", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonZoomIn.setText(QtGui.QApplication.translate("MainWindow", "Zoom+", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonUp.setText(QtGui.QApplication.translate("MainWindow", "Up", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonLeft.setText(QtGui.QApplication.translate("MainWindow", "Left", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAbort.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonRight.setText(QtGui.QApplication.translate("MainWindow", "Right", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "RA", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Dec", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonZoomOut.setText(QtGui.QApplication.translate("MainWindow", "Zoom-", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDown.setText(QtGui.QApplication.translate("MainWindow", "Down", None, QtGui.QApplication.UnicodeUTF8))

