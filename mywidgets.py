import wx

#====================================================================================================================================
# Definiciones
BUT_SIZE_X=20
BORDER=10
MIN_VALUE=0
MAX_VALUE=1

#====================================================================================================================================
# Panel para control de una variable
class servoCmd(wx.Panel):
    def __init__(self, parent, wdg_pos, wdg_size, base, index, limites, orientation):
        wx.Panel.__init__(self, parent, pos=wdg_pos, size=wdg_size)

        # Inicializo
        self.tam=wdg_size
        self.coord=base.getValue(index)
        self.base=base
        self.index=index
        self.limits=limites
        self.initUI(orientation)
        
    def initUI(self, orientation):
        self.SetBackgroundColour('#A0A0A0')

        if(orientation=="HOR"):
            slider_size=self.tam[0]-2*BUT_SIZE_X-10

            btn1 = wx.Button(self, label='-', size=(BUT_SIZE_X, self.tam[1]))
            self.sld = wx.Slider(self, -1, value=0, minValue=self.limits[MIN_VALUE], maxValue=self.limits[MAX_VALUE],
                                 style=wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS,
                                 size=(slider_size, -1), pos=(BUT_SIZE_X+BORDER/2, -1))
            btn2 = wx.Button(self, label='+', size=(BUT_SIZE_X, self.tam[1]), pos=(slider_size+BUT_SIZE_X+BORDER, -1))
        else:
            slider_size=self.tam[1]-2*BUT_SIZE_X-10
            btn1 = wx.Button(self, label='+', size=(self.tam[0], BUT_SIZE_X))
            self.sld = wx.Slider(self, -1, value=0, minValue=self.limits[MIN_VALUE], maxValue=self.limits[MAX_VALUE],
                                 style=wx.SL_AUTOTICKS | wx.SL_VERTICAL | wx.SL_LABELS,
                                 size=(-1, slider_size), pos=(-1, BUT_SIZE_X+BORDER/2))
            btn2 = wx.Button(self, label='-', size=(self.tam[0], BUT_SIZE_X), pos=(0, slider_size+BUT_SIZE_X+BORDER))

        self.sld.SetTickFreq(5, 1)
        # Callbacks
        self.sld.Bind(wx.EVT_SCROLL_CHANGED, self.onSlider) 
        btn1.Bind(wx.EVT_BUTTON, self.onClick)
        btn2.Bind(wx.EVT_BUTTON, self.onClick)

    def onClick(self, e):
        btn = e.GetEventObject()
        label = btn.GetLabelText()
        if(label=="-"):
            self.coord-=1
            if(self.coord<self.limits[MIN_VALUE]):self.coord=self.limits[MIN_VALUE]
            self.sld.SetValue(self.coord)
            self.base.setValue(self.index, self.coord)
        elif(label=="+"):
            self.coord+=1
            if(self.coord>self.limits[MAX_VALUE]):self.coord=self.limits[MAX_VALUE]
            self.sld.SetValue(self.coord)
            self.base.setValue(self.index, self.coord)

    def onSlider(self, e):
        self.coord=self.sld.GetValue()
        self.base.setValue(self.index, self.coord)
        print self.base.getValue(self.index)
