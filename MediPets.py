from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
from cryptography.fernet import Fernet
import os.path
import os
from tkinter import messagebox
import datetime
import threading
import math
import sys

#Generates a key to encrypt user data file
def keyGen():
    key = Fernet.generate_key()
    file = open('keyFile.key', 'wb')
    file.write(key)
    file.close
    return key

#Reads the key from keyFile.key
def keyRead():
    if (os.path.exists('keyFile.key')):
        file = open('keyFile.key','rb')
        key = file.read()
        file.close
    else:
        key = keyGen()
    return key

#Decrypts userData file
def readUserFile():
    key = Fernet(keyRead())
    file = open("userData.txt",'rb')
    data = file.readlines()
    file.close()
    name = key.decrypt(data[0])
    last = key.decrypt(data[1])
    animal = key.decrypt(data[2])
    med = key.decrypt(data[3])
    amount = key.decrypt(data[4])
    interval = key.decrypt(data[5])
    global readname
    readname = name.decode()
    global readlast
    readlast = last.decode()
    global readanimal
    readanimal = animal.decode()
    global readmed
    readmed = med.decode()
    global readamount
    readamount = amount.decode()
    global readInterval
    readInterval = interval.decode()
    
#Encrypts userData file and writes to file
def encodeUserFile(newName, newLast, newAnimal, newMed, newAmount, newInterval):
    encodedName = newName.encode()
    encodedLast = newLast.encode()
    encodedAnimal = newAnimal.encode()
    encodedMed = newMed.encode()
    encodedAmount = newAmount.encode()
    encodedInterval = newInterval.encode()
    newLine = '\n'.encode()
    key = Fernet(keyRead())
    encryptedName = key.encrypt(encodedName)
    encryptedLast = key.encrypt(encodedLast)
    encryptedAnimal = key.encrypt(encodedAnimal)
    encryptedMed = key.encrypt(encodedMed)
    encryptedAmount = key.encrypt(encodedAmount)
    encryptedInterval = key.encrypt(encodedInterval)
    file = open("userData.txt",'wb')
    file.write(encryptedName)
    file.write(newLine)
    file.write(encryptedLast)
    file.write(newLine)
    file.write(encryptedAnimal)
    file.write(newLine)
    file.write(encryptedMed)
    file.write(newLine)
    file.write(encryptedAmount)
    file.write(newLine)
    file.write(encryptedInterval)
    file.close()
    if 'dose' in greetText.get():
        greetText.set(newName + ", it's time to take your dose of " + newMed)
    else:
        greetText.set("Hello " + newName + ", how are you today?")

#Sets changes made by user to userData
def setChanges():
    newName = nameEnt.get()
    newLast = lastEnt.get()
    newAnimal = animalEnt.get()
    newMed = medEnt.get()
    newAmount = amountEnt.get()
    newInterval = intervalEnt.get()
    encodeUserFile(newName, newLast, newAnimal, newMed, newAmount, newInterval)
    messagebox.showinfo("Success", "Settings updated successfully")
    settingsWin.destroy()

#Sets changes from initial setup of software
def setChangesSetup(setup):
    newName = nameEnt.get()
    newLast = lastEnt.get()
    newAnimal = animalEnt.get()
    newMed = medEnt.get()
    newAmount = amountEnt.get()
    newInterval = intervalEnt.get()
    encodeUserFile(newName, newLast, newAnimal, newMed, newAmount, newInterval)
    messagebox.showinfo("Success", "Setup is complete. Please restart program")
    setup.destroy()

#Generates GUI Window to shutdown program
def shutDown():
    msgbox = messagebox.askquestion("Shutdown", "Are you sure you want to shutdown?")
    if msgbox == "yes":
        settingsWin.destroy()
        mainWin.destroy()
        quit()
    else:
        pass
    
#Generates Settings window
def launchSettings(event):
    readUserFile()
    global settingsWin
    settingsWin = Toplevel()
    settingsWin.geometry('215x500')
    settingsWin.title("Settings")
    toolbarPanel = Frame(settingsWin, width = '600', height = '64', background = 'yellowgreen')
    toolbarPanel.pack()
    homelbl = Label(toolbarPanel, text = "Settings", bg = 'yellowgreen', fg = 'white')
    homelbl.place(x = 30, y = 5)
    nameLbl = Label(settingsWin, text = "First Name:")
    nameLbl.place(x = 5, y = 65)
    nameEntContent = StringVar()
    nameEntContent.set(readname)
    global nameEnt
    nameEnt = Entry(settingsWin, textvariable = nameEntContent)
    nameEnt.place(x = 5, y = 90)
    lastLbl = Label(settingsWin, text = "Last Name:")
    lastLbl.place(x = 5, y = 120)
    lastEntContent = StringVar()
    lastEntContent.set(readlast)
    global lastEnt
    lastEnt = Entry(settingsWin, textvariable = lastEntContent)
    lastEnt.place(x = 5, y = 145)
    animalLbl = Label(settingsWin, text = "Avatar Name:")
    animalLbl.place(x = 5, y = 175)
    animalEntContent = StringVar()
    animalEntContent.set(readanimal)
    global animalEnt
    animalEnt = Entry(settingsWin, textvariable = animalEntContent)
    animalEnt.place(x = 5, y = 200)
    medLbl = Label(settingsWin, text = "Medicine Name:")
    medLbl.place(x = 5, y = 230)
    medEntContent = StringVar()
    medEntContent.set(readmed)
    global medEnt
    medEnt = Entry(settingsWin, textvariable = medEntContent)
    medEnt.place(x = 5, y = 255)
    amountLbl = Label(settingsWin, text = "Frequency:")
    amountLbl.place(x = 5, y = 285)
    amountEntContent = StringVar()
    amountEntContent.set(readamount)
    global amountEnt
    amountEnt = Entry(settingsWin, textvariable = amountEntContent)
    amountEnt.place(x = 5, y = 310)
    intervallbl = Label(settingsWin, text = "Interval:")
    intervallbl.place (x = 5, y = 340)
    intervalEntContent = StringVar()
    intervalEntContent.set(readInterval)
    global intervalEnt
    intervalEnt = Entry(settingsWin, textvariable = intervalEntContent)
    intervalEnt.place(x = 5, y = 365)
    submitBtn = Button(settingsWin, text = "Make Changes", command = setChanges)
    submitBtn.place(x = 50, y = 395)
    shutdownBtn = Button(settingsWin, text = "Shutdown", command = shutDown)
    shutdownBtn.place(x = 65, y = 420)
    
#Function is called when user presses pillTaken button
def pillTaken(yesbtn,buttonWait):
    buttonWait.set(1)
    dateFile = open('prevDose.txt', 'w')
    prevTime = datetime.datetime.now()
    prevTime = str(prevTime)
    dateFile.write(prevTime)
    dateFile.close()
    facelbl.configure(image=smileFace)
    greetText.set("Hello " + readname + ", how are you today?")
    yesbtn.destroy()

#Constantly checks to update time
def checkPill():
    global amountTaken
    amountTaken = 0
    readUserFile()
    name = readname
    medicineName = readmed
    frequency = int(readamount)
    global buttonWait
    buttonWait = IntVar()
    interval = float(readInterval)
    interval = datetime.timedelta(hours = interval)
    intervalfloat = interval.total_seconds()/3600
    amountTaken = 0
    noticetake1 = name + ", it's time to take your dose of " + medicineName
    countdown = StringVar()
    countdown.set("--")
    countdownlbl = Label(toolbarPanel, textvariable = countdown, bg = 'yellowgreen', fg = 'yellow')
    countdownlbl.place(x = 110, y = 10)
    #While there is still more pills to be taken
    while not amountTaken >= frequency:
        curDT = datetime.datetime.now()
        global dateFile
        dateFile = open('prevDose.txt', 'r+')
        prevDose = dateFile.read()
        dateFile.close()
        prevDose = datetime.datetime.strptime(prevDose, '%Y-%m-%d %H:%M:%S.%f')
        timeDiff = curDT - prevDose
        timeDiffSec = timeDiff.total_seconds()/3600
        #Take dose if statement
        if (timeDiffSec) >= intervalfloat or (prevDose.date() != curDT.date()) :
            facelbl.configure(image=straightFace)
            countdown.set("--")
            greetText.set(noticetake1)
            global yesbtn
            yesbtn = Button(mainWin,text = "Dose Taken", command = lambda: pillTaken(yesbtn,buttonWait))
            yesbtn.pack()
            mainWin.wait_variable(buttonWait)
            amountTaken = amountTaken + 1
        #Countdown to next dose
        else:
            facelbl.configure(image=smileFace)
            nextTime = prevDose + interval
            countdowncalc = nextTime - curDT
            countdowncalc = datetime.timedelta(seconds = math.ceil(countdowncalc.total_seconds()))
            countdowncalc = str(countdowncalc)
            countdown.set(countdowncalc)
        mainWin.update()
        #While there are no more pills and it isn't a new day
    while amountTaken >= frequency and prevDose.date() == datetime.datetime.now().date():
        
        greetText.set(name + ", you have taken all of your required doses for today")
        mainWin.update()
    #If new day use checkPill method
    checkPill()

#Generates setup window for user
def launchSetup():
    global setup
    setup = Tk()
    setup.geometry("550x425")
    setup.title("Med Manager: Setup")
    welcomelbl = Label(setup, text = "Welcome to Med Manager please fill in the details below",bg = 'yellowgreen', fg = 'white')
    welcomelbl.pack()
    nameLbl = Label(setup, text = "First Name:")
    nameLbl.pack()
    global nameEnt
    nameEnt = Entry(setup)
    nameEnt.pack()
    lastLbl = Label(setup, text = "Last Name:")
    lastLbl.pack()
    global lastEnt
    lastEnt = Entry(setup)
    lastEnt.pack()
    animalLbl = Label(setup, text = "Avatar Name:")
    animalLbl.pack()
    global animalEnt
    animalEnt = Entry(setup)
    animalEnt.pack()
    medLbl = Label(setup, text = "Medicine Name:")
    medLbl.pack()
    global medEnt
    medEnt = Entry(setup)
    medEnt.pack()
    amountLbl = Label(setup, text = "Frequency:")
    amountLbl.pack()
    global amountEnt
    amountEnt = Entry(setup)
    amountEnt.pack()
    intervallbl = Label(setup, text = "Interval(hours):")
    intervallbl.pack()
    global intervalEnt
    intervalEnt = Entry(setup)
    intervalEnt.pack()
    global greetText
    greetText = StringVar()
    submitBtn = Button(setup, text = "Make Changes", command = lambda: setChangesSetup(setup))
    submitBtn.pack()
    setup.mainloop()

#Checks wether program needs to be setup     
if not os.path.exists('userData.txt'):
    launchSetup()
    mainWin = Tk()
elif os.stat('userData.txt').st_size == 0:
    launchSetup()
    mainWin = Tk()
else:
    mainWin = Tk()

#Creates main home page for application
mainWin.geometry('600x400')
mainWin.configure(bg = 'white')
mainWin.title("MediPet")
global toolbarPanel
toolbarPanel = Frame(mainWin, width = '600', height = '64', background = 'yellowgreen')
toolbarPanel.pack()
animalStatPanel = Frame(mainWin, background = 'yellowgreen')
animalStatPanel.place(x = 10, y = 150)
readUserFile()
global smileFace                      
smileFace = ImageTk.PhotoImage(Image.open("Smile.png"))
global straightFace
straightFace = ImageTk.PhotoImage(Image.open("Straight.png"))
global sadFace
sadFace = ImageTk.PhotoImage(Image.open("Sad.png"))
settingsPic = ImageTk.PhotoImage(Image.open("Settings.png"))
# TODO: Add your own avatar after Image.open
animalPic = ImageTk.PhotoImage(Image.open(""))
settingslbl = Label(toolbarPanel, image = settingsPic, bg = 'yellowgreen')
settingslbl.place(x = 535, y = -5)
settingslbl.bind("<Button-1>", launchSettings)
global facelbl
facelbl = Label(toolbarPanel, image = straightFace, bg = 'yellowgreen')
facelbl.place(x = 0, y = -5)
homelbl = Label(toolbarPanel, text = "Home", bg = 'yellowgreen', fg = 'white')
homelbl.place(x = 250, y = 5)
statlbl = Label(animalStatPanel, text = "MediPet Stats", bg = 'yellowgreen', fg = 'white')
statlbl.pack()
hungerStat = int(5)
hungerStat = str(hungerStat)
hunVar = StringVar()
hunVar.set("Hunger: " + hungerStat)
hunlbl = Label(animalStatPanel, textvariable = hunVar, bg = 'yellowgreen', fg = 'white')
hunlbl.pack()
healthStat = int(5)
healthStat = str(hungerStat)
heaVar = StringVar()
heaVar.set("Health: " + healthStat)
healbl = Label(animalStatPanel, textvariable = heaVar, bg = 'yellowgreen', fg = 'white')
healbl.pack()
aliveStat = int(5)
aliveStat = str(aliveStat)
alVar = StringVar()
alVar.set("Days Alive: " + aliveStat)
allbl = Label(animalStatPanel, textvariable = alVar, bg = 'yellowgreen', fg = 'white')
allbl.pack()
happyStat = int(5)
happyStat = str(happyStat)
hapVar = StringVar()
hapVar.set("Happiness: " + happyStat)
haplbl = Label(animalStatPanel, textvariable = hapVar, bg = 'yellowgreen', fg = 'white')
haplbl.pack()
global greetText
greetText = StringVar()
greetText.set("Hello " + readname + ", how are you today?")
global greetlbl
greetlbl = Label(mainWin, textvariable = greetText, bg = 'yellowgreen', fg = 'white')
greetlbl.pack(pady = 10)
animallbl = Label(mainWin, image = animalPic)
animallbl.pack(side = BOTTOM)
mainWin.after(1000, checkPill)
mainWin.mainloop()
