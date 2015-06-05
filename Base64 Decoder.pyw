from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import asksaveasfilename
import base64
import os

user = os.getlogin()
version = "v1.0"

def decodeBase64():
    data = encoded.get("1.0", END)
    filename = asksaveasfilename(initialdir = 'C:/Users/'+user+'/Desktop')
    try:
        with open(r'{}'.format(filename), 'wb') as file:
            file.write(base64.standard_b64decode(data))
    except:
        pass
    return

def aboutMe():
    tkinter.messagebox.showinfo(title="About", message=("Base64 Decoder " + version +  "\nBy James Eichbaum\nCopyright 2015"))
    return

app = Tk()
app.title("Base64 Decoder")
width = app.winfo_screenwidth()
height = app.winfo_screenheight()
app.geometry('400x250+400+200')
app.geometry('{}x{}+{}+{}'.format(400,250,int(width/2)-200,int(height/2)-125))

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

#Prompt for Data
entryBox = StringVar()
entryBox.set("Paste encoded base64 data below")
label01 = Label(app, textvariable=entryBox, fg = "blue")
label01.place(x=105,y=10)

#Text Box to Paste Data
encodedData = StringVar()
encoded = Text(app, width = 47, height = 10)
encoded.place(x = 10, y = 40)

#Decode Button
decode = Button(app, text = "Decode", width = 10, command = decodeBase64)
decode.place(x = 160, y = 215)

app.mainloop()
