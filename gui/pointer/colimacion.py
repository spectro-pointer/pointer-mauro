#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4.Qt

from mainwindow import Ui_MainWindow as gui
#import gc

import pointer_cli_27 as pointer_cli

# Video/Picamwera stuff
from video_27 import Video

class GuiVideo(Video):
    """ A Video class with QImage conversion """
    def __init__(self, *args):
        Video.__init__(self, *args)
        
    def convertFrame(self):
        """
            Converts frame to format suitable for QtGui
        """
        try:
            height, width=self.currentFrame.shape[:2]
            img=QImage(self.currentFrame,
                       width,
                       height,
                       QImage.Format_RGB888)
            pixmap=QPixmap.fromImage(img)
#            self.previousFrame = self.currentFrame
            return pixmap
        except Exception as e:
            print >>sys.stderr, 'Exception: convertFrame():', e
            return None

# Pointer server hostname/IP
pointer_server = '192.168.0.101'
#pointer_server = 'pi'
# Camera server hostname/IP
camera_server = '192.168.0.100'
#camera_server = 'picamera'
       
class GraphicsPixmapItem(QGraphicsPixmapItem):
    def __init__(self, main=None):
        super(QGraphicsPixmapItem, self).__init__()
        self.main = main

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            centerx = self.pixmap().width()/2
            centery = self.pixmap().height()/2
            point = event.pos()
            x = point.x()
            y = point.y()
            print 'X_a:', x
            print 'Y_a:', y
            if self.main:
                self.main.target.draw(x, y)
                x -= self.main.frameSizeX/2
                y -= self.main.frameSizeY/2
                y *= -1
                print 'X_r:', x
                print 'Y_r:', y
                pan  = x / float(self.main.frameSizeX) * self.main.cameraPan
                tilt = y / float(self.main.frameSizeY) * self.main.cameraTilt
                print 'Pan :', pan
                print 'Tilt:', tilt
                self.main.pointer.move('AzEl', pan, tilt)

class Crosshair():
    """ A simple crosshair class """
    def __init__(self, graphicsScene, color=Qt.red, z=1):
        self.r=8 # crosshair radius [pixels]
        self.c=2 # cross excess length [pixels]
        self.z = z       
        self.gs = graphicsScene
        self.x = 0
        self.y = 0
        self.pen = QPen()
        self.pen.setColor(color)
                
        self.ellipse=None
        self.line1=None
        self.line2=None
  
    def stack(self, z):
        self.z = z

    def botton(self):
        self.z = 0
    
    def top(self):
        self.z=1

    def draw(self, x=None, y=None):

	print "x: " + str(x) + ", y: " + str(y)	

        if x != None:
            self.x = x-self.r
        if y != None:
            self.y = y-self.r

        if self.ellipse:
            self.gs.removeItem(self.ellipse)
            self.gs.removeItem(self.line1)
            self.gs.removeItem(self.line2)
        r=self.r
        c=self.c
        x=self.x
        y=self.y
        self.ellipse=self.gs.addEllipse(x, y, r*2, r*2, self.pen)
        self.line1=self.gs.addLine(QLineF(x-c, y+r, x+2*r+c, y+r), self.pen)
        self.line2=self.gs.addLine(QLineF(x+r, y-c, x+r, y+2*r+c), self.pen)      
        self.ellipse.setZValue(self.z)
        self.line1.setZValue(self.z)
        self.line2.setZValue(self.z)
    
class MainWindow(QMainWindow, gui):
    
    # Pointer GUI
    POINTERGUIVERSION = "0.0.5"

    def __init__(self, parent=None):

        QMainWindow.__init__(self)
        self.setupUi(self)

#        self.setWindowIcon(QIcon(QPixmap(":/icons/icons/pointer.png")))
        
        # Pointer client instance
        self.pointer = pointer_cli.Pointer_CLI()._getPointer(pointer_server)

        # Video capture
        fps=25
        captureTime = 1./fps*1000. # [ms]
        
        dataTime = 5000. # [ms]

        """
            Video capture address
        """
        # Webcam
#        videoStream = 0
        # Raspberry pi camera
#        videoStream = 'picamera'
        # Rtsp
#        videoStream = 'rtsp://' + camera_server + ':8554/'
        # Gstreamer0.10
#        videoStream = 'tcpclientsrc host=' + camera_server + ' port=5000 ! gdpdepay ! rtph264depay ! ffdec_h264 ! ffmpegcolorspace ! appsink sync=false'
        # Gstreamer1.0
        videoStream = 'tcpclientsrc host=' + camera_server + ' port=5000 ! gdpdepay ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink sync=false' # ffmpegcolorspace ! 
#        videoStream = 'tcpclientsrc host=' + camera_server + ' port=5000 ! h264parse ! avdec_h264 ! videoconvert ! appsink sync=false' # ffmpegcolorspace !
        
        if videoStream == 0: # Webcam, default resolution
            self.cameraPan = 46.5 # [°]
            self.cameraTilt= 22.5 # [°]
        elif videoStream == 'picamera':
            self.cameraPan = 46.5 # [°]
            self.cameraTilt= 22.5 # [°]
            self.frameSizeX= 1080 # [px]
            self.frameSizeY= 720 # [px]
        else: # rtsp/rtp (assumes server with picamera, server set resolution)
            self.cameraPan = 46.5 # [°]
            self.cameraTilt= 22.5 # [°]
            self.frameSizeX= 1080 # [px]
            self.frameSizeY= 720 # [px]

        # Open the video stream
        self.video = GuiVideo(videoStream, (self.frameSizeX, self.frameSizeY))

        # Graphics scene
        self.graphicsScene = QGraphicsScene()
        self.videoFrame = QPixmap()
        self.pixmapItem = GraphicsPixmapItem(main=self)
        
        self.graphicsScene.addItem(self.pixmapItem)
              
        self.graphicsView.setScene(self.graphicsScene)
        
        self.crosshair = Crosshair(self.graphicsScene)   
        
        self.target = Crosshair(self.graphicsScene, Qt.green)
        self.target.stack(0.9)
        
        # Scale factor
        self.scaleFactor = 1.25;
        
        # Create timers
        self.first = True
        self.captureTimer = QTimer()
        
        self.dataTimer = QTimer()

        # Connects
        self.connect(self.pushButtonUp, SIGNAL("pressed()"), self.OnPushButtonUpPressed)
        self.connect(self.pushButtonDown, SIGNAL("pressed()"), self.OnPushButtonDownPressed)
        self.connect(self.pushButtonRight, SIGNAL("pressed()"), self.OnPushButtonRightPressed)
        self.connect(self.pushButtonLeft, SIGNAL("pressed()"), self.OnPushButtonLeftPressed)
        self.connect(self.pushButtonAbort, SIGNAL("pressed()"), self.OnPushButtonAbortPressed)
        self.connect(self.pushButtonZoomIn, SIGNAL("pressed()"), self.OnPushButtonZoomInPressed)
        self.connect(self.pushButtonZoomOut, SIGNAL("pressed()"), self.OnPushButtonZoomOutPressed)
        
        self.connect(self.captureTimer, SIGNAL("timeout()"), self.OnCaptureTimeout)
        self.connect(self.dataTimer, SIGNAL("timeout()"), self.OnDataTimeout)
        
#        self.connect(self.graphicsScene, SIGNAL("changed()"), self.OnSceneChanged)

        # Start timers
        self.captureTimer.start(captureTime)
        
#        self.dataTimer.start(dataTime)
        
#        desktop = QApplication.desktop();
#        self.screen_width = desktop.width();
#        self.screen_height = desktop.height();
        
#        self.events_mutex = QMutex()

        self.graphicsView.show()
        self.update()

    def OnPushButtonUpPressed(self):
        steps = float(self.lineEditSteps.text())
        if self.radioButtonArcmins.isChecked():
            steps /= 60.
        elif self.radioButtonArcsecs.isChecked():
            steps /= 3600.
        if self.radioButtonSteps.isChecked():
            self.pointer.move('X', steps, 0)
        else:
            self.pointer.move('AzEl', 0, steps)

    def OnPushButtonDownPressed(self):
        steps = float(self.lineEditSteps.text())
        if self.radioButtonArcmins.isChecked():
            steps /= 60.
        elif self.radioButtonArcsecs.isChecked():
            steps /= 3600.
        if self.radioButtonSteps.isChecked():
            self.pointer.move('X', -steps, 0)
        else:
            self.pointer.move('AzEl', 0, -steps)

    def OnPushButtonRightPressed(self):
        steps = float(self.lineEditSteps.text())
        if self.radioButtonArcmins.isChecked():
            steps /= 60.
        elif self.radioButtonArcsecs.isChecked():
            steps /= 3600.
        if self.radioButtonSteps.isChecked():
            self.pointer.move('Z', steps, 0)
        else:
            self.pointer.move('AzEl', steps, 0)

    def OnPushButtonLeftPressed(self):
        steps = float(self.lineEditSteps.text())
        if self.radioButtonArcmins.isChecked():
            steps /= 60.
        elif self.radioButtonArcsecs.isChecked():
            steps /= 3600.
        if self.radioButtonSteps.isChecked():
            self.pointer.move('Z', -steps, 0)
        else:
            self.pointer.move('AzEl', -steps, 0)
            
    def OnPushButtonAbortPressed(self):
        self.pointer.abort()

    def OnPushButtonZoomInPressed(self):
        self.graphicsView.scale(self.scaleFactor, self.scaleFactor)

    def OnPushButtonZoomOutPressed(self):
        self.graphicsView.scale(1./self.scaleFactor, 1./self.scaleFactor)
                
    def OnCaptureTimeout(self):
        try:
            self.video.captureNextFrame()
            self.videoFrame = self.video.convertFrame()
            self.frameSizeX = self.videoFrame.width()
            self.frameSizeY = self.videoFrame.height()
#            print 'frame size X:', self.frameSizeX
#            print 'frame size Y:', self.frameSizeY
            self.graphicsScene.setSceneRect(QRectF(0, 0, self.frameSizeX, self.frameSizeY))
            self.pixmapItem.setPixmap(self.videoFrame)

	    # Red crosshair, set position
            if self.first:
                x = 366.25 # self.graphicsScene.width() / 2
                y = 262.5 # self.graphicsScene.height() / 2
                self.crosshair.draw(x, y)
                self.first = False
        except Exception as e:
            print >>sys.stderr, "Exception: OnCaptureTimeout():", e
            
    def OnDataTimeout(self):
        try:
            v1, v2 = self.pointer.get('AzEl')
            self.lineEditAz.setText(u'%.4f°' % v1)
            self.lineEditEl.setText(u'%.4f°' % v2)
            v1, v2 = self.pointer.get('RAdec')
            h = int(v1)
            m = int((v1 - h)*60.)
            s = (v1 - h - m / 60.)*3600.
            self.lineEditRA.setText(u'%02d:%02d:%05.2f' % (h, m, s))
            self.lineEditDec.setText(u'%.4f°' % v2)
        except Exception as e:
            print >>sys.stderr, "Exception: OnDataTimeout():", e

    
if __name__ == "__main__":
    QApplication.setApplicationName("POINTERGUI-COLIMACION");
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
#    window.MoveWindowToMiddle(window)
    sys.exit(app.exec_())
