import os
print("Calibrate v1.1")
import time
from PIL import Image
import tkinter
import tkinter.messagebox
import cv2
from tkinter.filedialog import askopenfilename
import webbrowser
import numpy as np
import re
import sys

root = tkinter.Tk()#Initializes the tkinter window
root.wm_iconbitmap(default='calibrate.ico')#This doesn't work on Linux for some reason. fuck linux tbh
root.title("Config calibrate")

class varstore():#Holds variables in a class because globals annoy me and I've just gotten used to doing it this way.
    def __init__(self):
        self.filename = ""
        self.y1 = 0#Placeholders
        self.y2 = 0
        self.x1 = 0
        self.x2 = 0
        self.cropOptions = ["16:9","18:9"]#Calibrations for a 16:9 phone won't work on 18:9, and vice versa.
        self.cropModel = tkinter.StringVar()
vs = varstore()

heightFence = tkinter.LabelFrame(root, text="Height cropping")
heightFence.pack(expand="yes")
topHeightCrop = tkinter.Scale(heightFence, from_=1, to=100, length=300,label="Crop from top",orient=tkinter.HORIZONTAL)
topHeightCrop.grid(row=0,column=0)
bottomHeightCrop = tkinter.Scale(heightFence, from_=1, to=100, length=300,label="Crop from bottom",orient=tkinter.HORIZONTAL)
bottomHeightCrop.set(100)
bottomHeightCrop.grid(row=0,column=1)

widthFence = tkinter.LabelFrame(root, text="Width cropping")
widthFence.pack(expand="yes")
leftWidthCrop = tkinter.Scale(widthFence, from_=1, to=100, length=300,label="Crop from left",orient=tkinter.HORIZONTAL)
leftWidthCrop.grid(row=0,column=0)
rightWidthCrop = tkinter.Scale(widthFence, from_=1, to=100, length=300,label="Crop from right",orient=tkinter.HORIZONTAL)
rightWidthCrop.set(100)
rightWidthCrop.grid(row=0,column=1)

imageFence = tkinter.LabelFrame(root, text="Image")
imageFence.pack(expand="yes")
fileButton = tkinter.Button(imageFence, text="Select screenshot",command=lambda : fileSelect())#Used lambdas because otherwise the buttons will have the action triggered at start
fileButton.pack(anchor=tkinter.W)
cropOption = tkinter.OptionMenu(imageFence, vs.cropModel, *vs.cropOptions)
vs.cropModel.set("16:9")
cropOption.pack(anchor=tkinter.W)
startButton = tkinter.Button(imageFence, text="Refresh image",command=lambda : refresh_())
startButton.pack(anchor=tkinter.W)
exportButton = tkinter.Button(imageFence, text="Export as config",command=lambda : export(vs.y1,vs.y2,vs.x1,vs.x2))
exportButton.pack(anchor=tkinter.W)

def fileSelect():#Opens native OS file selector
    vs.filename = askopenfilename()

def refresh_():#Makes the edited image pop up, so it can be saved or further adjusted
    try:
        image = cv2.imread(vs.filename)#Opens the image
        height, width, channels = image.shape#Gets dimensions
        #image = cv2.resize(image, (0,0), fx=0.4, fy=0.4)
        image = cv2.resize(image, (0,0), fx=0.28, fy=0.28)#The smaller the image is resized to, the faster the OCR can run. Too small makes it unreadable though.
        vs.y1 = topHeightCrop.get()
        vs.y2 = bottomHeightCrop.get()
        vs.x1 = leftWidthCrop.get()
        vs.x2 = rightWidthCrop.get()
        image = image[int(height/100)*vs.y1:int((height/100)*vs.y2),int((width/100)*vs.x1):int((width/100)*vs.x2)] #Crops it to user's liking - as set by sliders
        try:
            cv2.imshow("Output", image)
        except cv2.error:
            tkinter.messagebox.showerror("Error", "Cannot overcrop, check that slider values are correct.") #Overcropping so bottom is above top results in this
    except:
        tkinter.messagebox.showerror("Error", "Select an image first.")
    cv2.waitKey(0)
def export(y1,y2,x1,x2):
    def writeToConfig(name):
        with open(name+".ggpconf", 'w') as file:
            info = {}
            name_ = str(name)
            info[name_] = [vs.y1,vs.y2,vs.x1,vs.x2,vs.cropModel.get()]#Stores config as dict using the .ggpconf extension, but it's just text
            file.write(str(info))
        tkinter.messagebox.showinfo("Config saved", "Your config has been exported. To use it, place it in the configs folder for ggPoltergeist.")
    if vs.y1 == 0 and vs.y1 == 0 and vs.x1 == 0 and vs.x2 == 0:
        tkinter.messagebox.showerror("Error", "Cannot export unmodified values, try opening an image and refreshing it.")
    else:#User names it and it is then saved.
        toplevel = tkinter.Toplevel()
        nameLabel = tkinter.Label(toplevel,text="Enter config name")
        nameLabel.grid(row=1,column=0)
        nameBox = tkinter.Entry(toplevel,width=30)
        nameBox.grid(row=1,column=1)
        nameSet = tkinter.Button(toplevel,text="Export",command=lambda : writeToConfig(nameBox.get()))
        nameSet.grid(row=1,column=2)

root.mainloop()
