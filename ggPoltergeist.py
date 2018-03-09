from PIL import Image
import pytesseract
import tkinter
import cv2
import os
#from plyer import filechooser
import webbrowser
import numpy as np
import re
import sys
root = tkinter.Tk()
root.title("ggPoltergeist")
class varStore():
    def __init__(self):
        self.fenceWidth = 35
        self.postProcVar = tkinter.IntVar()
        self.cropVar = tkinter.BooleanVar(value=True)
        self.outputVar = tkinter.BooleanVar()
        self.cropModel = tkinter.StringVar()
        self.contrastVar = tkinter.BooleanVar()
        self.cropOptions = ["Mi Mix 2", "Pixel/XL", "Note8", "bottom text"]
        self.quizOption = tkinter.StringVar()
        self.quizOptions = ["HQ Trivia", "Quizbiz", "Beat The Q", "Cash Show", "Joyride", "QuizUp"]
    def returnVars(self):
        print("postProcVar, cropVar, cropModel, outputVar, contrastVar")
        print(self.postProcVar.get(),self.cropVar.get(),self.cropModel.get(),self.outputVar.get(),self.contrastVar.get())
vs = varStore()

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
cropShow = tkinter.Checkbutton(cropFence, text="Show output image", variable=vs.outputVar)
cropShow.pack(anchor=tkinter.W)
cropOption = tkinter.OptionMenu(cropFence, vs.cropModel, *vs.cropOptions)
vs.cropModel.set("Select Device")
cropOption.pack(anchor=tkinter.W)
postProcInfo = tkinter.Label(cropFence, width=vs.fenceWidth, text="Crop image when using phone.\nDo not crop for debugging.\nSelect phone model.                                    ",justify=tkinter.LEFT)
postProcInfo.pack(anchor=tkinter.W)

deviceFence = tkinter.LabelFrame(root, text="Device settings")
deviceFence.pack(expand="yes")
quizOption = tkinter.OptionMenu(deviceFence, vs.quizOption, *vs.quizOptions)
vs.quizOption.set("Select Quiz")
quizOption.pack(anchor=tkinter.W)
deviceInfo = tkinter.Label(deviceFence, width=vs.fenceWidth, text="Device list should show one device only.\nOnly works with USB debugging enabled.\nGo to <LINK> for tutorial.",justify=tkinter.LEFT)
deviceInfo.pack(anchor=tkinter.W)

def popup(text1,text2):
    toplevel = tkinter.Toplevel()
    label1 = tkinter.Label(toplevel,font = ("Arial", 20), text=text1, height=0, width=20)
    label1.pack()
    label2 = tkinter.Label(toplevel, text=text2, height=0, width=50)
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
            if vs.quizOption.get() == 'QuizUp':
                image = image[int(height/8):int((height/4)*2),0:int(width)]
            else:
                popup("Error","Image callibration doesn't exist; abort")
                break
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
        text1 = text.split("?")
        text1 = text1[0].split(".")
        text1 = text1[len(text1) - 1]
        text1 = text1.replace("\n", " ")
        print(text1)

        url = "https://www.google.com/search?q={}".format(text1)
        webbrowser.open(url)
        os.system("adb shell rm /sdcard/screen.png")
        os.remove("ggTemp.png")
        loop = False
fileButton = tkinter.Button(root, text="Select file",command=lambda : callback(1))
fileButton.pack(anchor=tkinter.W)

root.mainloop()
