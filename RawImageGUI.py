from __future__ import print_function
from imp import load_source
from os.path import join, dirname
from sys import platform, argv
from string import digits
try: import Tkinter as tk
except: import tkinter as tk

APP_X, APP_Y = 50, 50
CANVAS_WIDTH, CANVAS_HEIGHT = 500, 500
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
RMIN_CONFIG = ('rMin', 1, 1000, 10)
RMAX_CONFIG = ('rMax', 1, 1000, 100)
RRES_CONFIG = ('rRes', 0.1, 10, 2)
TMIN_CONFIG = ('thetaMin', -90, 90, -20)
TMAX_CONFIG = ('thetaMax', -90, 90, 20)
TRES_CONFIG = ('thetaRes', 0.1, 10, 10)
PMIN_CONFIG = ('phiMin', -90, 90, -45)
PMAX_CONFIG = ('phiMax', -90, 90, 45)
PRES_CONFIG = ('phiRes', 0.1, 10, 2)
THLD_CONFIG = ('threshold', 0.1, 100, 15)

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
            if not params[4]: # equals: if not mtiMode
                self.controlGUI.statusVar.set('STATUS_CALIBRATING')
                self.update_idletasks()
                self.wlbt.calibrate()
            self.lenOfPhi, self.lenOfR = self.wlbt.getRawImageSliceDimensions()
            self.canvasGUI.setGrid(self.lenOfPhi, self.lenOfR)
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
        self.lines = [self.setLines(self, i) for i in range(11)]
        self.rMin = self.setVar(self.lines[0], *RMIN_CONFIG)
        self.rMax = self.setVar(self.lines[1], *RMAX_CONFIG)
        self.rRes = self.setVar(self.lines[2], *RRES_CONFIG)
        self.tMin = self.setVar(self.lines[3], *TMIN_CONFIG)
        self.tMax = self.setVar(self.lines[4], *TMAX_CONFIG)
        self.tRes = self.setVar(self.lines[5], *TRES_CONFIG)
        self.pMin = self.setVar(self.lines[6], *PMIN_CONFIG)
        self.pMax = self.setVar(self.lines[7], *PMAX_CONFIG)
        self.pRes = self.setVar(self.lines[8], *PRES_CONFIG)
        self.thld = self.setVar(self.lines[9], *THLD_CONFIG)
        self.mti = self.setMtiVar(self.lines[10])
    def setLines(self, master, i):
        frame = tk.Frame(master)
        frame.grid(row=i, sticky=tk.W, pady=0)
        return frame
    def setVar(self, line, varValue, minValue, maxValue, defaultValue):
        tk.Label(line, text=varValue+' = ').pack(side=tk.LEFT)
        strVar = tk.StringVar()
        strVar.set(defaultValue)
        entry = tk.Entry(line, width=4, textvariable=strVar)
        entry.pack(side=tk.LEFT)
        strVar.trace('w', lambda a, b, c,
            strVar=strVar: self.validate(strVar, entry, minValue, maxValue))
        tk.Label(line, text=' value between '+str(minValue)).pack(side=tk.LEFT)
        tk.Label(line, text='and '+str(maxValue)).pack(side=tk.LEFT)
        return strVar
    def validate(self, strVar, entry, minValue, maxValue):
        num = strVar.get()
        if not num:
            self.alertForInvalidValue(entry); return
        for digit in num:
            if digit not in digits:
                self.alertForInvalidValue(entry); return
        num = float(num)
        if num < minValue or num > maxValue:
            self.alertForInvalidValue(entry); return
        entry.config(fg='gray1')
    def alertForInvalidValue(self, entry):
        entry.config(fg='#'+COLORS[235])
    def setMtiVar(self, line):
        tk.Label(line, text='mti = ').pack(side=tk.LEFT)
        mtiVar = tk.BooleanVar()
        mtiVar.set(0)
        rTrue = tk.Radiobutton(line, text='True', variable=mtiVar, value=1)
        rFalse = tk.Radiobutton(line, text='False', variable=mtiVar, value=0)
        rTrue.pack(side=tk.LEFT)
        rFalse.pack(side=tk.LEFT)
        return mtiVar
    def setThresholdLine(self, line, lineText):
        tk.Label(line, text=lineText).pack(side=tk.LEFT)
        entry = tk.Entry(line, width=4).pack(side=tk.LEFT)
        tk.Label(line, text=')').pack(side=tk.LEFT)
        return entry
    def getParams(self):
        rParams = (self.rMin.get(), self.rMax.get(), self.rRes.get())
        tParams = (self.tMin.get(), self.tMax.get(), self.tRes.get())
        pParams = (self.pMin.get(), self.pMax.get(), self.pRes.get())
        thldParam, mtiParam = self.thld.get(), self.mti.get()
        return rParams, tParams, pParams, thldParam, mtiParam

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
        if mtiMode == '0':
            self.wlbt.SetDynamicImageFilter(self.wlbt.FILTER_TYPE_MTI)
        else:
            self.wlbt.SetDynamicImageFilter(self.wlbt.FILTER_TYPE_NONE)
        self.wlbt.Start()
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
    iconPath = join(dirname(argv[0]), 'RawImageGUI-icon.png')
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
