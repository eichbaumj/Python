from tkinter import *
import tkinter.messagebox

#need to set initial state that will change with each press of the 3 buttons
state = 1  # 1 = VarInt 2 = Integer 3 = Length

def selection(state):
    if state == 1:
        varint.configure(fg = 'red')
        integer.configure(fg = 'blue')
        length.configure(fg = 'blue')
    elif state == 2:
        varint.configure(fg = 'blue')
        integer.configure(fg = 'red')
        length.configure(fg = 'blue')
    elif state == 3:
        varint.configure(fg = 'blue')
        integer.configure(fg = 'blue')
        length.configure(fg = 'red')
    return
        
def clear():
    storedvalue.delete(0, END)
    return


def varint():
    global state
    if state == 1:
        pass
    if state == 2:
        pass ##This is where goto convert int to varint would be
    if state == 3:
        pass ##This would have two functions - convert string to int,and then convert int to varint
    state = 1
    selection(state)
    return

def integer():
    global state
    if state == 3:
        string_to_integer()
    elif state == 2:
        pass
    elif state == 1:
        varint_to_int()
    
    state = 2
    selection(state)
    return

def length():
    global state
    if state == 2:
        getlength()
    elif state == 3:
        pass
    elif state == 1:
        varint_to_int()
        getlength()
    else:
        storedvalue.delete(0, END)
    state = 3
    selection(state)
    return
    
def aboutMe():
    tkinter.messagebox.showinfo(title="About", message="VarInt Calculator 2.0\nBy James Eichbaum\nMicro Systemation\nCopyright 2014")
    return

def string_to_integer():
    if storedvalue.get():
        try:
            string = int(storedvalue.get())
            #print(string)
            integer = (string * 2) + 13
            storedvalue.delete(0, END)
            storedvalue.insert(0, integer)
        except ValueError:
            storedvalue.delete(0, END)
            storedvalue.insert(0, "Error: Invalid Length Value")
    else:
        storedvalue.delete(0, END)
    return

def getlength():
    if storedvalue.get():
        try:
            integer = int(storedvalue.get())
            #print(integer)
            if integer >= 12:
                if integer % 2:
                    #Data is a String
                    integer = (integer - 13) // 2
                else:
                    #Data is a BLOB
                    integer = (integer - 12) // 2
                storedvalue.delete(0, END)
                storedvalue.insert(0, integer)
            else:
                storedvalue.delete(0, END)
        except ValueError:
            storedvalue.delete(0, END)
            storedvalue.insert(0, "Error: Invalid Integer")
    return
                
def varint_to_int():
    if storedvalue.get():
        try:
            hexinput = storedvalue.get()
            hexinput = bytes.fromhex(hexinput)
            numofvalues = len(hexinput)
            this = 0
            last = (hexinput[numofvalues - 1] << 1)
            count = 2
            leftshift = 8
            while (numofvalues - count) >= 0:
                this = ((((hexinput[numofvalues - count] << 1) & 0xFF) >> 1) << leftshift)
                last = (this | last)
                count += 1
                leftshift += 7
            #print ((last >> 1))
            storedvalue.delete(0,END)
            storedvalue.insert(0, (last >> 1))                     
        except ValueError:
            storedvalue.delete(0, END)
            storedvalue.insert(0, "Error: Invalid Hex Value")
    else:
        pass
    return

############################################################
#Number Buttons
def button0():
    storedvalue.insert(END, "0")
    return

def button1():
    storedvalue.insert(END, "1")
    return

def button2():
    storedvalue.insert(END, "2")
    return

def button3():
    storedvalue.insert(END, "3")
    return

def button4():
    storedvalue.insert(END, "4")
    return

def button5():
    storedvalue.insert(END, "5")
    return

def button6():
    storedvalue.insert(END, "6")
    return

def button7():
    storedvalue.insert(END, "7")
    return

def button8():
    storedvalue.insert(END, "8")
    return

def button9():
    storedvalue.insert(END, "9")
    return

def buttonA():
    storedvalue.insert(END, "A")
    return

def buttonB():
    storedvalue.insert(END, "B")
    return

def buttonC():
    storedvalue.insert(END, "C")
    return

def buttonD():
    storedvalue.insert(END, "D")
    return

def buttonE():
    storedvalue.insert(END, "E")
    return

def buttonF():
    storedvalue.insert(END, "F")
    return


############################################################

#Create Window
app = Tk()
app.title("VarInt Calculator")
app.geometry('220x190+500+200')

#Menu Bar
menubar = Menu(app)

#File Menu
filemenu = Menu(menubar,tearoff=0)
filemenu.add_command(label = "Quit", command=app.quit)
menubar.add_cascade(label = "File", menu=filemenu)

#Edit Menu
editmenu = Menu(menubar, tearoff=0)
editmenu.add_cascade(label="Copy", command=None)
editmenu.add_cascade(label="Paste", command=None)
menubar.add_cascade(label="Edit", menu=editmenu)

#Help Menu
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_cascade(label="About", command=aboutMe)
menubar.add_cascade(label="Help", menu=helpmenu)
app.config(menu=menubar)

############################################################

#Input window
value = StringVar(None)
storedvalue = Entry(app, width = 34, justify = RIGHT, textvariable=value)
storedvalue.place(x = 5, y = 5)

#VarInt Button
varint = Button(app, text="VarInt", fg = 'red', width=5,command=varint)
varint.place(x = 60, y =35)

#Integer Button
integer = Button(app, text="Integer", fg = 'blue', width=5,command=integer)
integer.place(x = 112, y =35)

#String Button
length = Button(app, text="Length", fg = 'blue', width=5,command=length)
length.place(x = 167, y =35)

#Clear Button
clear = Button(app, text="Clear", width = 5, command = clear)
clear.place(x = 7, y = 35)

#A Button
a = Button(app, text="A", fg = 'brown', width=5,command=buttonA)
a.place(x = 7, y =65)

#1 Button
button1 = Button(app, text="1", width=5,command=button1)
button1.place(x = 60, y =65)

#4 Button
button4 = Button(app, text="4", width=5,command=button4)
button4.place(x = 60, y =95)

#7 Button
button7 = Button(app, text="7", width=5,command=button7)
button7.place(x = 60, y =125)

#E Button
buttonE = Button(app, text="E", fg = 'brown', width=5,command=buttonE)
buttonE.place(x = 60, y =155)

#2 Button
button2 = Button(app, text="2", width=5,command=button2)
button2.place(x = 112, y =65)

#5 Button
button5 = Button(app, text="5", width=5,command=button5)
button5.place(x = 112, y =95)

#8 Button
button8 = Button(app, text="8", width=5,command=button8)
button8.place(x = 112, y =125)

#F Button
buttonF = Button(app, text="F", fg = 'brown', width=5,command=buttonF)
buttonF.place(x = 112, y =155)

#3 Button
button3 = Button(app, text="3", width=5,command=button3)
button3.place(x = 167, y =65)

#6 Button
button6 = Button(app, text="6", width=5,command=button6)
button6.place(x = 167, y =95)

#9 Button
button9 = Button(app, text="9", width=5,command=button9)
button9.place(x = 167, y =125)

#0 Button
button0 = Button(app, text="0", width=5,command=button0)
button0.place(x = 167, y =155)

#B Button
b = Button(app, text="B", fg = 'brown', width=5,command=buttonB)
b.place(x = 7, y =95)

#C Button
c = Button(app, text="C", fg = 'brown', width=5,command=buttonC)
c.place(x = 7, y =125)

#D Button
d = Button(app, text="D", fg = 'brown', width=5,command=buttonD)
d.place(x = 7, y =155)


##################################################################

#Main Loop
app.mainloop()

