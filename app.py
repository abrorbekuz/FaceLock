import cv2; import time; import os
import mediapipe as mp; import numpy as np
import calendar; from PIL import ImageTk, Image
import face_recognition as fr; import datetime
import shutil
from tkinter import Tk, PhotoImage, Label, Button, messagebox, PanedWindow, Entry

form = Tk()

dark = "#000000"; white = "#FFFFFF"; gray = "#666666"

wt = form.winfo_screenwidth() + 5; ht = form.winfo_screenheight()
form.attributes("-fullscreen", 1); #form.iconbitmap(dir)
form.overrideredirect(True); form.resizable(False, False)
form.config(bg = dark); form.wm_attributes("-topmost", 1)

cap = cv2.VideoCapture(0)
mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection(0.75)

def modewrite(mode):
    file = open('mode.bpl', 'w+')
    file.write(mode); file.close()
    os.startfile('zipio.py')
    time.sleep(0.4)

modewrite('read')

onImg = PhotoImage(file = r"data/swon.png")
offImg = PhotoImage(file = r"data/swoff.png")
submit = PhotoImage(file = r"data/submit.png")
retryer = PhotoImage(file = r"data/retry.png")
user_bc = PhotoImage(file = r"data/user.png")

def hideunhide(a):
    d = {}
    for c in (65, 97):
        for i in range(26):
            d[chr(i+c)] = chr((i+13) % 26 + c)
    return "".join([d.get(c, c) for c in a])

file = open('data/conf.ini')
data = file.readlines(); file.close()

name, password = [i.replace('\n', '') for i in data][:2]
name, password = hideunhide(name), hideunhide(password)
user_welcome = f"hello {name}"

mode = "register" if not os.path.exists("data/admin.png") else "login"
btnState, panda, detected = False, True, False

def onHover(onhover, widget):
    onhover.bind("<Enter>", func = lambda i: widget.config(bg = white))
    onhover.bind("<Leave>", func = lambda i: widget.config(bg = gray))

def joke():
    messagebox.showinfo("XD", "Bu usulni bobomning bobosi ham biladi )")

def switch():
    global btnState
    
    if btnState:
        form.config(bg = dark)
        btn.config(image = onImg, bg = dark, activebackground = dark)
        txt.config(bg = dark, fg = white)
        if mode == "register":
            okbutton.config(bg = dark); retrybtn.config(bg = dark)
        btnState = False
    else:
        form.config(bg = white)
        btn.config(image = offImg, bg = white, activebackground = white)
        txt.config(bg = white, fg = dark)
        if mode == "register":
            okbutton.config(bg = white); retrybtn.config(bg = white)
        btnState = True

def forceexit():
    modewrite('write')

def pandatru():
    global panda
    if panda == True:
        panda = False
    else:
        panda = True

def save():
    modewrite('write')
    shutil.copy("add.png", "data/admin.png")
    os.remove("add.png")
    time.sleep(2)
    exit()

def retry():
    global panda
    okbutton["image"], retrybtn["image"] = "", ""
    panda = True

txt = Label(form, text = "Light mode", font = "Bahnschrift 20", bg = dark, fg = white)
txt.place(x = 30, y = ht - 65)

btn = Button(form, text = "OFF", command = switch, borderwidth = 0, bg = dark, activebackground = dark, image = onImg)
btn.place(x = wt - 60, y = ht - 40, anchor = "center")

face = Button(form, text = "Face", bg = dark, bd = 0, highlightthickness = 0)
face.place(relx = 0.5, rely = 0.5, anchor = "center")

if mode == "register":
    okbutton = Button(form, text = "", command = save, borderwidth = 0, bg = dark, activebackground = dark)
    okbutton.place(x = 180, y = ht - 43, anchor = "center")
    retrybtn = Button(form, text = "", borderwidth = 0, command = retry, bg = dark, activebackground = dark)
    retrybtn.place(x = 480, y = ht - 43, anchor = "center")

if mode == "login":
    panel = PanedWindow(bg = gray, border = 2)
    edit = Entry(bd = 0, bg = "#FFFFFF", font = "Bahnschrift 20")
    button = Button(text = "→", font = "Arial 20", bd = 0, bg = "#333333", command = onHover(edit, panel))
    panel.add(edit); panel.add(button);
    panel.place(relx = 0.5 , rely = 0.6, anchor = "center")

def heisornot(img):
    txt.place(y = ht - 65)
    image = fr.load_image_file("data/admin.png")
    image_encoding = fr.face_encodings(image)[0]
    unknow_encoding = fr.face_encodings(img)[0]
    results = fr.compare_faces([image_encoding], unknow_encoding)
    if results[0]:
        return True
    else:
        return False

def getdate():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    txt.place(y = ht - 80)
    date = "{}:{}                     \n{}, {} {}".format(now.hour, now.minute, 
    calendar.day_name[my_date.weekday()], now.day, 
    calendar.month_name[now.month])

    return date

def circular_image(img, mode):
    global btnState
    raw_shape = img.shape
    raw = np.zeros(raw_shape, dtype = "uint8")
    radius = (raw_shape[0] + raw_shape[1]) // 4
    if btnState != True:
        raw = cv2.circle(raw, (raw_shape[0] // 2, raw_shape[1] // 2),
                            radius, (255, 255, 255), -1)
        img = cv2.bitwise_and(img, raw)
    else:
        raw = cv2.circle(raw, (raw_shape[0] // 2, raw_shape[1] // 2), radius, (255, 255, 255), -1)
        grayed = cv2.cvtColor(raw, cv2.COLOR_RGB2GRAY)
        _, inver = cv2.threshold(grayed, 50, 255, cv2.THRESH_BINARY_INV)
        raw = cv2.cvtColor(inver, cv2.COLOR_GRAY2RGB)

        img = cv2.bitwise_or(img, raw)
    return img

def main():
    global mode; global panda; global detected
    boob = ""; a = detected
    _, img = cap.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(img)
    if results.detections:
        for id, detection in enumerate(results.detections):
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                   int(bboxC.width * iw), int(bboxC.height * ih)
            
            h, w, h1, w1 = bbox
            sc = img[w:w + w1, h:h + h1]
            if detected == False:
                sc = cv2.resize(sc, (200, 200))

            if mode == "register":
                face.place(relx = 0.5, rely = 0.5, anchor = "center")
                txt["text"] = "Detecting..."
                okbutton["image"], retrybtn["image"] = "", ""
                imgs = ImageTk.PhotoImage(Image.fromarray(img))
                if panda:
                    if int(detection.score[0] * 100) >= 96:
                        some = cv2.cvtColor(sc, cv2.COLOR_BGR2RGB)
                        cv2.imwrite("add.png", some)
                        boob = ImageTk.PhotoImage(Image.fromarray(sc))
                        panda = False

                    if boob == "":
                        face["image"] = imgs
                else:
                    admin = PhotoImage(file = r"add.png")
                    face["image"] = admin
                    okbutton["image"], retrybtn["image"] = submit, retryer
                    txt["text"] = "press                    to submit else "

                form.update()
                form.protocol("WM_DELETE_WINDOW", forceexit)
            else:
                if detected == False:
                    face.place(relx = 0.5, rely = 0.3, anchor = "center")
                    if panda == False:
                        if int(detection.score[0] * 100) >= 95:
                            a = heisornot(sc)

                        if a == True:
                            txt["text"] = user_welcome
                            panel.destroy(); face.destroy()
                            detected = True
                        else:
                            imgs = ImageTk.PhotoImage(Image.fromarray(circular_image(sc, mode)))
                            face["image"] = imgs
                            txt["text"] = "you are not admin"
                    else:
                        face["image"] = user_bc
                        face["command"] = pandatru
                        txt["text"] = getdate()
                        trypass = str(edit.get())
                        if trypass == password:
                            txt["text"] = user_welcome
                            panel.destroy(); face.destroy()
                            detected = True
                else:
                    modewrite('write')
                    time.sleep(2)
                    exit()

                form.update()
                form.protocol("WM_DELETE_WINDOW", joke)

try:
    while True:
        main()
except Exception as e:
    pass