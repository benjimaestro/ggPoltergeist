import os
print("ggPoltergeist v1.2 Private Release\n")
print("Discord: Benjimaestro#0119\nReddit: /u/benjimaestro\nGithub: github.com/benjimaestro")
os.system('setx TESSDATA_PREFIX "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"')
from PIL import Image
import pytesseract
import tkinter
import cv2
#from plyer import filechooser
import webbrowser
import numpy as np
import re
import sys
import glob
import ast
import tkinter.messagebox
root = tkinter.Tk()
root.title("ggPoltergeist")
root.resizable(False, False)
root.wm_attributes("-topmost", 1)
class varStore():
    def __init__(self):
        self.fenceWidth = 35
        self.postProcVar = tkinter.IntVar()
        self.cropVar = tkinter.BooleanVar(value=True)
        self.outputVar = tkinter.BooleanVar()
        self.cropModel = tkinter.StringVar()
        self.contrastVar = tkinter.BooleanVar()
        self.cropOptions = ["16:9", "18:9"]
        self.quizOption = tkinter.StringVar()
        self.quizOptions = []
        self.quizParams = {"QuizUp [18:9]":[6,17,1,100],"QuizUp [16:9]":[8,17,1,100],"HQ Trivia [18:9]":[6, 13, 3, 38]}
        self.currentParams = ''
    def returnVars(self):
        print("postProcVar, cropVar, cropModel, outputVar, contrastVar")
        print(self.postProcVar.get(),self.cropVar.get(),self.cropModel.get(),self.outputVar.get(),self.contrastVar.get())
vs = varStore()
path = '.\configs'
for filename in glob.glob(os.path.join(path, '*.ggpconf')):
    with open(filename, 'r') as f:
        config = f.read()
    try:
        config = ast.literal_eval(config)
    except ValueError:
        pass
    for key in config:
        vs.quizParams[key] = config[key]
for key in vs.quizParams:
    vs.quizOptions.append(key)

postProcFence = tkinter.LabelFrame(root, text="Postprocessing")
postProcFence.pack(expand="yes")
threshButton = tkinter.Radiobutton(postProcFence, text="Thresh", variable=vs.postProcVar, value=0).pack(anchor=tkinter.W)
blurButton = tkinter.Radiobutton(postProcFence, text="Blur", variable=vs.postProcVar, value=1).pack(anchor=tkinter.W)
postProcInfo = tkinter.Label(postProcFence, width=vs.fenceWidth, text="Use thresh for speed.\nUse blur for noisy images.\nBlur is slower.                                                   ",justify=tkinter.LEFT)
postProcInfo.pack(anchor=tkinter.W)
contrastCheck = tkinter.Checkbutton(postProcFence, text="Contrast increase", variable=vs.contrastVar)
contrastCheck.pack(anchor=tkinter.W)

cropFence = tkinter.LabelFrame(root, text="Image Cropping")
cropFence.pack(expand="yes")
cropCheck = tkinter.Checkbutton(cropFence, text="Crop image", variable=vs.cropVar)
cropCheck.pack(anchor=tkinter.W)
cropOption = tkinter.OptionMenu(cropFence, vs.cropModel, *vs.cropOptions)
vs.cropModel.set("Select Screen Ratio")
#cropOption.pack(anchor=tkinter.W)
postProcInfo = tkinter.Label(cropFence, width=vs.fenceWidth, text="Crop image when using phone.\nDo not crop for debugging.\nSelect phone model.                                    ",justify=tkinter.LEFT)
postProcInfo.pack(anchor=tkinter.W)

deviceFence = tkinter.LabelFrame(root, text="Device settings")
deviceFence.pack(expand="yes")
quizOption = tkinter.OptionMenu(deviceFence, vs.quizOption, *vs.quizOptions)
vs.quizOption.set("Select Quiz")
quizOption.pack(anchor=tkinter.W)
applyButton = tkinter.Button(deviceFence, text="Refresh connected devices",command=lambda : adb())
applyButton.pack(anchor=tkinter.W)
adbDevices = tkinter.Text(deviceFence,height=4, width=30)
adbDevices.pack()
deviceInfo = tkinter.Label(deviceFence, width=vs.fenceWidth, text="Device list should show one device only.\nOnly works with USB debugging enabled.\nCheck wiki for tutorial.\nMake sure that aspect ratio is correct.",justify=tkinter.LEFT)
deviceInfo.pack(anchor=tkinter.W)

applyButton = tkinter.Button(root, text="Apply settings",command=lambda : setParams())
applyButton.pack(anchor=tkinter.W)

fileButton = tkinter.Button(root, text="Help",command=lambda : webbrowser.open("https://github.com/benjimaestro/ggPoltergeist/wiki/How-to-use-ggPoltergeist"))
fileButton.pack(anchor=tkinter.W)

def adb():
    try:
        deviceName = os.popen('adb shell getprop ro.product.model').read().strip()
        device = os.popen('adb devices').read().strip()
        device = device.split("\n")
        device[1] = device[1].split("\t")
        device_ = deviceName +" ("+ device[1][0]+")"
    except:
        device_ = "No devices found.\nMake sure it is connected\nwith USB debugging enabled."
    adbDevices.delete("1.0",tkinter.END)
    adbDevices.insert(tkinter.END,device_)

def setParams():
    if vs.quizOption.get() == 'Select Quiz':
        tkinter.messagebox.showerror("Error", "Make sure quiz option was set, and you're using the right screen ratio for optimal results.")
    else:
        vs.currentParams = vs.quizParams[vs.quizOption.get()]
        start()

def start():
    toplevel = tkinter.Toplevel()
    toplevel.wm_attributes("-topmost", 1)
    label1 = tkinter.Button(toplevel,font = ("Arial", 60),bg='green', text="Run", command=lambda:callback(1))
    label1.pack()

def popup(text1,text2):
    toplevel = tkinter.Toplevel()
    label1 = tkinter.Label(toplevel,font = ("Arial", 20), text=text1, height=0, width=20)
    label1.pack()
    label2 = tkinter.Label(toplevel, text=text2, height=0, width=70)
    label2.pack()

def callback(event):
    loop = True
    while loop == True:
        os.system("adb shell screencap -p /sdcard/screen.png")
        os.system("adb pull /sdcard/screen.png")
        image = cv2.imread("screen.png")
        if vs.cropVar.get() == True:
            #image = cv2.resize(image, (0,0), fx=0.4, fy=0.4)
            height, width, channels = image.shape
            #image = image[int(width/8):int(width),0:int(height)]
            #image = cv2.resize(image, (0,0), fx=0.4, fy=0.4)
            image = cv2.resize(image, (0,0), fx=0.28, fy=0.28)
            image = image[int((height/100)*vs.currentParams[0]):int((height/100)*vs.currentParams[1]),int((width/100)*vs.currentParams[2]):int((width/100)*vs.currentParams[3])]
        else:
            pass

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if vs.postProcVar.get() == 1:
            gray = cv2.medianBlur(gray, 3)
        else:
            gray = cv2.threshold(gray, 1, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)[1]

        cv2.imwrite("ggTemp.png", gray)
        text = pytesseract.image_to_string(Image.open('ggTemp.png'))
        if vs.outputVar == True:
            cv2.imshow("Output", Image.open('ggTemp.png'))
        else:
            pass
        #text1 = text.split("?")
        #text1 = text1[0].split(".")
        #text1 = text1[len(text1) - 1]
        text = text.replace("\n", " ")
        print(text)

        url = "https://www.google.com/search?q={}".format(text)
        webbrowser.open(url)
        os.system("adb shell rm /sdcard/screen.png")
        os.remove("ggTemp.png")
        loop = False
adb()
root.mainloop()
