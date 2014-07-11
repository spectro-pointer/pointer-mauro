#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys

from PyQt4.QtCore import *
#from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtGui import *
from mainwindow import Ui_MainWindow as gui
#import gc

import cv2
import numpy as np
import pointer_cli_27 as pointer_cli

# Pointer server hostname
server_host = 'pi'

class Video():
    def __init__(self, capture):
        self.capture = capture
        self.currentFrame=np.array([])

    def captureNextFrame(self):
        """ 
            Capture frame, reverse RBG BGR, and return opencv image                                                                         
        """
        ret, readFrame=self.capture.read()
        if(ret==True):
            self.currentFrame=cv2.cvtColor(readFrame, cv2.COLOR_BGR2RGB)
        else:
            print 'No frame'

    def convertFrame(self):
        """
            Converts frame to format suitable for QtGui
        """
        try:
            height,width=self.currentFrame.shape[:2]
            img=QImage(self.currentFrame,
                              width,
                              height,
                              QImage.Format_RGB888)
            pixmap=QPixmap.fromImage(img)
#            self.previousFrame = self.currentFrame
            return pixmap
        except Exception as e:
            print 'convertFrame() exception:', e
            return None


class MainWindow(QMainWindow, gui):
    
    # Pointer GUI
    POINTERGUIVERSION = "0.0.2"

    def __init__(self, parent=None):

        QMainWindow.__init__(self)
        self.setupUi(self)

#        self.setWindowIcon(QIcon(QPixmap(":/icons/icons/pointer.png")))
        
        # Pointer client instance
        self.pointer = pointer_cli.Pointer_CLI()._getPointer(server_host)

        # Video capture
        fps=25
        captureTime = 1./fps*1000. # [ms]
        self.vcap = cv2.VideoCapture()  # generic

        """
            Video stream address: It may be an address of an mpeg stream, 
            e.g. "http://user:pass@cam_address:8081/cgi/mjpg/mjpg.cgi?.mjpg"
        """
        videoStreamAddress = 0 # webcam
#        videoStreamAddress = 'rtsp://' + server_host + ':8554/'

        """" Open the video stream, and make sure it's opened """
        if not self.vcap.open(videoStreamAddress):
            print "Error opening video stream or file"
            sys.exit(-1);
        
        self.video = Video(self.vcap)

        # Graphics scene
        self.graphicsScene = QGraphicsScene()
        self.videoFrame = QPixmap()
        self.pixmapItem = self.graphicsScene.addPixmap(self.videoFrame)
        
        # Crosshair
        self.red = QColor()
        self.red.setRedF(1)
        self.green = QColor()
        self.green.setGreenF(1)
#        self.white = QColor()
#        self.white.setRgb(255, 255, 255)

        self.x=0
        self.y=0
        self.ellipse=None
        self.line1=None
        self.line2=None
#        self.crosshair()
        
        self.graphicsView.setScene(self.graphicsScene)       
        
        #Create timers
        self.captureTimer = QTimer()

        #Connects
        self.connect(self.pushButtonUp, SIGNAL("pressed()"), self.OnPushButtonUpPressed)
        self.connect(self.pushButtonDown, SIGNAL("pressed()"), self.OnPushButtonDownPressed)
        self.connect(self.pushButtonRight, SIGNAL("pressed()"), self.OnPushButtonRightPressed)
        self.connect(self.pushButtonLeft, SIGNAL("pressed()"), self.OnPushButtonLeftPressed)
        self.connect(self.pushButtonAbort, SIGNAL("pressed()"), self.OnPushButtonAbortPressed)
        
        self.connect(self.captureTimer, SIGNAL("timeout()"), self.OnCaptureTimeout)
        
        self.connect(self.graphicsScene, SIGNAL("changed()"), self.OnSceneChanged)

        #Start timers
        self.captureTimer.start(captureTime)
        
#        desktop = QApplication.desktop();
#        self.screen_width = desktop.width();
#        self.screen_height = desktop.height();
#        print "Your resolution: " + str(self.screen_width) + "x" + str(self.screen_height)
        
#        self.events_mutex = QMutex()

        self.graphicsView.show()
        self.update()

    def OnPushButtonUpPressed(self):
#        QMessageBox.warning(self, "Warning", "<strong>Up</strong> pressed.")
        steps = float(self.plainTextSteps.toPlainText())
        if self.radioButtonArcmins.isChecked():
            steps /= 60.
        elif self.radioButtonArcsecs.isChecked():
            steps /= 3600.
        if self.radioButtonSteps.isChecked():
            self.pointer.move('X', steps)
        else:
            self.pointer.move('AzEl', 0, steps)

    def OnPushButtonDownPressed(self):
        steps = float(self.plainTextSteps.toPlainText())
        if self.radioButtonArcmins.isChecked():
            steps /= 60.
        elif self.radioButtonArcsecs.isChecked():
            steps /= 3600.
        if self.radioButtonSteps.isChecked():
            self.pointer.move('X', -steps)
        else:
            self.pointer.move('AzEl', 0, -steps)

    def OnPushButtonRightPressed(self):
        steps = float(self.plainTextSteps.toPlainText())
        if self.radioButtonArcmins.isChecked():
            steps /= 60.
        elif self.radioButtonArcsecs.isChecked():
            steps /= 3600.
        if self.radioButtonSteps.isChecked():
            self.pointer.move('Z', steps)
        else:
            self.pointer.move('AzEl', steps, 0)

    def OnPushButtonLeftPressed(self):
        steps = float(self.plainTextSteps.toPlainText())
        if self.radioButtonArcmins.isChecked():
            steps /= 60.
        elif self.radioButtonArcsecs.isChecked():
            steps /= 3600.
        if self.radioButtonSteps.isChecked():
            self.pointer.move('Z', -steps)
        else:
            self.pointer.move('AzEl', -steps, 0)
            
    def OnPushButtonAbortPressed(self):
        self.pointer.abort()
        
    def crosshair(self):
        r=8 # crosshair radius [pixels]
        c=2 # cross excess length [pixels]
        pen = QPen()
        pen.setColor(self.red) # crosshair color
        
        if self.ellipse:
            self.graphicsScene.removeItem(self.ellipse)
        if self.line1:
            self.graphicsScene.removeItem(self.line1)
        if self.line2:
            self.graphicsScene.removeItem(self.line2)
        
        self.x = self.graphicsScene.width() / 2
        self.y = self.graphicsScene.height() / 2
        self.ellipse=self.graphicsScene.addEllipse(self.x, self.y, r*2, r*2, pen)
        self.line1=self.graphicsScene.addLine(QLineF(self.x-c, self.y+r, self.x+2*r+c, self.y+r), pen)
        self.line2=self.graphicsScene.addLine(QLineF(self.x+r, self.y-c, self.x+r, self.y+2*r+c), pen)
        self.ellipse.setZValue(1)
        self.line1.setZValue(1)
        self.line2.setZValue(1)
#        self.graphicsView.show()


    def OnCaptureTimeout(self):
        try:
            self.video.captureNextFrame()
            self.videoFrame = self.video.convertFrame()
#            self.videoFrame.setScaledContents(True)
            self.graphicsScene.removeItem(self.pixmapItem)
            self.pixmapItem=self.graphicsScene.addPixmap(self.videoFrame)
            self.crosshair()
#            self.graphicsScene.emit(SIGNAL("changed()"))
#            self.graphicsView.show()
#            self.update()
#        except TypeError:
        except Exception as e:
            print "OnCaptureTimeout() exception:", e
    
    def OnSceneChanged(self, rect=None):
        print 'changed:', rect
        
if __name__ == "__main__":
    QApplication.setApplicationName("POINTERGUI");
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
#    window.MoveWindowToMiddle(window)
    sys.exit(app.exec_())
