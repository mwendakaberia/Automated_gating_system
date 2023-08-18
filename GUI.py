import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from PIL import ImageTk,Image


def select_file():
    location=filedialog.askopenfilename(initialdir="/",title="select file",
                                       filetype=(("jpeg","*.jpg",".png"),("All Files","*.*")))

    label.config(text="This is the image selected")
    img=Image.open(location)
    canvas.image=ImageTk.PhotoImage(img)
    canvas.create_image(0,0,image=canvas.image,anchor="nw")

    global loc
    loc = location

# def recognise():
#     #import car_person_recognition
#     car_person_recognition.path=loc


root=tk.Tk()
root.title("My image")
root.minsize(400,500)
root.config(bg="cyan")
label=ttk.Label(root,text="Select the image you want")
labelFont = ('times',40,'bold')
label.configure(font=labelFont,background="black",foreground="cyan")
label.pack(expand=1)
canvas = Canvas(root,bg="aliceblue",height=250,width=300)
canvas.pack(expand=YES,fill=BOTH)
frame = ttk.LabelFrame(root,text="What would you like to do")
frame.pack(expand=1)
button = ttk.Button(frame,text="Select image",command=select_file)
button.grid(column=0,row=0)
button = ttk.Button(frame,text="Recognise")
button.grid(column=1,row=0)
label1=ttk.Label(frame,text="")
label1.grid(column=1,row=1)
root.mainloop()