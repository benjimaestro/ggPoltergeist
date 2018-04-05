print("ggPoltergeist v2 Private Release\n")
print("Discord: Benjimaestro#0119\nReddit: /u/benjimaestro\nGithub: github.com/benjimaestro")
import os
os.system('setx TESSDATA_PREFIX "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"')

import requests
from bs4 import BeautifulSoup
import threading
import multiprocessing as mp
import wikipediaapi
import time
import nltk
import pytesseract
import cv2
import re
import sys
import glob
import ast
from PIL import Image

import tkinter.messagebox
root = tkinter.Tk()
root.title("ggPoltergeist v2.0")
root.resizable(False, False)
root.wm_attributes("-topmost", 1)



class varstore():
    def __init__(self):
        self.countGoogle = []
        self.countWiki = []
        self.list1 = []
        self.list2 = []
        self.list3 = []
        self.finish_ = 0.0
        self.question_nouns = ''
        self.quizOption = tkinter.StringVar()
        self.localeOption = tkinter.StringVar()
        self.quizupConf = {'q':[5, 16, 1, 100],'a1':[54, 61, 1, 100],'a2':[67, 76, 1, 100],'a3':[25, 34, 1, 100]}
        self.cashshowConf = {'q':[33, 58, 10, 190],'a1':[73, 87, 29, 175],'a2':[93, 106, 29, 175],'a3':[110, 125, 29, 175]}
        self.preset = {"CashShow [18:9]":{'q':[33, 58, 10, 190],'a1':[73, 87, 29, 175],'a2':[93, 106, 29, 175],'a3':[110, 125, 29, 175]},
                        "CashShow [16:9]":{'q':[45, 72, 10, 190],'a1':[81, 97, 29, 175],'a2':[105, 119, 29, 175],'a3':[124, 140, 29, 175]},
                        "QuizUp [18:9]": {'q':[5, 16, 1, 100],'a1':[54, 61, 1, 100],'a2':[67, 76, 1, 100],'a3':[25, 34, 1, 100]}
                        }
        self.presetList = ["CashShow [18:9]","CashShow [16:9]", "QuizUp [18:9]"]
        self.presetOption = tkinter.StringVar()
        self.text = {}
        self.fenceWidth = 35
        self.localeList = ["EN-US","EN-GB","ID","IN", "FR","DE","BR"]
        self.locale = {
                       "EN-US":"https://www.google.com/search?hl=en&q=",
                       "EN-GB":"https://www.google.co.uk/search?hl=en&q=",
                       "ID":"https://www.google.co.id/search?hl=en&q=",
                       "FR":"https://www.google.fr/search?hl=en&q=",
                       "DE":"https://www.google.de/search?hl=en&q=",
                       "BR":"https://www.google.com.br/search?hl=en&q="
                       }


def nounify(question):
    for q in nltk.pos_tag(nltk.word_tokenize(question)):
        if q[1] == 'NN' or q[1] == 'NNP':
            vs.question_nouns += " " + q[0]
    vs.question_nouns = vs.question_nouns.strip().split(' ')

    print("Nouns:", vs.question_nouns)

def count_words(url, the_word):
    r = requests.get(url, allow_redirects=False)
    soup = BeautifulSoup(r.content, 'lxml')
    words = soup.find(text=lambda text: text and the_word in text)
    try:
        return len(words)
    except:
        return 0

def wikipedia_(answer, q, cCount):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(q)
    count = 0
    answer_ = answer
    count = page.text.lower().split().count(answer)
    cCount.value = count
    print(answer, count)

def google_(word,q,finish,qOut,finish_,locale):
    q = q.replace(" ", "+")
    url = str(locale+q)
    count = count_words(url, word)
    if vs.list1 != []:
        if vs.list2 != []:
            vs.list3 = [word,count]
        else:
            vs.list2 = [word,count]
    else:
        vs.list1 = [word,count]
    #print(qOut)
    if finish == 1.0:
        vs.finish_ = 1.0
    return qOut
def counter(a1,a2,a3,q,vs):
    #d = manager.dict()
    #d[0] = a1
    #d[1] = a2
    #d[2] = a3
    #finish_ = mp.Value('d', 0.0)
    #c1_Count = mp.Value('d', 0.0)
    #c2_Count = mp.Value('d', 0.0)
    #c3_Count = mp.Value('d', 0.0)

    #c1_ = mp.Process(target=google_, args=(a1,q,c1_Count,0.0,q1Out,finish_,vs.locale[vs.localeOption.get()]))
    #c2_ = mp.Process(target=google_, args=(a2,q,c2_Count,0.0,q2Out,finish_,vs.locale[vs.localeOption.get()]))
    #c3_ = mp.Process(target=google_, args=(a3,q,c3_Count,1.0,q3Out,finish_,vs.locale[vs.localeOption.get()]))
    #c1_.start()
    #c2_.start()
    #c3_.start()

    threading.Thread(target=google_(a1,q,0.0,vs.list1,vs.finish_,vs.locale[vs.localeOption.get()])).start()
    threading.Thread(target=google_(a2,q,0.0,vs.list2,vs.finish_,vs.locale[vs.localeOption.get()])).start()
    threading.Thread(target=google_(a3,q,1.0,vs.list3,vs.finish_,vs.locale[vs.localeOption.get()])).start()


    while vs.finish_ == 0.0:
        pass

    print(vs.list1)
    print(vs.list1[0], vs.list1[1])
    print(vs.list2[0], vs.list2[1])
    print(vs.list3[0], vs.list3[1])
    perc = vs.list1[1]+vs.list2[1]+vs.list3[1]
    try:
        list1perc = str(round((vs.list1[1]/perc)*100, 1)) + "% "
    except:
        list1perc = "0% "
    try:
        list2perc = str(round((vs.list2[1]/perc)*100, 1)) + "% "
    except:
        list2perc = "0% "
    try:
        list3perc = str(round((vs.list3[1]/perc)*100, 1)) + "% "
    except:
        list3perc = "0% "
    results = str(q)+"\n"+str(vs.list1[0])+": "+list1perc+"("+str(vs.list1[1])+")\n"+str(vs.list2[0])+": "+list2perc+"("+str(vs.list2[1])+")\n"+str(vs.list3[0])+": "+list3perc+"("+str(vs.list3[1])+")"
    tkinter.messagebox.showinfo("Results (using "+vs.localeOption.get()+", "+vs.presetOption.get()+")", results)
    #os.system("adb shell rm /sdcard/screen.png")
    #os.remove("ggq.png")
    #os.remove("screen.png")
    #os.remove("gga1.png")
    #os.remove("gga2.png")
    #os.remove("gga3.png")

def classTest(x):
    vs.x_ = x
    print(vs.x_)
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
def ocrRun(name, image_, height, width):

    fileName = "gg"+name+".png"
    preset = vs.preset[vs.presetOption.get()][name]
    img = image_[int((height/500)*preset[0]):int((height/500)*preset[1]),int((width/500)*preset[2]):int((width/500)*preset[3])]
    cv2.imwrite(fileName, img)
    text = pytesseract.image_to_string(Image.open(fileName))
    text = text.replace("\n", " ")
    vs.text[name] = text.replace("|", "I")
def setParams():
    start()
def start():
    def callback():
        os.system("adb shell screencap -p /sdcard/screen.png")
        os.system("adb pull /sdcard/screen.png")
        image = cv2.imread("screen.png")
        height, width, channels = image.shape
        image = cv2.resize(image, (0,0), fx=0.4, fy=0.4)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.threshold(image, 1, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)[1]
        threading.Thread(target=ocrRun('q',image,height, width)).start()
        threading.Thread(target=ocrRun('a1',image,height, width)).start()
        threading.Thread(target=ocrRun('a2',image,height, width)).start()
        threading.Thread(target=ocrRun('a3',image,height, width)).start()
        print(vs.text)
        counter(vs.text['a1'],vs.text['a2'],vs.text['a3'],vs.text['q'],vs)

    toplevel = tkinter.Toplevel()
    toplevel.wm_attributes("-topmost", 1)
    label1 = tkinter.Button(toplevel,font = ("Arial", 60),bg='green', text="Run", command=lambda:callback())
    label1.pack()
if __name__ == '__main__':
    vs = varstore()

    deviceFence = tkinter.LabelFrame(root, text="Device settings")
    deviceFence.pack(expand="yes")
    quizOption = tkinter.OptionMenu(deviceFence, vs.presetOption, *vs.presetList)
    vs.presetOption.set("CashShow [18:9]")
    quizOption.pack(anchor=tkinter.W)
    localeOption = tkinter.OptionMenu(deviceFence, vs.localeOption, *vs.localeList)
    vs.localeOption.set(vs.localeList[0])
    localeOption.pack(anchor=tkinter.W)
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

    adb()
    #manager = mp.Manager()
    q1Out = vs.list1
    q2Out = vs.list2
    q3Out = vs.list3
    root.mainloop()
