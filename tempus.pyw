from tkinter import *
import tkinter.messagebox
import datetime
import struct

version = ("v1.5")


def little(value):
    """
    The function, little(), will convert a hex string entered by
    the user and convert it to little endian.
    """
        
    string = []
    if len(value)%2 != 0:
        string.append("0")
    for i in value:
        string.append(i)
    length = len(string)
    count = length - 2
    newstring = []
    while count >= 0:
        hex_split = [string[count],string[count+1]]
        hex_combined = "".join(hex_split)
        newstring.append(hex_combined)
        count -=2
    newstring = "".join(newstring)
    return newstring

def brewTime(secs, adjustment):
    """
    Accounts for the 10 years and 5 day difference for Unix Time.
    Also accounts for the 2 leap years that exist within those 10 years.
    Use calendar module to check. calendar.leapdays(1970,1980)
    """
    brewtime = datetime.datetime.utcfromtimestamp(secs+315964800+adjustment)
    return brewtime

def unixTime(secs, adjustment):
    unixtime = datetime.datetime.utcfromtimestamp(secs+adjustment)
    return unixtime

def unixmilTime(secs,adjustment):
    """
    Divides the number of seconds by 1000 to obtain unix time.
    """
    unixtime = datetime.datetime.utcfromtimestamp((secs/1000) + adjustment)
    return unixtime

def MACTime(secs,adjustment):
    """
    Accounts for 31 year difference from Unix Time. Also accounts for
    the 8 leap years in that 31 year timespan. Use calendar module to
    check. calendar.leapdays(1970,2001)
    """
    MACtime = datetime.datetime.utcfromtimestamp(secs+978307200+adjustment)
    return MACtime

def convertTime():
    adjustment = timeslider.get() * 3600
    if timeslider.get() >= 0:
        sign = "+"
    else:
        sign = ""
    if storedhex.get():
        if checkBoxVal.get():
            name = little(storedhex.get())
        elif checkBoxVal.get() == 0:
            try:
                name = storedhex.get()
            except ValueError:
                name = 0
        if checkBoxVal2.get():
            try:
                name = struct.unpack('>d', bytes.fromhex(name))[0]
            except ValueError:
                name = 0
        else:
            try:
                name = int(name, 16)
            #name += adjustment
            except ValueError:
                name = 0
    elif storedval.get():
        try:
            name = int(storedval.get())
            #name += adjustment
        except ValueError:
            name = 0
    else:
        name = 0
    try:
        unixtime = unixTime(float(name), adjustment)
        values = [unixtime.year, unixtime.month, unixtime.day, unixtime.hour, unixtime.minute, unixtime.second]
        niceunix = ("{0}-{1:02}-{2:02} {3:02}:{4:02}:{5:02}".format(*values))
    except ValueError:
        unixtime = "Invalid value"
        niceunix = "Invalid value"
    try:
        brewtime = brewTime(float(name), adjustment)
        values = [brewtime.year, brewtime.month, brewtime.day, brewtime.hour, brewtime.minute, brewtime.second]
        nicebrew = ("{0}-{1:02}-{2:02} {3:02}:{4:02}:{5:02}".format(*values))
    except ValueError:
        brewtime = "Invalid value"
        nicebrew = "Invalid value"
    try:
        mactime = MACTime(float(name), adjustment)
        values = [mactime.year, mactime.month, mactime.day, mactime.hour, mactime.minute, mactime.second]
        nicemac = ("{0}-{1:02}-{2:02} {3:02}:{4:02}:{5:02}".format(*values))
    except ValueError:
        mactime = "Invalid value"
        nicemac = "Invalid value"
    try:
        miltime = unixmilTime(float(name), adjustment)
        values = [miltime.year, miltime.month, miltime.day, miltime.hour, miltime.minute, miltime.second]
        nicemil = ("{0}-{1:02}-{2:02} {3:02}:{4:02}:{5:02}".format(*values))
    except ValueError:
        miltime = "Invalid value"
        nicemil = "Invalid value"
    MilTime.set(str(nicemil) + " {0}{1} UTC".format(sign, timeslider.get()))
    MACtext.set(str(nicemac) + " {0}{1} UTC".format(sign, timeslider.get()))
    BrewText.set(str(nicebrew) + " {0}{1} UTC".format(sign, timeslider.get()))
    UnixText.set(str(niceunix) + " {0}{1} UTC".format(sign, timeslider.get()))
    storedval.delete(0,END)
    storedhex.delete(0,END)
    return

def aboutMe():
    tkinter.messagebox.showinfo(title="About", message="Tempus Timestamp Converter v1.5\nBy James Eichbaum\nCopyright 2013")
    return

#Create Window
app = Tk()
app.title("Tempus")
app.geometry('425x250+400+200')

#Menu Bar
menubar = Menu(app)

#File Menu
filemenu = Menu(menubar,tearoff=0)
filemenu.add_command(label = "Quit", command=app.quit)
menubar.add_cascade(label = "File", menu=filemenu)

#Help Menu
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_cascade(label="About", command=aboutMe)
menubar.add_cascade(label="Help", menu=helpmenu)

app.config(menu=menubar)

#Labels
UnixText = StringVar()
UnixText.set("1970-01-01 00:00:00 +0 UTC")
label1 = Label(app, textvariable=UnixText,fg = 'blue', height=2)
label1.place(x = 170, y=5)

unix = StringVar()
unix.set("Unix Time:")
label01=Label(app, textvariable=unix,height=2)
label01.place(x=15, y=5)

MilTime = StringVar()
MilTime.set("1970-01-01 00:00:00 +0 UTC")
label4 = Label(app, textvariable=MilTime,fg = 'blue', height=2)
label4.place(x = 170, y = 40)

mil = StringVar()
mil.set("Unix Millisecond Time:")
label04 = Label(app, textvariable=mil, height=2)
label04.place(x = 15, y=40)

BrewText = StringVar()
BrewText.set("1980-01-06 00:00:00 +0 UTC")
label2 = Label(app, textvariable=BrewText,fg = 'blue', height=2)
label2.place(x = 170, y = 75)

brew = StringVar()
brew.set("BREW Time:")
label02 = Label(app, textvariable=brew, height=2)
label02.place(x=15, y=75)


MACtext = StringVar()
MACtext.set("2001-01-01 00:00:00 +0 UTC")
label3 = Label(app, textvariable=MACtext,fg = 'blue', height=2)
label3.place(x=170,y=110)

mac = StringVar()
mac.set("MAC Time:")
label03 = Label(app,textvariable=mac, height=2)
label03.place(x=15, y=110)

line = StringVar()
line.set("_______________________________________________________________________________")
linelabel = Label(app, textvariable=line, fg = 'grey', height = 1)
linelabel.place(x=15, y=135)

ver = StringVar()
ver.set(version)
verlabel = Label(app,textvariable = ver, fg = 'red', height = 2)
verlabel.place(x = 390, y = 220)

#Input Fields
#Decimal label
prompt = StringVar()
prompt.set("Enter Decimal Value:")
uprompt = Label(app, textvariable=prompt, height = 2)
uprompt.place(x = 15, y = 186)

timesecs = StringVar(None)
storedval = Entry(app, textvariable=timesecs)
storedval.place(x = 170, y = 195)

#Hex Label
hexprompt = StringVar()
hexprompt.set("Enter Hex Value:")
uhexprompt = Label(app, textvariable=hexprompt, height = 2)
uhexprompt.place(x = 15, y = 160)

timehex = StringVar(None)
storedhex = Entry(app, textvariable=timehex)
storedhex.place(x = 170, y = 169)

#Tick Box
checkBoxVal = IntVar()
checkBox1 = Checkbutton(app, variable=checkBoxVal, text="Little Endian")
checkBox1.place(x = 305, y=195)

checkBoxVal2 = IntVar()
checkBox2 = Checkbutton(app, variable=checkBoxVal2, text = "64 bit double")
checkBox2.place(x = 305, y = 165)


timezone = StringVar()
timezone.set("Offset:")
timelabel = Label(app, textvariable=timezone, height=2)
timelabel.place(x=336, y=5)

timescale = IntVar()
timeslider = Scale(app, from_=-12, to=12, orient=VERTICAL)
timeslider.place(x=375, y=5)


#Calculate Button
button1 = Button(app, text="Calculate", width=18,command=convertTime)
button1.place(x = 163, y =220)

#Main Loop
app.mainloop()
