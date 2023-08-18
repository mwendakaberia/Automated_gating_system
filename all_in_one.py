from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
import tensorflow as tf
import keras
import numpy as np
import cv2
import pytesseract
import mysql.connector

conn=mysql.connector.connect(host="localhost",database="school_project",user="root",password="")


def select_file():
    location=filedialog.askopenfilename(initialdir="/",title="select file",
                                       filetype=(("jpeg","*.jpg",".png"),("All Files","*.*")))

    label.config(text="This is the image selected")
    root.config(bg="cyan")
    label1.config(text="")
    img=Image.open(location)
    img2=img.resize((300,250))
    canvas.image=ImageTk.PhotoImage(img2)
    canvas.create_image(0,0,image=canvas.image,anchor="nw")

    global loc
    loc = location


def recognise():
    car_person_recognition()


def car_person_recognition():
    model = keras.models.load_model('car_person_model.h5')

    height = 180
    width = 180

    class_names = ['cars', 'people']

    img = keras.preprocessing.image.load_img(loc, target_size=(height, width))
    img = keras.preprocessing.image.img_to_array(img)
    img = tf.expand_dims(img, 0)

    predictions = model.predict(img)
    score = tf.nn.softmax(predictions[0])
    name = class_names[np.argmax(score)]

    if (name == "cars"):
       plate_recognition()
       label1.config(text="The number plate is " + text1)
    else:
        face_recognition()
        label1.config(text=before1 + name1)


def plate_recognition():
    image = cv2.imread(loc)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 11, 30, 90)
    edges = cv2.Canny(blur, 90, 90)

    contours, new = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    image_copy = image.copy()
    _ = cv2.drawContours(image_copy, contours, -1, (0, 0, 255), 2)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]
    image_copy = image.copy()
    _ = cv2.drawContours(image_copy, contours, -1, (0, 0, 255), 2)

    plate = None
    for c in contours:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(c)
            plate = image[y:y + h, x:x + w]
            break

    cv2.imwrite("plate.png", plate)

    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
    text = pytesseract.image_to_string(plate,config='--psm 3')
    print(text)
    text2 = str(text)
    global text1
    if len(text2) < 4:
        text1 = "Number plate not recognized"
    else:
        text1 = text2
        cursor=conn.cursor()
        #sql="select * from car_records where number_plate = %s"
        cursor.execute("select * from car_records where number_plate = %s", (text1,))
        result=cursor.fetchone()
        date2=str((datetime.now().strftime("%H:%M:%S")))
        if result:
            sql2 = "update car_records set departure_time=%s where  number_plate=%s"
            values = (date2,text1)
            cursor.execute(sql2, values)
            conn.commit()
        else:
            sql2 = "insert into car_records(number_plate,arrival_time) values(%s,%s)"
            values=(text1,date2)
            cursor.execute(sql2, values)
            conn.commit()
            print(cursor.lastrowid)


def face_recognition():
    height = 180
    width = 180

    class_names = ['Lecturer', 'Non_Teaching', 'Student']

    model = keras.models.load_model('face_model2.h5')

    img = keras.preprocessing.image.load_img(loc, target_size=(height, width))
    img = keras.preprocessing.image.img_to_array(img)
    img = tf.expand_dims(img, 0)
    print(img.shape)

    predictions = model.predict(img)
    score = tf.nn.softmax(predictions[0])

    probability=100 * np.max(score)

    if probability>=80:
        name = class_names[np.argmax(score)]
        before="This image belongs to "
        label.config(text="This image belongs to " + name)
    else:
        name="unrecognised"
        before="This image is "

        root.config(bg="red")
        label.config(text="SECURITY ALERT!!!")

    global before1
    before1=before
    global name1
    name1=name

    print("This image most likely belongs to  {}  with a  {:.2f}  percent confidence."
          .format(class_names[np.argmax(score)], 100 * np.max(score)))

def car_data():
    cursor=conn.cursor()
    cursor.execute("select * from car_records")
    result=cursor.fetchall()
    table=tk.Toplevel(root, width=500, height=500)
    table.minsize(400, 500)
    table.title("Car Records")
    i=0
    for row in result:
        for item in range(len(row)):
            e=Entry(table,width=10,fg="blue")
            e.grid(row=i,column=item)
            data=row[item]
            if data:
                e.insert(END, data)
        i=i+1


def loginPage():
    loginlevel = tk.Toplevel(root, width=500, height=500)
    loginlevel.title("Login Page")
    loginlevel.minsize(400, 400)
    labeltop = ttk.Label(loginlevel)
    labeltop.config(foreground="red", text="Please provide your details", font=("Helvatical bold", 25))
    labeltop.place(x=50, y=10)
    namelabel = ttk.Label(loginlevel)
    namelabel.config(background="black", foreground="cyan", text="Username")
    namelabel.place(x=20, y=70)
    username = Entry(loginlevel)
    username.place(x=20, y=90)
    passwordlabel = ttk.Label(loginlevel)
    passwordlabel.config(background="black", foreground="cyan", text="Password")
    passwordlabel.place(x=20, y=130)
    password = Entry(loginlevel, show="*")
    password.place(x=20, y=150)

    def loginver():
        cursor = conn.cursor()
        sql2 = "select * from user where Username=%s and Password=%s"
        values=(username.get(),password.get())
        cursor.execute(sql2, values)
        result=cursor.fetchone()

        if result:
            car_data()
            loginlevel.destroy()
        else:
            sym=messagebox.askokcancel("Error!!","Wrong credentials,Please check again and retry")
            if sym:
                loginlevel.mainloop()


    login = Button(loginlevel, text="Login", bg="green", font=("Helvatical bold", 25),
                   command=loginver)
    login.place(x=70, y=200)
    loginlevel.mainloop()


root=tk.Tk()
root.title("My image")
root.minsize(700,700)
root.config(bg="lightblue",width=700,height=700)
label5=ttk.Label(root,text="MMUST Automated Gating System")
labelFont5 = ('times',50,'bold')
label5.configure(font=labelFont5,foreground="red")
label5.pack(pady=10,expand=1)
label=ttk.Label(root,text="Select the image you want")
labelFont = ('times',40,'bold')
label.configure(font=labelFont,background="black",foreground="cyan")
label.pack(pady=60,expand=1)
canvas = Canvas(root,bg="aliceblue",height=250,width=300)
canvas.pack(pady=20,expand=1)
frame = ttk.LabelFrame(root,text="What would you like to do")
frame.pack()
button = Button(frame,text="Select image",command=select_file,bg="green")
button.grid(column=0,row=0)
button = Button(frame,text="Recognise",command=recognise,bg="green")
button.grid(column=1,row=0)
label1=ttk.Label(frame,text="")
label1.grid(column=1,row=1)
btn_admin=Button(root,text="ADMIN",command=loginPage,bg="green")
btn_admin.place(x=0,y=0)
root.mainloop()