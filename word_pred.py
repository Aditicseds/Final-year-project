import cv2
import numpy as np
import os
import tkinter as tk
from PIL import Image, ImageTk
from keras.models import load_model
from cvzone.HandTrackingModule import HandDetector

OFFSET = 20
IMG_SIZE = 400
MODEL_PATH = "word_prediction_model.h5"
DATASET_PATH = "Predefined"

detector = HandDetector(maxHands=1)

class Application:

    def __init__(self):

        self.vs = cv2.VideoCapture(0)

        self.model = load_model(MODEL_PATH)
        print("Model loaded")

        self.labels = sorted(os.listdir(DATASET_PATH))
        print("Labels:", self.labels)

        self.root = tk.Tk()
        self.root.title("Sign Language Word Prediction")
        self.root.geometry("1200x700")

        title = tk.Label(self.root,text="Sign Language Word Prediction",
                         font=("Arial",25,"bold"))
        title.pack()

        self.panel = tk.Label(self.root)
        self.panel.place(x=50,y=80,width=500,height=400)

        self.panel2 = tk.Label(self.root)
        self.panel2.place(x=650,y=80,width=400,height=400)

        self.word_label = tk.Label(self.root,text="Prediction:",
                                   font=("Arial",22,"bold"))
        self.word_label.place(x=450,y=520)

        self.output = tk.Label(self.root,text="",
                               font=("Arial",28))
        self.output.place(x=450,y=580)

        self.video_loop()

        self.root.mainloop()


    def video_loop(self):

        ret, frame = self.vs.read()

        frame = cv2.flip(frame,1)

        hands,_ = detector.findHands(frame)

        white = np.ones((IMG_SIZE,IMG_SIZE,3),np.uint8)*255

        if hands:

            hand = hands[0]
            x,y,w,h = hand['bbox']

            crop = frame[y-OFFSET:y+h+OFFSET,x-OFFSET:x+w+OFFSET]

            if crop.size != 0:

                crop = cv2.resize(crop,(64,64))

                img = crop/255.0

                img = img.reshape(1,64,64,3)

                pred = self.model.predict(img)

                index = np.argmax(pred)

                word = self.labels[index]

                self.output.config(text=word)

            lm = hand['lmList']

            for i in range(0,4):
                cv2.line(white,(lm[i][0],lm[i][1]),
                         (lm[i+1][0],lm[i+1][1]),(0,255,0),3)

            for i in range(5,8):
                cv2.line(white,(lm[i][0],lm[i][1]),
                         (lm[i+1][0],lm[i+1][1]),(0,255,0),3)

            for i in range(9,12):
                cv2.line(white,(lm[i][0],lm[i][1]),
                         (lm[i+1][0],lm[i+1][1]),(0,255,0),3)

            for i in range(13,16):
                cv2.line(white,(lm[i][0],lm[i][1]),
                         (lm[i+1][0],lm[i+1][1]),(0,255,0),3)

            for i in range(17,20):
                cv2.line(white,(lm[i][0],lm[i][1]),
                         (lm[i+1][0],lm[i+1][1]),(0,255,0),3)

            for point in lm:
                cv2.circle(white,(point[0],point[1]),4,(0,0,255),-1)

        img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)

        self.panel.imgtk = imgtk
        self.panel.config(image=imgtk)

        white = cv2.cvtColor(white,cv2.COLOR_BGR2RGB)
        white = Image.fromarray(white)
        imgtk2 = ImageTk.PhotoImage(image=white)

        self.panel2.imgtk = imgtk2
        self.panel2.config(image=imgtk2)

        self.root.after(10,self.video_loop)


Application()