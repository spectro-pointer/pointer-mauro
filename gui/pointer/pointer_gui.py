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

POINTER_SERVER='pi'

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
    POINTERGUIVERSION = "0.0.1"

    def __init__(self, parent=None):

        QMainWindow.__init__(self)
        self.setupUi(self)

#        self.setWindowIcon(QIcon(QPixmap(":/icons/icons/pointer.png")))

        # Video capture
        fps=25
        CAPTURE_TIMER_TIME = 1./fps*1000. # [ms]
#        self.vcap = cv2.VideoCapture(0) # webcam
        self.vcap = cv2.VideoCapture()  # generic

        """
            it may be an address of an r stream, 
            e.g. "http://user:pass@cam_address:8081/cgi/mjpg/mjpg.cgi?.mjpg"
        """
        videoStreamAddress = 'rtsp://' + POINTER_SERVER + ':8554/'

        """"open the video stream and make sure it's opened """
        if not self.vcap.open(videoStreamAddress):
            print "Error opening video stream or file"
            sys.exit(-1);
        self.video = Video(self.vcap)

        # Graphics scene
        self.videoFrame = QPixmap()

        self.graphicsScene = QGraphicsScene()
#        self.graphicsScene.addText("Hello, world!")
        
        self.pixmapItem = self.graphicsScene.addPixmap(self.videoFrame)

        self.graphicsView.setScene(self.graphicsScene)
        
        #Create timers
        self.capture_timer = QTimer()

        #Connects
        self.connect(self.pushButtonUp, SIGNAL("pressed()"), self.OnPushButtonUpPressed)
        self.connect(self.pushButtonDown, SIGNAL("pressed()"), self.OnPushButtonDownPressed)
        self.connect(self.pushButtonRight, SIGNAL("pressed()"), self.OnPushButtonRightPressed)
        self.connect(self.pushButtonLeft, SIGNAL("pressed()"), self.OnPushButtonLeftPressed)
        
        self.connect(self.capture_timer, SIGNAL("timeout()"), self.OnCaptureTimeout)

        #Start timers
        self.capture_timer.start(CAPTURE_TIMER_TIME)
        
#        desktop = QApplication.desktop();
#        self.screen_width = desktop.width();
#        self.screen_height = desktop.height();
#        print "Your resolution: " + str(self.screen_width) + "x" + str(self.screen_height)
        
#        self.events_mutex = QMutex()

        self.graphicsView.show()
        self.update()

    def OnPushButtonUpPressed(self):
        QMessageBox.warning(self, "Warning", "<strong>Up</strong> pressed.")

    def OnPushButtonDownPressed(self):
        QMessageBox.warning(self, "Warning", "<strong>Down</strong> pressed.")

    def OnPushButtonRightPressed(self):
        QMessageBox.warning(self, "Warning", "<strong>Right</strong> pressed.")

    def OnPushButtonLeftPressed(self):
        QMessageBox.warning(self, "Warning", "<strong>Left</strong> pressed.")
        
    def OnCaptureTimeout(self):
        try:
            self.video.captureNextFrame()
            self.videoFrame = self.video.convertFrame()
#            self.videoFrame.setScaledContents(True)
            self.graphicsScene.removeItem(self.pixmapItem)
            self.pixmapItem=self.graphicsScene.addPixmap(self.videoFrame)
#            self.graphicsView.show()
#            self.update()
        except TypeError:
            print "No frame"

if __name__ == "__main__":
    QApplication.setApplicationName("POINTERGUI");
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
#    window.MoveWindowToMiddle(window)
    sys.exit(app.exec_())
