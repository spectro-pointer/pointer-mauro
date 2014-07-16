#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4.Qt

from mainwindow import Ui_MainWindow as gui
#import gc

import cv2
import numpy as np
import pointer_cli_27 as pointer_cli

# Picamera stuff
import io
try:
    import picamera
except:
    print >>sys.stderr, "Warning: picamera module not found"
    pass

# Pointer server hostname/IP
pointer_server = 'pi'
# Camera server hostname/IP
camera_server = pointer_server

class Video():
    """
        Video class
            - Webcam/Picamera/Video stream abstraction
            - QtGui output format support
    """
    def __init__(self, stream, res=None):
        self.piCamera=False
        if stream == 'picamera':
            self.capture = picamera.PiCamera()
            if res:
                self.capture.resolution = res
            self.capture.hflip = True
            self.capture.vflip = True
            self.piCamera = True
        else:
            self.capture = cv2.VideoCapture()
            if not self.capture.open(stream):
                print >>sys.stderr, "Error: video stream or device open failed"
                sys.exit(-1);
        self.currentFrame=np.array([])

    def captureNextFrame(self):
        """ 
            Capture frame, reverse RBG BGR, and return opencv image                                                                         
        """
        ret = False
        readFrame = None
        if self.piCamera:
            ret, readFrame=self.readPicamera()
        else:
            ret, readFrame=self.capture.read()
        if(ret):
            self.currentFrame=cv2.cvtColor(readFrame, cv2.COLOR_BGR2RGB)
        else:
            print >>sys.stderr, 'Warning: no frame'
            
    def readPicamera(self):
        """ 
            Read a single frame from the camera and return the data as an OpenCV
            image (which is a numpy array).
        """
        # This code is based on the picamera example at:
        # http://picamera.readthedocs.org/en/release-1.0/recipes1.html#capturing-to-an-opencv-object
        # Capture a frame from the camera.
        data = io.BytesIO()
        try:
            self.capture.capture(data, format='jpeg', use_video_port=True)
        except Exception as e:
            print >>sys.stderr, 'Exception: readPiCamera():', e
            return False, None
        data = np.fromstring(data.getvalue(), dtype = np.uint8)
        # Decode the image data and return an OpenCV image.
        readFrame = cv2.imdecode(data, 1)
        return True, readFrame

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
        
        if videoStream == 0: # Webcam, default resolution
            self.cameraPan = 30. # [°]
            self.cameraTilt= 20. # [°]
        elif videoStream == 'picamera':
            self.cameraPan = 40.5 # [°]
            self.cameraTilt= 22.5 # [°]
            self.frameSizeX= 1080 # [px]
            self.frameSizeY= 720 # [px]
        else: # rtsp/rtp (assumes server with picamera, server set resolution)
            self.cameraPan = 40.5 # [°]
            self.cameraTilt= 22.5 # [°]

        # Open the video stream
        self.video = Video(videoStream, (self.frameSizeX, self.frameSizeY))

        # Graphics scene
        self.graphicsScene = QGraphicsScene()
        self.videoFrame = QPixmap()
        self.pixmapItem = GraphicsPixmapItem(main=self)
        
        self.graphicsScene.addItem(self.pixmapItem)
              
        self.graphicsView.setScene(self.graphicsScene)
        
        self.crosshair = Crosshair(self.graphicsScene)   
        
        self.target = Crosshair(self.graphicsScene, Qt.green)
        self.target.stack(0.9)
        
        # Create timers
        self.first = True
        self.captureTimer = QTimer()

        # Connects
        self.connect(self.pushButtonUp, SIGNAL("pressed()"), self.OnPushButtonUpPressed)
        self.connect(self.pushButtonDown, SIGNAL("pressed()"), self.OnPushButtonDownPressed)
        self.connect(self.pushButtonRight, SIGNAL("pressed()"), self.OnPushButtonRightPressed)
        self.connect(self.pushButtonLeft, SIGNAL("pressed()"), self.OnPushButtonLeftPressed)
        self.connect(self.pushButtonAbort, SIGNAL("pressed()"), self.OnPushButtonAbortPressed)
        
        self.connect(self.captureTimer, SIGNAL("timeout()"), self.OnCaptureTimeout)
        
#        self.connect(self.graphicsScene, SIGNAL("changed()"), self.OnSceneChanged)

        # Start timers
        self.captureTimer.start(captureTime)
        
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
            self.pointer.move('X', steps)
        else:
            self.pointer.move('AzEl', 0, steps)

    def OnPushButtonDownPressed(self):
        steps = float(self.lineEditSteps.text())
        if self.radioButtonArcmins.isChecked():
            steps /= 60.
        elif self.radioButtonArcsecs.isChecked():
            steps /= 3600.
        if self.radioButtonSteps.isChecked():
            self.pointer.move('X', -steps)
        else:
            self.pointer.move('AzEl', 0, -steps)

    def OnPushButtonRightPressed(self):
        steps = float(self.lineEditSteps.text())
        if self.radioButtonArcmins.isChecked():
            steps /= 60.
        elif self.radioButtonArcsecs.isChecked():
            steps /= 3600.
        if self.radioButtonSteps.isChecked():
            self.pointer.move('Z', steps)
        else:
            self.pointer.move('AzEl', steps, 0)

    def OnPushButtonLeftPressed(self):
        steps = float(self.lineEditSteps.text())
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
            if self.first:
                x = self.graphicsScene.width() / 2
                y = self.graphicsScene.height() / 2
                self.crosshair.draw(x, y)
                self.first = False
        except Exception as e:
            print >>sys.stderr, "Exception: OnCaptureTimeout():", e
    
if __name__ == "__main__":
    QApplication.setApplicationName("POINTERGUI");
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
#    window.MoveWindowToMiddle(window)
    sys.exit(app.exec_())
