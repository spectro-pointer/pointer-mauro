#!/usr/bin/python
# -*- coding: cp1252 -*-

import cv2
from cv2 import cv
import os
import wx
import mywidgets as mywdg

#====================================================================================================================================
# Variables Globales
APP_SIZE_X=800          # Tamaño horizontal de la ventana de la aplicacion [px]
APP_SIZE_Y=680          # Tamaño vertical de la ventana de la aplicacion [px]
FRAME_SIZE_X=640        # Tamaño horizontal del frame de imagen en la aplicacion [px]
FRAME_SIZE_Y=480        # Tamaño vertical del frame de imagen en la aplicacion [px]
CMD_SIZE_X=APP_SIZE_X   # Tamño horizontal del panel inferior de comandos [px]
CMD_SIZE_Y=120          # Tamaño vertical del panel inferior de comandos [px]
CAM_DEG_PAN=30          # Amplitud horizontal de la camara en el frame de imagen [°]
CAM_DEG_TILT=20         # Amplitud vertical de la camara en el frame de imagen [°]
MAX_DEG_PAN=90          # Maxima amplitud absoluta de desplazamiento PAN [°]
MIN_DEG_PAN=-90         # Minima amplitud absoluta de desplazamiento PAN [°]
MAX_DEG_TILT=45         # Maxima amplitud absoluta de desplazamiento TILT [°]
MIN_DEG_TILT=-45        # Minima amplitud absoluta de desplazamiento TILT [°]

#====================================================================================================================================
# Clase donde almaceno los datos del sistema
class dataBase:
    coords={'pan':0.0, 'tilt':0.0}
    pointer={'pan':0.0, 'tilt':0.0}

    def setValue(self, index, value):
        self.coords[index]=value

    def getValue(self, index):
        return self.coords[index]

    def setPointer(self, index, value):
        self.pointer[index]=value

    def getPointer(self, index):
        return self.pointer[index]

#====================================================================================================================================
# Ventana Principal
class MainWindow(wx.Frame):
    def __init__(self, parent, title, ancho, alto, capture, base):
        wx.Frame.__init__(self, parent, title=title, size=(ancho, alto), style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

        self.capture = capture
        # Configuraciones de la ventana principal
        # Icono de barra de titulo
        ico = wx.Icon("camara.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        # StatusBar
        self.CreateStatusBar()
        # Paneles para layout
        self.panel = wx.Panel(self)

        mywdg.servoCmd(self.panel, (APP_SIZE_X/2+FRAME_SIZE_X/2+10, (FRAME_SIZE_Y-300)/2), (50, 300), base, 'tilt', (MIN_DEG_TILT, MAX_DEG_TILT), "VER")

        # ************** Menues
        # Archivo
        filemenu = wx.Menu()
        menuExit = wx.MenuItem(filemenu, wx.ID_EXIT, "&Salir")
        start_image = wx.Image("salir.png") 
        start_image.Rescale(15, 15) 
        image = wx.BitmapFromImage(start_image)
        menuExit.SetBitmap(image)
        filemenu.AppendItem(menuExit)
        
        # Ayuda
        aboutmenu = wx.Menu();
        menuAbout = wx.MenuItem(aboutmenu, wx.ID_ABOUT, "A&cerca de")
        start_image = wx.Image("about.png") 
        start_image.Rescale(15, 15) 
        image = wx.BitmapFromImage(start_image)
        menuAbout.SetBitmap(image)
        aboutmenu.AppendItem(menuAbout)

        # Creo la barra del menu
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&Archivo") # Agrego el "filemenu"
        menuBar.Append(aboutmenu, "A&yuda")  # Agrego el "aboutmenu"
        self.SetMenuBar(menuBar)             # Agrego la barra a la ventana

        # Configuro eventos
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        #self.Centre()
        
    def OnAbout(self, e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, "Aplicación para operación de Espectroscopio", "Acerca de", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy()   # finally destroy it when finished.

    def OnExit(self, e):
        self.capture.release()
        self.Destroy()
        self.Close(True)  # Close the frame.

#====================================================================================================================================
# Panel para la imagen de la camara
class showCapture(wx.Panel):
    def __init__(self, parent, capture, base, pointer, fps=20):
        wx.Panel.__init__(self, parent.panel, pos=((APP_SIZE_X-FRAME_SIZE_X)/2, 0), size=(FRAME_SIZE_X, FRAME_SIZE_Y))

        self.capture = capture
        self.base=base
        
        self.pointer=pointer
        
        ret, frame = self.capture.read()
        height, width = frame.shape[:2]
        self.SetSize((width, height))
        self.ancho = width
        self.alto = height
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        self.bmp = wx.BitmapFromBufferRGBA(width, height, frame)

        self.timer = wx.Timer(self)
        self.timer.Start(10000./fps)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)
        self.Bind(wx.EVT_LEFT_UP, self.onClick)

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)
        self.SetSize((self.ancho, self.alto))

    def NextFrame(self, event):
        ret, frame = self.capture.read()
        # Centro de Pantalla
        cv2.circle(frame, (self.ancho/2, self.alto/2), 7, (0, 255, 0, 0.6))
        cv2.line(frame, (self.ancho/2, (self.alto/2)-10), (self.ancho/2, (self.alto/2)+10), (0, 255, 0, 0.6))
        cv2.line(frame, ((self.ancho/2)-10, self.alto/2), ((self.ancho/2)+10, self.alto/2), (0, 255, 0, 0.6))
        # Target de camara
        x = int(self.base.getPointer('pan')*(float(FRAME_SIZE_X)/2)/(float(CAM_DEG_PAN)/2)+FRAME_SIZE_X/2)
        y = int(-1*self.base.getPointer('tilt')*(float(FRAME_SIZE_Y)/2)/(float(CAM_DEG_TILT)/2)+FRAME_SIZE_Y/2)
        
        cv2.circle(frame, (x, y), 7, (0, 0, 255))
        cv2.line(frame, (x, y-10), (x, y+10), (0, 0, 255))
        cv2.line(frame, (x-10, y), (x+10, y), (0, 0, 255))
        
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            self.bmp.CopyFromBufferRGBA(frame)
            self.Refresh()
            
    def onClick(self, e):
        coord = self.ScreenToClient(wx.GetMousePosition())
        
        # Proceso las coordenadas del contenedor del frame para convertirlas en posicion pan-tilt
        # Las traslado relativas al centro del frame (pan=0, tilt=0)
        coord_x = coord[0]-FRAME_SIZE_X/2
        coord_y = -(coord[1]-FRAME_SIZE_Y/2)
        # Busco el porcentaje de angulo que debe desplazarse
        pos_pan = float((float(coord_x)/(float(FRAME_SIZE_X)/2.))*(float(CAM_DEG_PAN)/2.))
        pos_tilt = float((float(coord_y)/(float(FRAME_SIZE_Y)/2.))*(float(CAM_DEG_TILT)/2.))
        print "Movimiento Relativo (PAN TILT): ", pos_pan, pos_tilt
        
        # Seteo coordenadas a puntero
        self.pointer.move('AzEl', pos_pan, pos_tilt)

        self.base.setPointer('pan', pos_pan)
        self.base.setPointer('tilt', pos_tilt)
        
        # Seteo en la base
        pos_pan+=self.base.getValue('pan')
        if(pos_pan>MAX_DEG_PAN):pos_pan=MAX_DEG_PAN
        if(pos_pan>MIN_DEG_PAN):pos_pan=MIN_DEG_PAN
        pos_tilt+=self.base.getValue('tilt')
        if(pos_tilt>MAX_DEG_TILT):pos_tilt=MAX_DEG_TILT
        if(pos_tilt<MIN_DEG_TILT):pos_tilt=MIN_DEG_TILT
        
        self.base.setValue('pan', pos_pan)
        self.base.setValue('tilt', pos_tilt)        

#====================================================================================================================================
# Panel para los controles
class showCommands(wx.Panel):
    def __init__(self, parent, base):
        wx.Panel.__init__(self, parent.panel, pos=((APP_SIZE_X-CMD_SIZE_X)/2, FRAME_SIZE_Y+5), size=(CMD_SIZE_X, CMD_SIZE_Y))

        self.initUI()
                
    def initUI(self):
        self.SetBackgroundColour('#E0E0E0')
        mywdg.servoCmd(self, ((APP_SIZE_X-300)/2, 0), (300, 50), base, 'pan', (MIN_DEG_PAN, MAX_DEG_PAN), "HOR")
        

#====================================================================================================================================
# "main"
import pointer_cli_27 as pointer_cli

# Tomo imagen de la webcam
capture = cv2.VideoCapture(0)

# Tomo instancia a una estructura de datos de la base y la inicializo
base = dataBase()

# Pointer server hostname
server_host = 'localhost'

# Pointer client instance
pointer = pointer_cli.Pointer_CLI()._getPointer(server_host)

# Inicio
app = wx.App(False)
mainwin = MainWindow(None, "Operacion de Espectroscopio - IFA", APP_SIZE_X, APP_SIZE_Y, capture, base)
camara = showCapture(mainwin, capture, base, pointer)
botones = showCommands(mainwin, base)
mainwin.Show()
app.MainLoop()

