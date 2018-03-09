class benchmark():
    def __init__(self):
        self.startup = 0
bench = benchmark()
import time
bench.startup = time.time()
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
root.title("Benchmark")
class varStore():
    def __init__(self):
        self.fenceWidth = 35
        self.postProcVar = tkinter.IntVar()
        self.cropVar = tkinter.BooleanVar(value=True)
        self.quizOption = tkinter.StringVar()
        self.quizOptions = ["QuizUp"]
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

cropFence = tkinter.LabelFrame(root, text="Image Cropping")
cropFence.pack(expand="yes")
cropCheck = tkinter.Checkbutton(cropFence, text="Crop image                                                     ", variable=vs.cropVar,state=tkinter.DISABLED)
cropCheck.pack(anchor=tkinter.W)

deviceFence = tkinter.LabelFrame(root, text="Device settings")
deviceFence.pack(expand="yes")
quizOption = tkinter.OptionMenu(deviceFence, vs.quizOption, *vs.quizOptions)
quizOption.config(state=tkinter.DISABLED)
vs.quizOption.set("QuizUp")
quizOption.pack(anchor=tkinter.W)
deviceInfo = tkinter.Label(deviceFence, width=vs.fenceWidth, text="Device list should show one device only.\nOnly works with USB debugging enabled.\nGo to <LINK> for tutorial.",justify=tkinter.LEFT)
deviceInfo.pack(anchor=tkinter.W)

def popup(text1,text2):
    toplevel = tkinter.Toplevel()
    label1 = tkinter.Label(toplevel,font = ("Arial", 20), text=text1, height=0, width=20)
    label1.pack()
    label2 = tkinter.Label(toplevel, text=text2, height=0, width=50)
    label2.pack()
def scores(text1,text2,text3,text4,text5,text6,text7,accuracy):
    toplevel = tkinter.Toplevel()
    title = tkinter.Label(toplevel,font = ("Arial Bold", 25), text="Benchmark Scores", height=0, width=20)
    title.pack()
    if accuracy == True:
        passCheck = tkinter.Label(toplevel,font = ("Arial Bold", 15), text="OCR was 100% correct", height=0, width=20, fg='green')
        passCheck.pack()
    else:
        passCheck = tkinter.Label(toplevel,font = ("Arial Bold", 15), text="OCR accuracy test failed", height=0, width=20, foreground='red')
        passCheck.pack()
    label1 = tkinter.Label(toplevel, text="Program startup time :"+str(text1), height=0, width=50)
    label1.pack()
    label2 = tkinter.Label(toplevel, text="ADB transfer time :"+str(text2), height=0, width=50)
    label2.pack()
    label3 = tkinter.Label(toplevel, text="Image crop time :"+str(text3), height=0, width=50)
    label3.pack()
    label4 = tkinter.Label(toplevel, text="Image postprocessing time :"+str(text4), height=0, width=50)
    label4.pack()
    label5 = tkinter.Label(toplevel, text="Image OCR time :"+str(text5), height=0, width=50)
    label5.pack()
    label6 = tkinter.Label(toplevel, text="Browser opening time :"+str(text6), height=0, width=50)
    label6.pack()
    title = tkinter.Label(toplevel,font = ("Arial", 15), text="==============================\nFinal score: "+str(text7)+"\n==============================", height=0, width=50)
    title.pack()
    label6 = tkinter.Label(toplevel, text="How to interpret your scores:\nScores are measured in seconds, the lower the better.\nA final score of above 2s is undesired.\nAnything above 3s is hard to use.\nImprove your scores by running from fast storage, like an SSD.\nYou could also compile tesseract-ocr yourself to use OpenCL features.\nYou could use a faster browser, or use faster internet.\nBetter PC specs will decrease OCR,post processing and crop times.\n A better phone will decrease ADB time.\nProgram startup time is just a fun metric.\nIt isn't part of the final score and shouldn't affect real world use.", height=0, width=80)
    label6.pack()

def callback(event):
    bench.start = time.time()
    loop = True
    while loop == True:
        try:
            os.system("adb shell screencap -p /sdcard/screen.png")
            os.system("adb pull /sdcard/screen.png")
            image = cv2.imread("screen.png")
            height, width, channels = image.shape
        except:
            print("NO DEVICES FOUND. SKIPPING ADB BENCHMARK.")
            image = cv2.imread("BenchmarkDemo.png")
            height, width, channels = image.shape

        bench.adbEnd = time.time() - bench.start

        #image = cv2.resize(image, (0,0), fx=0.4, fy=0.4)
        height, width, channels = image.shape
        #image = image[int(width/8):int(width),0:int(height)]
        image = image[int(height/8):int((height/4)*2),0:int(width)]

        bench.cropEnd = (time.time() - bench.start) - bench.adbEnd

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if vs.postProcVar.get() == 1:
            gray = cv2.medianBlur(gray, 3)
        else:
            gray = cv2.threshold(gray, 1, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)[1]

        bench.postProcEnd = ((time.time() - bench.start) - bench.adbEnd) - bench.cropEnd

        cv2.imwrite("ggTemp.png", gray)
        text = pytesseract.image_to_string(Image.open('ggTemp.png'))

        bench.ocrEnd = (((time.time() - bench.start) - bench.adbEnd) - bench.cropEnd) - bench.postProcEnd

        #os.remove("ggTemp.png")
        text1 = text.split("?")
        text1 = text1[0].split(".")
        text1 = text1[len(text1) - 1]
        text1 = text1.replace("\n", " ")
        print(text1)

        url = "https://www.google.com/search?q={}".format(text1)
        webbrowser.open(url)
        os.system("adb shell rm /sdcard/screen.png")
        bench.browserEnd = ((((time.time() - bench.start) - bench.adbEnd) - bench.cropEnd) - bench.postProcEnd) - bench.ocrEnd
        loop = False
    print(bench.startupEnd)
    print("==============")
    print(bench.adbEnd)
    print(bench.cropEnd)
    print(bench.postProcEnd)
    print(bench.ocrEnd)
    print(bench.browserEnd)
    bench.end = bench.adbEnd+bench.cropEnd+bench.postProcEnd+bench.ocrEnd+bench.browserEnd
    print("Final score:",bench.end)
    if text1 == 'What is the basic unit of resistance':
        accuracy = True
    else:
        accuracy = False
    scores(bench.startupEnd, bench.adbEnd, bench.cropEnd, bench.postProcEnd, bench.ocrEnd, bench.browserEnd, bench.end, accuracy)
    os.remove("ggTemp.png")
fileButton = tkinter.Button(root, text="Start benchmark",command=lambda : callback(1))
fileButton.pack(anchor=tkinter.W)
bench.startupEnd = time.time() -  bench.startup
print(bench.startupEnd)
root.mainloop()
