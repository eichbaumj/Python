from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import askopenfilename
import hashlib
import itertools
import time

version = "v1.2"

def getGesture():
    fname = askopenfilename(filetypes=(("Gesture files", "*.key"), ("All files", "*.*")))
    if fname:
        hexlist = []
        f = open(fname, 'rb')
        file = f.read()
        f.close()
        for h in file:
            a = (hex(h).replace('0x', ''))
            if len(a) == 1:
                a = ('0' + a)
            hexlist.append(a)
        hexstring = ''.join(hexlist)
        sha1val.set(hexstring)
        return


def updateLegend(number):    
    if number == "0":
        poslabel0 = Label(app, textvariable=pos0, fg = "green", bg = "black", justify = CENTER, font=("Calibri", 14))
        poslabel0.place(x=175,y=20)
    elif number == "1":
        poslabel1 = Label(app, textvariable=pos1, fg = "green", bg = "black", justify = CENTER, font=("Calibri", 14))
        poslabel1.place(x=199,y=20)
    elif number == "2":
        poslabel2 = Label(app, textvariable=pos2, fg = "green", bg = "black", justify = CENTER, font=("Calibri", 14))
        poslabel2.place(x=223,y=20)      
    elif number == "3":
        poslabel3 = Label(app, textvariable=pos3, fg = "green", bg = "black", justify = CENTER, font=("Calibri", 14))
        poslabel3.place(x=175,y=49)        
    elif number == "4":
        poslabel4 = Label(app, textvariable=pos4, fg = "green", bg = "black", justify = CENTER, font=("Calibri", 14))
        poslabel4.place(x=199,y=49)        
    elif number == "5":
        poslabel5 = Label(app, textvariable=pos5, fg = "green", bg = "black", justify = CENTER, font=("Calibri", 14))
        poslabel5.place(x=223,y=49)        
    elif number == "6":
        poslabel6 = Label(app, textvariable=pos6, fg = "green", bg = "black", justify = CENTER, font=("Calibri", 14))
        poslabel6.place(x=175,y=78)        
    elif number == "7":
        poslabel7 = Label(app, textvariable=pos7, fg = "green", bg = "black", justify = CENTER, font=("Calibri", 14))
        poslabel7.place(x=199,y=78)        
    elif number == "8":
        poslabel8 = Label(app, textvariable=pos8, fg = "green", bg = "black", justify = CENTER, font=("Calibri", 14))
        poslabel8.place(x=223,y=78)
    app.update()
    time.sleep(.75)
    return
            
def decodePattern(sha1):
    combined = ""
    options = [0,1,2,3,4,5,6,7,8]
    for l in range(4,len(options)+1):
        for subset in itertools.permutations(options, l):
            for i in subset:
                combined += str(i)
            hashvalue = hashit(convertHex(combined))
            if sha1 == hashvalue:
                for number in combined:
                    updateLegend(number)
                return combined
            combined = ""
    return False
            
def convertHex(pattern):
	hexpattern = b""
	for number in pattern:
		if number == "0":
			hexval = b'\x00'
		if number == "1":
			hexval = b'\x01'
		if number == "2":
			hexval = b'\x02'
		if number == "3":
			hexval = b'\x03'
		if number == "4":
			hexval = b'\x04'
		if number == "5":
			hexval = b'\x05'
		if number == "6":
			hexval = b'\x06'
		if number == "7":
			hexval = b'\x07'
		if number == "8":
			hexval = b'\x08'
		hexpattern += hexval
	return hexpattern

def hashit(pattern):
	sha1 = hashlib.sha1(pattern).hexdigest()
	return sha1

def decodeSha1():
    if storedsha1.get():
        clearLegend()
        gesture = decodePattern(storedsha1.get().lower())
        if gesture:
            formatted = '->'.join(gesture)
            pattern.set(formatted)
        else:
            pattern.set("Pattern not found")
    return

def clear():
    storedsha1.delete(0,END)
    pattern.set("Enter SHA1 Value into the Field Below")
    clearLegend()
    return

def clearLegend():    
    pos0 = StringVar()
    pos0.set(" 0 ")
    poslabel0 = Label(app, textvariable=pos0, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
    poslabel0.place(x=175,y=20)

    pos1 = StringVar()
    pos1.set(" 1 ")
    poslabel1 = Label(app, textvariable=pos1, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
    poslabel1.place(x=199,y=20)

    pos2 = StringVar()
    pos2.set(" 2 ")
    poslabel2 = Label(app, textvariable=pos2, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
    poslabel2.place(x=223,y=20)

    pos3 = StringVar()
    pos3.set(" 3 ")
    poslabel3 = Label(app, textvariable=pos3, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
    poslabel3.place(x=175,y=49)

    pos4 = StringVar()
    pos4.set(" 4 ")
    poslabel4 = Label(app, textvariable=pos4, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
    poslabel4.place(x=199,y=49)

    pos5 = StringVar()
    pos5.set(" 5 ")
    poslabel5 = Label(app, textvariable=pos5, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
    poslabel5.place(x=223,y=49)

    pos6 = StringVar()
    pos6.set(" 6 ")
    poslabel6 = Label(app, textvariable=pos6, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
    poslabel6.place(x=175,y=78)

    pos7 = StringVar()
    pos7.set(" 7 ")
    poslabel7 = Label(app, textvariable=pos7, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
    poslabel7.place(x=199,y=78)

    pos8 = StringVar()
    pos8.set(" 8 ")
    poslabel8 = Label(app, textvariable=pos8, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
    poslabel8.place(x=223,y=78)
    return

def aboutMe():
    tkinter.messagebox.showinfo(title="About", message=("Android Gesture Pattern Decoder " + version +  "\nBy James Eichbaum\nCopyright 2013"))
    return

app = Tk()
app.title("Gesture Decoder")
app.geometry('400x250+400+200')

#Menu Bar
menubar = Menu(app)

#File Menu
filemenu = Menu(menubar,tearoff=0)
filemenu.add_command(label = "Open", command = getGesture)
filemenu.add_command(label = "Quit", command=app.quit)
menubar.add_cascade(label = "File", menu=filemenu)


#Help Menu
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_cascade(label="About", command=aboutMe)
menubar.add_cascade(label="Help", menu=helpmenu)

app.config(menu=menubar)



#Pring Legend
pos0 = StringVar()
pos0.set(" 0 ")
poslabel0 = Label(app, textvariable=pos0, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
poslabel0.place(x=175,y=20)

pos1 = StringVar()
pos1.set(" 1 ")
poslabel1 = Label(app, textvariable=pos1, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
poslabel1.place(x=199,y=20)

pos2 = StringVar()
pos2.set(" 2 ")
poslabel2 = Label(app, textvariable=pos2, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
poslabel2.place(x=223,y=20)

pos3 = StringVar()
pos3.set(" 3 ")
poslabel3 = Label(app, textvariable=pos3, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
poslabel3.place(x=175,y=49)

pos4 = StringVar()
pos4.set(" 4 ")
poslabel4 = Label(app, textvariable=pos4, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
poslabel4.place(x=199,y=49)

pos5 = StringVar()
pos5.set(" 5 ")
poslabel5 = Label(app, textvariable=pos5, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
poslabel5.place(x=223,y=49)

pos6 = StringVar()
pos6.set(" 6 ")
poslabel6 = Label(app, textvariable=pos6, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
poslabel6.place(x=175,y=78)

pos7 = StringVar()
pos7.set(" 7 ")
poslabel7 = Label(app, textvariable=pos7, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
poslabel7.place(x=199,y=78)

pos8 = StringVar()
pos8.set(" 8 ")
poslabel8 = Label(app, textvariable=pos8, fg = "white", bg = "black", justify = CENTER, font=("Calibri", 14))
poslabel8.place(x=223,y=78)

#Prompt: Enter SHA1 Value:
prompt = StringVar()
prompt.set("Enter SHA1 Value:")
uprompt = Label(app, textvariable=prompt, height = 2,)
uprompt.place(x=15,y=170)

#Entry Box for SHA1 Value
sha1val = StringVar()
storedsha1 = Entry(app, textvariable=sha1val, width=42)
storedsha1.place(x=125,y=180)

#Label: Gesture Pattern:
patlabel = StringVar()
patlabel.set("Gesture Pattern:")
label02 = Label(app,textvariable=patlabel, height = 2)
label02.place(x=15,y=140)

#Result: Decoded Gesture Pattern in Blue
pattern = StringVar()
pattern.set("Enter SHA1 Value Below and Click Decode")
label01 = Label(app, textvariable=pattern, fg = "blue")
label01.place(x=125,y=148)

#Decode Button
decode = Button(app, text="Decode", width=10, command=decodeSha1)
decode.place(x=145, y=210)

#Clear Button
clear = Button(app, text="Clear", width = 10, command=clear)
clear.place(x=245,y=210)

#Browse Button
browsebutton = Button(app, text = "Browse", command = getGesture, width = 10)
browsebutton.place(x=15,y=210)

#Version
ver = StringVar()
ver.set(version)
verlabel = Label(app,textvariable = ver, fg = 'red', height = 2)
verlabel.place(x = 370, y = 220)

app.mainloop()
