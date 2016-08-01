from __future__ import print_function
from imp import load_source
from os.path import join, dirname
from sys import platform, argv
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
try:
    range = xrange
except NameError:
    pass

COLORS = ["000083", "000087", "00008B", "00008F", "000093", "000097", "00009B",
    "00009F", "0000A3", "0000A7", "0000AB", "0000AF", "0000B3", "0000B7",
    "0000BB", "0000BF", "0000C3", "0000C7", "0000CB", "0000CF", "0000D3",
    "0000D7", "0000DB", "0000DF", "0000E3", "0000E7", "0000EB", "0000EF",
    "0000F3", "0000F7", "0000FB", "0000FF", "0003FF", "0007FF", "000BFF",
    "000FFF", "0013FF", "0017FF", "001BFF", "001FFF", "0023FF", "0027FF",
    "002BFF", "002FFF", "0033FF", "0037FF", "003BFF", "003FFF", "0043FF",
    "0047FF", "004BFF", "004FFF", "0053FF", "0057FF", "005BFF", "005FFF",
    "0063FF", "0067FF", "006BFF", "006FFF", "0073FF", "0077FF", "007BFF",
    "007FFF", "0083FF", "0087FF", "008BFF", "008FFF", "0093FF", "0097FF",
    "009BFF", "009FFF", "00A3FF", "00A7FF", "00ABFF", "00AFFF", "00B3FF",
    "00B7FF", "00BBFF", "00BFFF", "00C3FF", "00C7FF", "00CBFF", "00CFFF",
    "00D3FF", "00D7FF", "00DBFF", "00DFFF", "00E3FF", "00E7FF", "00EBFF",
    "00EFFF", "00F3FF", "00F7FF", "00FBFF", "00FFFF", "03FFFB", "07FFF7",
    "0BFFF3", "0FFFEF", "13FFEB", "17FFE7", "1BFFE3", "1FFFDF", "23FFDB",
    "27FFD7", "2BFFD3", "2FFFCF", "33FFCB", "37FFC7", "3BFFC3", "3FFFBF",
    "43FFBB", "47FFB7", "4BFFB3", "4FFFAF", "53FFAB", "57FFA7", "5BFFA3",
    "5FFF9F", "63FF9B", "67FF97", "6BFF93", "6FFF8F", "73FF8B", "77FF87",
    "7BFF83", "7FFF7F", "83FF7B", "87FF77", "8BFF73", "8FFF6F", "93FF6B",
    "97FF67", "9BFF63", "9FFF5F", "A3FF5B", "A7FF57", "ABFF53", "AFFF4F",
    "B3FF4B", "B7FF47", "BBFF43", "BFFF3F", "C3FF3B", "C7FF37", "CBFF33",
    "CFFF2F", "D3FF2B", "D7FF27", "DBFF23", "DFFF1F", "E3FF1B", "E7FF17",
    "EBFF13", "EFFF0F", "F3FF0B", "F7FF07", "FBFF03", "FFFF00", "FFFB00",
    "FFF700", "FFF300", "FFEF00", "FFEB00", "FFE700", "FFE300", "FFDF00",
    "FFDB00", "FFD700", "FFD300", "FFCF00", "FFCB00", "FFC700", "FFC300",
    "FFBF00", "FFBB00", "FFB700", "FFB300", "FFAF00", "FFAB00", "FFA700",
    "FFA300", "FF9F00", "FF9B00", "FF9700", "FF9300", "FF8F00", "FF8B00",
    "FF8700", "FF8300", "FF7F00", "FF7B00", "FF7700", "FF7300", "FF6F00",
    "FF6B00", "FF6700", "FF6300", "FF5F00", "FF5B00", "FF5700", "FF5300",
    "FF4F00", "FF4B00", "FF4700", "FF4300", "FF3F00", "FF3B00", "FF3700",
    "FF3300", "FF2F00", "FF2B00", "FF2700", "FF2300", "FF1F00", "FF1B00",
    "FF1700", "FF1300", "FF0F00", "FF0B00", "FF0700", "FF0300", "FF0000",
    "FB0000", "F70000", "F30000", "EF0000", "EB0000", "E70000", "E30000",
    "DF0000", "DB0000", "D70000", "D30000", "CF0000", "CB0000", "C70000",
    "C30000", "BF0000", "BB0000", "B70000", "B30000", "AF0000", "AB0000",
    "A70000", "A30000", "9F0000", "9B0000", "970000", "930000", "8F0000",
    "8B0000", "870000", "830000", "7F0000"]
APP_X, APP_Y = 50, 50
CANVAS_WIDTH, CANVAS_HEIGHT = 500, 500
RMIN_CONFIG = ('rMin', 1, 1000, 10.0)
RMAX_CONFIG = ('rMax', 1, 1000, 100.0)
RRES_CONFIG = ('rRes', 0.1, 10, 2.0)
TMIN_CONFIG = ('thetaMin', -90, 90, -20.0)
TMAX_CONFIG = ('thetaMax', -90, 90, 20.0)
TRES_CONFIG = ('thetaRes', 0.1, 10, 10.0)
PMIN_CONFIG = ('phiMin', -90, 90, -45.0)
PMAX_CONFIG = ('phiMax', -90, 90, 45.0)
PRES_CONFIG = ('phiRes', 0.1, 10, 2.0)
THLD_CONFIG = ('threshold', 0.1, 100, 15.0)

class MainGUI(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configGUI = ConfigGUI(self)
        self.controlGUI = ControlGUI(self)
        self.canvasGUI = CanvasGUI(self)
        self.configGUI.grid(row=0, column=0, sticky=tk.N)
        self.controlGUI.grid(row=1, column=0, sticky=(tk.EW, tk.S))
        self.canvasGUI.grid(row=0, column=1, rowspan=2)
        self.wlbt = Walabot(self)
    def startWlbt(self):
        if self.wlbt.isConnected():
            self.controlGUI.statusVar.set('STATUS_CONNECTED')
            self.update_idletasks()
            params = self.configGUI.getParams()
            self.wlbt.setParams(*params)
            self.configGUI.setParams(*self.wlbt.getArenaParams())
            if not params[4]: # equals: if not mtiMode
                self.controlGUI.statusVar.set('STATUS_CALIBRATING')
                self.update_idletasks()
                self.wlbt.calibrate()
            self.lenOfPhi, self.lenOfR = self.wlbt.getRawImageSliceDimensions()
            self.canvasGUI.setGrid(self.lenOfPhi, self.lenOfR)
            self.configGUI.changeEntriesState('disabled')
            self.startCycles()
        else:
            self.controlGUI.statusVar.set('STATUS_DISCONNECTED')
    def startCycles(self):
        self.controlGUI.statusVar.set('STATUS_SCANNING')
        rawImage = self.wlbt.triggerAndGetRawImageSlice()
        self.canvasGUI.update(rawImage, self.lenOfPhi, self.lenOfR)
        self.controlGUI.fpsVar.set(self.wlbt.getFps())
        self.cyclesId = self.after_idle(self.startCycles)

class ConfigGUI(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text='Walabot Configuration')
        self.rMin = ParameterGUI(self, *RMIN_CONFIG)
        self.rMax = ParameterGUI(self, *RMAX_CONFIG)
        self.rRes = ParameterGUI(self, *RRES_CONFIG)
        self.tMin = ParameterGUI(self, *TMIN_CONFIG)
        self.tMax = ParameterGUI(self, *TMAX_CONFIG)
        self.tRes = ParameterGUI(self, *TRES_CONFIG)
        self.pMin = ParameterGUI(self, *PMIN_CONFIG)
        self.pMax = ParameterGUI(self, *PMAX_CONFIG)
        self.pRes = ParameterGUI(self, *PRES_CONFIG)
        self.thld = ParameterGUI(self, *THLD_CONFIG)
        self.mti = MtiGUI(self)
        self.rMin.grid(row=0, sticky=tk.W)
        self.rMax.grid(row=1, sticky=tk.W)
        self.rRes.grid(row=2, sticky=tk.W)
        self.tMin.grid(row=3, sticky=tk.W)
        self.tMax.grid(row=4, sticky=tk.W)
        self.tRes.grid(row=5, sticky=tk.W)
        self.pMin.grid(row=6, sticky=tk.W)
        self.pMax.grid(row=7, sticky=tk.W)
        self.pRes.grid(row=8, sticky=tk.W)
        self.thld.grid(row=9, sticky=tk.W)
        self.mti.grid(row=10, sticky=tk.W)
    def getParams(self):
        rParams = (self.rMin.get(), self.rMax.get(), self.rRes.get())
        tParams = (self.tMin.get(), self.tMax.get(), self.tRes.get())
        pParams = (self.pMin.get(), self.pMax.get(), self.pRes.get())
        thldParam, mtiParam = self.thld.get(), self.mti.get()
        return rParams, tParams, pParams, thldParam, mtiParam
    def setParams(self, rParams, thetaParams, phiParams, threshold):
        self.rMin.set(rParams[0])
        self.rMax.set(rParams[1])
        self.rRes.set(rParams[2])
        self.tMin.set(thetaParams[0])
        self.tMax.set(thetaParams[1])
        self.tRes.set(thetaParams[2])
        self.pMin.set(phiParams[0])
        self.pMax.set(phiParams[1])
        self.pRes.set(phiParams[2])
        self.thld.set(threshold)
    def changeEntriesState(self, state):
        self.rMin.changeEntryState(state)
        self.rMax.changeEntryState(state)
        self.rRes.changeEntryState(state)
        self.tMin.changeEntryState(state)
        self.tMax.changeEntryState(state)
        self.tRes.changeEntryState(state)
        self.pMin.changeEntryState(state)
        self.pMax.changeEntryState(state)
        self.pRes.changeEntryState(state)
        self.thld.changeEntryState(state)

class ParameterGUI(tk.Frame):
    def __init__(self, master, varValue, minValue, maxValue, defaultValue):
        tk.Frame.__init__(self, master)
        tk.Label(self, text=varValue+' = ').pack(side=tk.LEFT)
        self.minValue, self.maxValue = minValue, maxValue
        self.var = tk.StringVar()
        self.var.set(defaultValue)
        self.entry = tk.Entry(self, width=6, textvariable=self.var)
        self.entry.pack(side=tk.LEFT)
        self.var.trace('w', lambda a, b, c, var=self.var:
            self.validate())
        tk.Label(self, text=' value between '+str(minValue)).pack(side=tk.LEFT)
        tk.Label(self, text='and '+str(maxValue)).pack(side=tk.LEFT)
    def validate(self):
        num = self.var.get()
        try:
            num = float(num)
            if num < self.minValue or num > self.maxValue:
                self.entry.config(fg='#'+COLORS[235]); return
            self.entry.config(fg='gray1')
        except ValueError:
            self.entry.config(fg='#'+COLORS[235]); return
    def get(self):
        return self.var.get()
    def set(self, value):
        self.var.set(value)
    def changeEntryState(self, state):
        """ Change the state of 'entry' according to the given state.
            Arguments:
                state       most be either 'normal' or 'disabled'
        """
        self.entry.configure(state=state)

class MtiGUI(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text='mti = ').pack(side=tk.LEFT)
        self.mtiVar = tk.BooleanVar()
        self.mtiVar.set(0)
        tk.Radiobutton(self, text='True', variable=self.mtiVar,
            value=1).pack(side=tk.LEFT)
        tk.Radiobutton(self, text='False', variable=self.mtiVar,
            value=0).pack(side=tk.LEFT)
    def get(self):
        return self.mtiVar.get()
    def set(self, value):
        self.mtiVar.set(value)

class ControlGUI(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text='Control Panel')
        self.buttonsFrame = tk.Frame(self)
        self.runButton, self.stopButton = self.setButtons(self.buttonsFrame)
        self.statusFrame = tk.Frame(self)
        self.statusVar = self.setVar(self.statusFrame, 'APP_STATUS', '')
        self.errorFrame = tk.Frame(self)
        self.errorVar = self.setVar(self.errorFrame, 'EXCEPTION', '')
        self.fpsFrame = tk.Frame(self)
        self.fpsVar = self.setVar(self.fpsFrame, 'FRAME_RATE', 'N/A')
        self.buttonsFrame.grid(row=0, column=0, sticky=tk.W)
        self.statusFrame.grid(row=1, columnspan=2, sticky=tk.W)
        self.errorFrame.grid(row=2, columnspan=2, sticky=tk.W)
        self.fpsFrame.grid(row=3, columnspan=2, sticky=tk.W)
    def setButtons(self, frame):
        runButton = tk.Button(frame, text='Start', command=self.start)
        stopButton = tk.Button(frame, text='Stop', command=self.stop)
        runButton.grid(row=0, column=0)
        stopButton.grid(row=0, column=1)
        return runButton, stopButton
    def setVar(self, frame, varText, default):
        strVar = tk.StringVar()
        strVar.set(default)
        tk.Label(frame, text=(varText).ljust(12)).grid(row=0, column=0)
        tk.Label(frame, textvariable=strVar).grid(row=0, column=1)
        return strVar
    def start(self):
        self.master.startWlbt()
    def stop(self):
        if hasattr(self.master, 'cyclesId'):
            self.master.after_cancel(self.master.cyclesId)
            self.master.configGUI.changeEntriesState('normal')
            self.statusVar.set('STATUS_IDLE')

class CanvasGUI(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text='Raw Image Slice: Phi / R')
        self.canvas = tk.Canvas(self, width=CANVAS_WIDTH,
                height=CANVAS_HEIGHT)
        self.canvas.pack()
        self.canvas.configure(background='#'+COLORS[0])
        self.cells = []
    def setGrid(self, sizeX, sizeY):
        recHeight, recWidth = CANVAS_WIDTH/sizeX, CANVAS_HEIGHT/sizeY
        self.cells = [[self.canvas.create_rectangle(recWidth*col,
            recHeight*row, recWidth*(col+1), recHeight*(row+1), width=0)
            for col in range(sizeY)] for row in range(sizeX)]
    def update(self, rawImage, lenOfPhi, lenOfR):
        for i in range(lenOfPhi):
            for j in range(lenOfR):
                self.canvas.itemconfigure(self.cells[lenOfPhi-i-1][j],
                    fill='#'+COLORS[rawImage[i][j]])

class Walabot:
    def __init__(self, master):
        self.master = master
        if platform == 'win32': # for windows
            path = join('C:/', 'Program Files', 'Walabot', 'WalabotSDK',
                'python')
        else: # for linux, raspberry pi, etc.
            path = join('/usr', 'share', 'walabot', 'python')
        self.wlbt = load_source('WalabotAPI', join(path, 'WalabotAPI.py'))
        self.wlbt.Init()
        self.wlbt.SetSettingsFolder()
    def isConnected(self):
        try:
            self.wlbt.ConnectAny()
        except self.wlbt.WalabotError as err:
            if err.code == 19: # 'WALABOT_INSTRUMENT_NOT_FOUND'
                return False
        return True
    def setParams(self, rParams, thetaParams, phiParams, thld, mtiMode):
        self.wlbt.SetProfile(self.wlbt.PROF_SENSOR)
        try:
            self.wlbt.SetArenaR(*tuple(map(float, rParams)))
            self.wlbt.SetArenaTheta(*tuple(map(float, thetaParams)))
            self.wlbt.SetArenaPhi(*tuple(map(float, phiParams)))
            self.wlbt.SetThreshold(float(thld))
        except self.wlbt.WalabotError as err:
            self.master.controlGUI.errorVar.set(str(err))
        if mtiMode:
            self.wlbt.SetDynamicImageFilter(self.wlbt.FILTER_TYPE_MTI)
        else:
            self.wlbt.SetDynamicImageFilter(self.wlbt.FILTER_TYPE_NONE)
        self.wlbt.Start()
    def getArenaParams(self):
        rParams = self.wlbt.GetArenaR()
        thetaParams = self.wlbt.GetArenaTheta()
        phiParams = self.wlbt.GetArenaPhi()
        threshold = self.wlbt.GetThreshold()
        return rParams, thetaParams, phiParams, threshold
    def calibrate(self):
        self.wlbt.StartCalibration()
        while self.wlbt.GetStatus()[0] == self.wlbt.STATUS_CALIBRATING:
            self.wlbt.Trigger()
    def getRawImageSliceDimensions(self):
        return self.wlbt.GetRawImageSlice()[1:3]
    def triggerAndGetRawImageSlice(self):
        self.wlbt.Trigger()
        return self.wlbt.GetRawImageSlice()[0]
    def getFps(self):
        return int(self.wlbt.GetAdvancedParameter('FrameRate'))

def configureWindow(root):
    root.title('Walabot - Raw Image Slice Example')
    iconPath = join(dirname(argv[0]), 'raw-image-slice-icon.png')
    iconFile = tk.PhotoImage(file=iconPath)
    root.tk.call('wm', 'iconphoto', root._w, iconFile) # set app icon
    root.geometry('+{}+{}'.format(APP_X, APP_Y))
    root.resizable(width=False, height=False)
    root.option_add('*Font', 'TkFixedFont')

def startApp():
    root = tk.Tk()
    configureWindow(root)
    MainGUI(root).pack()
    root.mainloop()

if __name__ == '__main__':
    startApp()