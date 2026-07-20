# # Importing Libraries
# import threading
#
# import numpy as np
# import math
# import cv2
# import os, sys
# import traceback
# import pyttsx3
# from keras.models import load_model
# from cvzone.HandTrackingModule import HandDetector
# from string import ascii_uppercase
# import enchant
# ddd=enchant.Dict("en-US")
# hd = HandDetector(maxHands=1)
# hd2 = HandDetector(maxHands=1)
# import tkinter as tk
# from PIL import Image, ImageTk
#
# offset=29
#
#
# os.environ["THEANO_FLAGS"] = "device=cuda, assert_no_cpu_op=True"
#
#
# # Application :
#
# class Application:
#
#     def __init__(self):
#         self.vs = cv2.VideoCapture(0)
#         self.current_image = None
#         self.model = load_model('cnn8grps_rad1_model.h5')
#         self.speak_engine=pyttsx3.init()
#         self.speak_engine.setProperty("rate",100)
#         voices=self.speak_engine.getProperty("voices")
#         self.speak_engine.setProperty("voice",voices[0].id)
#
#         self.ct = {}
#         self.ct['blank'] = 0
#         self.blank_flag = 0
#         self.space_flag=False
#         self.next_flag=True
#         self.prev_char=""
#         self.count=-1
#         self.ten_prev_char=[]
#         for i in range(10):
#             self.ten_prev_char.append(" ")
#
#
#         for i in ascii_uppercase:
#             self.ct[i] = 0
#         print("Loaded model from disk")
#
#
#         self.root = tk.Tk()
#         self.root.title("Sign Language To Text Conversion")
#         self.root.protocol('WM_DELETE_WINDOW', self.destructor)
#         #############################################################################################
#         self.root.geometry("1300x750")
#
#         # Title
#         self.T = tk.Label(self.root, text="Sign Language To Text Conversion", font=("Courier", 24, "bold"))
#         self.T.place(x=240, y=10)
#
#         # Camera output
#         self.panel = tk.Label(self.root, bg="gray")
#         self.panel.place(x=60, y=60, width=500, height=350)
#
#         # Processed hand sign output
#         self.panel2 = tk.Label(self.root, bg="lightgray")
#         self.panel2.place(x=700, y=60, width=400, height=350)
#
#         # Current Character
#         self.T1 = tk.Label(self.root, text="Character :", font=("Courier", 22, "bold"))
#         self.T1.place(x=60, y=430)
#
#         self.panel3 = tk.Label(self.root, text="", font=("Courier", 22))
#         self.panel3.place(x=250, y=430)
#
#         # Sentence area
#         self.T3 = tk.Label(self.root, text="Sentence :", font=("Courier", 22, "bold"))
#         self.T3.place(x=60, y=480)
#
#         self.panel5 = tk.Text(self.root, font=("Courier", 18), wrap="word", height=2, width=45)
#         self.panel5.place(x=260, y=480)
#
#         # Suggestions
#         self.T4 = tk.Label(self.root, text="Suggestions :", fg="red", font=("Courier", 22, "bold"))
#         self.T4.place(x=60, y=540)
#
#         # Suggestion buttons
#         btn_y = 580
#         self.b1 = tk.Button(self.root, text="", font=("Courier", 16), width=10, command=self.action1)
#         self.b1.place(x=120, y=btn_y)
#
#         self.b2 = tk.Button(self.root, text="", font=("Courier", 16), width=10, command=self.action2)
#         self.b2.place(x=350, y=btn_y)
#
#         self.b3 = tk.Button(self.root, text="", font=("Courier", 16), width=10, command=self.action3)
#         self.b3.place(x=580, y=btn_y)
#
#         self.b4 = tk.Button(self.root, text="", font=("Courier", 16), width=10, command=self.action4)
#         self.b4.place(x=810, y=btn_y)
#
#         # Speak + Clear buttons (bottom right)
#         self.speak = tk.Button(self.root, text="Speak", font=("Courier", 18), width=8, command=self.speak_fun)
#         self.speak.place(x=1100, y=480)
#
#         self.clear = tk.Button(self.root, text="Clear", font=("Courier", 18), width=8, bg="red", fg="white",
#                                command=self.clear_fun)
#         self.clear.place(x=1100, y=580)
#
#         self.str = " "
#         self.ccc=0
#         self.word = " "
#         self.current_symbol = "C"
#         self.photo = "Empty"
#
#
#         self.word1=" "
#         self.word2 = " "
#         self.word3 = " "
#         self.word4 = " "
#
#         self.video_loop()
#
#     def video_loop(self):
#         try:
#             ok, frame = self.vs.read()
#             cv2image = cv2.flip(frame, 1)
#             if cv2image.any:
#                 hands = hd.findHands(cv2image, draw=False, flipType=True)
#                 cv2image_copy=np.array(cv2image)
#                 cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)
#                 self.current_image = Image.fromarray(cv2image)
#                 imgtk = ImageTk.PhotoImage(image=self.current_image)
#                 self.panel.imgtk = imgtk
#                 self.panel.config(image=imgtk)
#
#                 if hands[0]:
#                     hand = hands[0]
#                     map = hand[0]
#                     x, y, w, h=map['bbox']
#                     image = cv2image_copy[y - offset:y + h + offset, x - offset:x + w + offset]
#
#                     white = cv2.imread("white.jpg")
#                     # img_final=img_final1=img_final2=0
#                     if image.all:
#                         handz = hd2.findHands(image, draw=False, flipType=True)
#                         self.ccc += 1
#                         if handz[0]:
#                             hand = handz[0]
#                             handmap=hand[0]
#                             self.pts = handmap['lmList']
#                             # x1,y1,w1,h1=hand['bbox']
#
#                             os = ((400 - w) // 2) - 15
#                             os1 = ((400 - h) // 2) - 15
#                             for t in range(0, 4, 1):
#                                 cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
#                                          (0, 255, 0), 3)
#                             for t in range(5, 8, 1):
#                                 cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
#                                          (0, 255, 0), 3)
#                             for t in range(9, 12, 1):
#                                 cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
#                                          (0, 255, 0), 3)
#                             for t in range(13, 16, 1):
#                                 cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
#                                          (0, 255, 0), 3)
#                             for t in range(17, 20, 1):
#                                 cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
#                                          (0, 255, 0), 3)
#                             cv2.line(white, (self.pts[5][0] + os, self.pts[5][1] + os1), (self.pts[9][0] + os, self.pts[9][1] + os1), (0, 255, 0),
#                                      3)
#                             cv2.line(white, (self.pts[9][0] + os, self.pts[9][1] + os1), (self.pts[13][0] + os, self.pts[13][1] + os1), (0, 255, 0),
#                                      3)
#                             cv2.line(white, (self.pts[13][0] + os, self.pts[13][1] + os1), (self.pts[17][0] + os, self.pts[17][1] + os1),
#                                      (0, 255, 0), 3)
#                             cv2.line(white, (self.pts[0][0] + os, self.pts[0][1] + os1), (self.pts[5][0] + os, self.pts[5][1] + os1), (0, 255, 0),
#                                      3)
#                             cv2.line(white, (self.pts[0][0] + os, self.pts[0][1] + os1), (self.pts[17][0] + os, self.pts[17][1] + os1), (0, 255, 0),
#                                      3)
#
#                             for i in range(21):
#                                 cv2.circle(white, (self.pts[i][0] + os, self.pts[i][1] + os1), 2, (0, 0, 255), 1)
#
#                             res=white
#                             self.predict(res)
#
#                             self.current_image2 = Image.fromarray(res)
#
#                             imgtk = ImageTk.PhotoImage(image=self.current_image2)
#
#                             self.panel2.imgtk = imgtk
#                             self.panel2.config(image=imgtk)
#
#                             self.panel3.config(text=self.current_symbol, font=("Courier", 30))
#
#                             #self.panel4.config(text=self.word, font=("Courier", 30))
#
#
#
#                             self.b1.config(text=self.word1, font=("Courier", 20), wraplength=825, command=self.action1)
#                             self.b2.config(text=self.word2, font=("Courier", 20), wraplength=825,  command=self.action2)
#                             self.b3.config(text=self.word3, font=("Courier", 20), wraplength=825,  command=self.action3)
#                             self.b4.config(text=self.word4, font=("Courier", 20), wraplength=825,  command=self.action4)
#
#                 # Only update if the sentence has changed
#                 if getattr(self, '_last_str', None) != self.str:
#                     self.panel5.delete('1.0', tk.END)
#                     self.panel5.insert(tk.END, self.str)
#                     self._last_str = self.str
#         # Insert updated sentence
#
#         except Exception:
#             print(Exception.__traceback__)
#             hands = hd.findHands(cv2image, draw=False, flipType=True)
#             cv2image_copy=np.array(cv2image)
#             cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)
#             self.current_image = Image.fromarray(cv2image)
#             imgtk = ImageTk.PhotoImage(image=self.current_image)
#             self.panel.imgtk = imgtk
#             self.panel.config(image=imgtk)
#
#             if hands:
#                 # #print(" --------- lmlist=",hands[1])
#                 hand = hands[0]
#                 x, y, w, h = hand['bbox']
#                 image = cv2image_copy[y - offset:y + h + offset, x - offset:x + w + offset]
#
#                 white = cv2.imread("C:\\Users\\devansh raval\\PycharmProjects\\pythonProject\\white.jpg")
#                 # img_final=img_final1=img_final2=0
#
#                 handz = hd2.findHands(image, draw=False, flipType=True)
#                 print(" ", self.ccc)
#                 self.ccc += 1
#                 if handz:
#                     hand = handz[0]
#                     self.pts = hand['lmList']
#                     # x1,y1,w1,h1=hand['bbox']
#
#                     os = ((400 - w) // 2) - 15
#                     os1 = ((400 - h) // 2) - 15
#                     for t in range(0, 4, 1):
#                         cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
#                                  (0, 255, 0), 3)
#                     for t in range(5, 8, 1):
#                         cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
#                                  (0, 255, 0), 3)
#                     for t in range(9, 12, 1):
#                         cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
#                                  (0, 255, 0), 3)
#                     for t in range(13, 16, 1):
#                         cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
#                                  (0, 255, 0), 3)
#                     for t in range(17, 20, 1):
#                         cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
#                                  (0, 255, 0), 3)
#                     cv2.line(white, (self.pts[5][0] + os, self.pts[5][1] + os1), (self.pts[9][0] + os, self.pts[9][1] + os1), (0, 255, 0),
#                              3)
#                     cv2.line(white, (self.pts[9][0] + os, self.pts[9][1] + os1), (self.pts[13][0] + os, self.pts[13][1] + os1), (0, 255, 0),
#                              3)
#                     cv2.line(white, (self.pts[13][0] + os, self.pts[13][1] + os1), (self.pts[17][0] + os, self.pts[17][1] + os1),
#                              (0, 255, 0), 3)
#                     cv2.line(white, (self.pts[0][0] + os, self.pts[0][1] + os1), (self.pts[5][0] + os, self.pts[5][1] + os1), (0, 255, 0),
#                              3)
#                     cv2.line(white, (self.pts[0][0] + os, self.pts[0][1] + os1), (self.pts[17][0] + os, self.pts[17][1] + os1), (0, 255, 0),
#                              3)
#
#                     for i in range(21):
#                         cv2.circle(white, (self.pts[i][0] + os, self.pts[i][1] + os1), 2, (0, 0, 255), 1)
#
#                     res=white
#                     self.predict(res)
#
#                     self.current_image2 = Image.fromarray(res)
#
#                     imgtk = ImageTk.PhotoImage(image=self.current_image2)
#
#                     self.panel2.imgtk = imgtk
#                     self.panel2.config(image=imgtk)
#
#                     self.panel3.config(text=self.current_symbol, font=("Courier", 30))
#
#                     #self.panel4.config(text=self.word, font=("Courier", 30))
#
#
#
#                     self.b1.config(text=self.word1, font=("Courier", 20), wraplength=825, command=self.action1)
#                     self.b2.config(text=self.word2, font=("Courier", 20), wraplength=825,  command=self.action2)
#                     self.b3.config(text=self.word3, font=("Courier", 20), wraplength=825,  command=self.action3)
#                     self.b4.config(text=self.word4, font=("Courier", 20), wraplength=825,  command=self.action4)
#
#             self.panel5.config(text=self.str, font=("Courier", 30), wraplength=1025)
#         except Exception:
#             print("==", traceback.format_exc())
#         finally:
#             self.root.after(1, self.video_loop)
#
#     def distance(self,x,y):
#         return math.sqrt(((x[0] - y[0]) ** 2) + ((x[1] - y[1]) ** 2))
#
#     def action1(self):
#         idx_space = self.str.rfind(" ")
#         idx_word = self.str.find(self.word, idx_space)
#         last_idx = len(self.str)
#         self.str = self.str[:idx_word]
#         self.str = self.str + self.word1.upper()
#
#
#     def action2(self):
#         idx_space = self.str.rfind(" ")
#         idx_word = self.str.find(self.word, idx_space)
#         last_idx = len(self.str)
#         self.str=self.str[:idx_word]
#         self.str=self.str+self.word2.upper()
#         #self.str[idx_word:last_idx] = self.word2
#
#
#     def action3(self):
#         idx_space = self.str.rfind(" ")
#         idx_word = self.str.find(self.word, idx_space)
#         last_idx = len(self.str)
#         self.str = self.str[:idx_word]
#         self.str = self.str + self.word3.upper()
#
#
#
#     def action4(self):
#         idx_space = self.str.rfind(" ")
#         idx_word = self.str.find(self.word, idx_space)
#         last_idx = len(self.str)
#         self.str = self.str[:idx_word]
#         self.str = self.str + self.word4.upper()
#
#     def speak_fun(self):
#         text_to_speak = self.str.strip()
#         if text_to_speak:  # Only speak if there is text
#             threading.Thread(target=self._speak_thread, args=(text_to_speak,)).start()
#
#     def _speak_thread(self, text):
#         self.speak_engine.say(text)
#         self.speak_engine.runAndWait()
#
#
#     def clear_fun(self):
#         self.str=" "
#         self.word1 = " "
#         self.word2 = " "
#         self.word3 = " "
#         self.word4 = " "
#
#     def predict(self, test_image):
#         white=test_image
#         white = white.reshape(1, 400, 400, 3)
#         prob = np.array(self.model.predict(white)[0], dtype='float32')
#         ch1 = np.argmax(prob, axis=0)
#         prob[ch1] = 0
#         ch2 = np.argmax(prob, axis=0)
#         prob[ch2] = 0
#         ch3 = np.argmax(prob, axis=0)
#         prob[ch3] = 0
#
#         pl = [ch1, ch2]
#
#         # condition for [Aemnst]
#         l = [[5, 2], [5, 3], [3, 5], [3, 6], [3, 0], [3, 2], [6, 4], [6, 1], [6, 2], [6, 6], [6, 7], [6, 0], [6, 5],
#              [4, 1], [1, 0], [1, 1], [6, 3], [1, 6], [5, 6], [5, 1], [4, 5], [1, 4], [1, 5], [2, 0], [2, 6], [4, 6],
#              [1, 0], [5, 7], [1, 6], [6, 1], [7, 6], [2, 5], [7, 1], [5, 4], [7, 0], [7, 5], [7, 2]]
#         if pl in l:
#             if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][
#                 1]):
#                 ch1 = 0
#
#         # condition for [o][s]
#         l = [[2, 2], [2, 1]]
#         if pl in l:
#             if (self.pts[5][0] < self.pts[4][0]):
#                 ch1 = 0
#                 print("++++++++++++++++++")
#                 # print("00000")
#
#         # condition for [c0][aemnst]
#         l = [[0, 0], [0, 6], [0, 2], [0, 5], [0, 1], [0, 7], [5, 2], [7, 6], [7, 1]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if (self.pts[0][0] > self.pts[8][0] and self.pts[0][0] > self.pts[4][0] and self.pts[0][0] > self.pts[12][0] and self.pts[0][0] > self.pts[16][
#                 0] and self.pts[0][0] > self.pts[20][0]) and self.pts[5][0] > self.pts[4][0]:
#                 ch1 = 2
#
#         # condition for [c0][aemnst]
#         l = [[6, 0], [6, 6], [6, 2]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if self.distance(self.pts[8], self.pts[16]) < 52:
#                 ch1 = 2
#
#
#         # condition for [gh][bdfikruvw]
#         l = [[1, 4], [1, 5], [1, 6], [1, 3], [1, 0]]
#         pl = [ch1, ch2]
#
#         if pl in l:
#             if self.pts[6][1] > self.pts[8][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][1] and self.pts[0][0] < self.pts[8][
#                 0] and self.pts[0][0] < self.pts[12][0] and self.pts[0][0] < self.pts[16][0] and self.pts[0][0] < self.pts[20][0]:
#                 ch1 = 3
#
#
#
#         # con for [gh][l]
#         l = [[4, 6], [4, 1], [4, 5], [4, 3], [4, 7]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if self.pts[4][0] > self.pts[0][0]:
#                 ch1 = 3
#
#         # con for [gh][pqz]
#         l = [[5, 3], [5, 0], [5, 7], [5, 4], [5, 2], [5, 1], [5, 5]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if self.pts[2][1] + 15 < self.pts[16][1]:
#                 ch1 = 3
#
#         # con for [l][x]
#         l = [[6, 4], [6, 1], [6, 2]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if self.distance(self.pts[4], self.pts[11]) > 55:
#                 ch1 = 4
#
#         # con for [l][d]
#         l = [[1, 4], [1, 6], [1, 1]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if (self.distance(self.pts[4], self.pts[11]) > 50) and (
#                     self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
#                     self.pts[20][1]):
#                 ch1 = 4
#
#         # con for [l][gh]
#         l = [[3, 6], [3, 4]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if (self.pts[4][0] < self.pts[0][0]):
#                 ch1 = 4
#
#         # con for [l][c0]
#         l = [[2, 2], [2, 5], [2, 4]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if (self.pts[1][0] < self.pts[12][0]):
#                 ch1 = 4
#
#         # con for [l][c0]
#         l = [[2, 2], [2, 5], [2, 4]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if (self.pts[1][0] < self.pts[12][0]):
#                 ch1 = 4
#
#         # con for [gh][z]
#         l = [[3, 6], [3, 5], [3, 4]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][
#                 1]) and self.pts[4][1] > self.pts[10][1]:
#                 ch1 = 5
#
#         # con for [gh][pq]
#         l = [[3, 2], [3, 1], [3, 6]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if self.pts[4][1] + 17 > self.pts[8][1] and self.pts[4][1] + 17 > self.pts[12][1] and self.pts[4][1] + 17 > self.pts[16][1] and self.pts[4][
#                 1] + 17 > self.pts[20][1]:
#                 ch1 = 5
#
#         # con for [l][pqz]
#         l = [[4, 4], [4, 5], [4, 2], [7, 5], [7, 6], [7, 0]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if self.pts[4][0] > self.pts[0][0]:
#                 ch1 = 5
#
#         # con for [pqz][aemnst]
#         l = [[0, 2], [0, 6], [0, 1], [0, 5], [0, 0], [0, 7], [0, 4], [0, 3], [2, 7]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if self.pts[0][0] < self.pts[8][0] and self.pts[0][0] < self.pts[12][0] and self.pts[0][0] < self.pts[16][0] and self.pts[0][0] < self.pts[20][0]:
#                 ch1 = 5
#
#         # con for [pqz][yj]
#         l = [[5, 7], [5, 2], [5, 6]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if self.pts[3][0] < self.pts[0][0]:
#                 ch1 = 7
#
#         # con for [l][yj]
#         l = [[4, 6], [4, 2], [4, 4], [4, 1], [4, 5], [4, 7]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if self.pts[6][1] < self.pts[8][1]:
#                 ch1 = 7
#
#         # con for [x][yj]
#         l = [[6, 7], [0, 7], [0, 1], [0, 0], [6, 4], [6, 6], [6, 5], [6, 1]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if self.pts[18][1] > self.pts[20][1]:
#                 ch1 = 7
#
#         # condition for [x][aemnst]
#         l = [[0, 4], [0, 2], [0, 3], [0, 1], [0, 6]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if self.pts[5][0] > self.pts[16][0]:
#                 ch1 = 6
#
#
#         # condition for [yj][x]
#         print("2222  ch1=+++++++++++++++++", ch1, ",", ch2)
#         l = [[7, 2]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if self.pts[18][1] < self.pts[20][1] and self.pts[8][1] < self.pts[10][1]:
#                 ch1 = 6
#
#         # condition for [c0][x]
#         l = [[2, 1], [2, 2], [2, 6], [2, 7], [2, 0]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if self.distance(self.pts[8], self.pts[16]) > 50:
#                 ch1 = 6
#
#         # con for [l][x]
#
#         l = [[4, 6], [4, 2], [4, 1], [4, 4]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if self.distance(self.pts[4], self.pts[11]) < 60:
#                 ch1 = 6
#
#         # con for [x][d]
#         l = [[1, 4], [1, 6], [1, 0], [1, 2]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if self.pts[5][0] - self.pts[4][0] - 15 > 0:
#                 ch1 = 6
#
#         # con for [b][pqz]
#         l = [[5, 0], [5, 1], [5, 4], [5, 5], [5, 6], [6, 1], [7, 6], [0, 2], [7, 1], [7, 4], [6, 6], [7, 2], [5, 0],
#              [6, 3], [6, 4], [7, 5], [7, 2]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][
#                 1]):
#                 ch1 = 1
#
#         # con for [f][pqz]
#         l = [[6, 1], [6, 0], [0, 3], [6, 4], [2, 2], [0, 6], [6, 2], [7, 6], [4, 6], [4, 1], [4, 2], [0, 2], [7, 1],
#              [7, 4], [6, 6], [7, 2], [7, 5], [7, 2]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and
#                     self.pts[18][1] > self.pts[20][1]):
#                 ch1 = 1
#
#         l = [[6, 1], [6, 0], [4, 2], [4, 1], [4, 6], [4, 4]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if (self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and
#                     self.pts[18][1] > self.pts[20][1]):
#                 ch1 = 1
#
#         # con for [d][pqz]
#         fg = 19
#         # print("_________________ch1=",ch1," ch2=",ch2)
#         l = [[5, 0], [3, 4], [3, 0], [3, 1], [3, 5], [5, 5], [5, 4], [5, 1], [7, 6]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if ((self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
#                  self.pts[18][1] < self.pts[20][1]) and (self.pts[2][0] < self.pts[0][0]) and self.pts[4][1] > self.pts[14][1]):
#                 ch1 = 1
#
#         l = [[4, 1], [4, 2], [4, 4]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if (self.distance(self.pts[4], self.pts[11]) < 50) and (
#                     self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
#                     self.pts[20][1]):
#                 ch1 = 1
#
#         l = [[3, 4], [3, 0], [3, 1], [3, 5], [3, 6]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if ((self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
#                  self.pts[18][1] < self.pts[20][1]) and (self.pts[2][0] < self.pts[0][0]) and self.pts[14][1] < self.pts[4][1]):
#                 ch1 = 1
#
#         l = [[6, 6], [6, 4], [6, 1], [6, 2]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if self.pts[5][0] - self.pts[4][0] - 15 < 0:
#                 ch1 = 1
#
#         # con for [i][pqz]
#         l = [[5, 4], [5, 5], [5, 1], [0, 3], [0, 7], [5, 0], [0, 2], [6, 2], [7, 5], [7, 1], [7, 6], [7, 7]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if ((self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
#                  self.pts[18][1] > self.pts[20][1])):
#                 ch1 = 1
#
#         # con for [yj][bfdi]
#         l = [[1, 5], [1, 7], [1, 1], [1, 6], [1, 3], [1, 0]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if (self.pts[4][0] < self.pts[5][0] + 15) and (
#             (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
#              self.pts[18][1] > self.pts[20][1])):
#                 ch1 = 7
#
#         # con for [uvr]
#         l = [[5, 5], [5, 0], [5, 4], [5, 1], [4, 6], [4, 1], [7, 6], [3, 0], [3, 5]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if ((self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
#                  self.pts[18][1] < self.pts[20][1])) and self.pts[4][1] > self.pts[14][1]:
#                 ch1 = 1
#
#         # con for [w]
#         fg = 13
#         l = [[3, 5], [3, 0], [3, 6], [5, 1], [4, 1], [2, 0], [5, 0], [5, 5]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if not (self.pts[0][0] + fg < self.pts[8][0] and self.pts[0][0] + fg < self.pts[12][0] and self.pts[0][0] + fg < self.pts[16][0] and
#                     self.pts[0][0] + fg < self.pts[20][0]) and not (
#                     self.pts[0][0] > self.pts[8][0] and self.pts[0][0] > self.pts[12][0] and self.pts[0][0] > self.pts[16][0] and self.pts[0][0] > self.pts[20][
#                 0]) and self.distance(self.pts[4], self.pts[11]) < 50:
#                 ch1 = 1
#
#         # con for [w]
#
#         l = [[5, 0], [5, 5], [0, 1]]
#         pl = [ch1, ch2]
#         if pl in l:
#             if self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1]:
#                 ch1 = 1
#
#         # -------------------------condn for 8 groups  ends
#
#         # -------------------------condn for subgroups  starts
#         #
#         if ch1 == 0:
#             ch1 = 'S'
#             if self.pts[4][0] < self.pts[6][0] and self.pts[4][0] < self.pts[10][0] and self.pts[4][0] < self.pts[14][0] and self.pts[4][0] < self.pts[18][0]:
#                 ch1 = 'A'
#             if self.pts[4][0] > self.pts[6][0] and self.pts[4][0] < self.pts[10][0] and self.pts[4][0] < self.pts[14][0] and self.pts[4][0] < self.pts[18][
#                 0] and self.pts[4][1] < self.pts[14][1] and self.pts[4][1] < self.pts[18][1]:
#                 ch1 = 'T'
#             if self.pts[4][1] > self.pts[8][1] and self.pts[4][1] > self.pts[12][1] and self.pts[4][1] > self.pts[16][1] and self.pts[4][1] > self.pts[20][1]:
#                 ch1 = 'E'
#             if self.pts[4][0] > self.pts[6][0] and self.pts[4][0] > self.pts[10][0] and self.pts[4][0] > self.pts[14][0] and self.pts[4][1] < self.pts[18][1]:
#                 ch1 = 'M'
#             if self.pts[4][0] > self.pts[6][0] and self.pts[4][0] > self.pts[10][0] and self.pts[4][1] < self.pts[18][1] and self.pts[4][1] < self.pts[14][1]:
#                 ch1 = 'N'
#
#         if ch1 == 2:
#             if self.distance(self.pts[12], self.pts[4]) > 42:
#                 ch1 = 'C'
#             else:
#                 ch1 = 'O'
#
#         if ch1 == 3:
#             if (self.distance(self.pts[8], self.pts[12])) > 72:
#                 ch1 = 'G'
#             else:
#                 ch1 = 'H'
#
#         if ch1 == 7:
#             if self.distance(self.pts[8], self.pts[4]) > 42:
#                 ch1 = 'Y'
#             else:
#                 ch1 = 'J'
#
#         if ch1 == 4:
#             ch1 = 'L'
#
#         if ch1 == 6:
#             ch1 = 'X'
#
#         if ch1 == 5:
#             if self.pts[4][0] > self.pts[12][0] and self.pts[4][0] > self.pts[16][0] and self.pts[4][0] > self.pts[20][0]:
#                 if self.pts[8][1] < self.pts[5][1]:
#                     ch1 = 'Z'
#                 else:
#                     ch1 = 'Q'
#             else:
#                 ch1 = 'P'
#
#         if ch1 == 1:
#             if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][
#                 1]):
#                 ch1 = 'B'
#             if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][
#                 1]):
#                 ch1 = 'D'
#             if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][
#                 1]):
#                 ch1 = 'F'
#             if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] > self.pts[20][
#                 1]):
#                 ch1 = 'I'
#             if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] < self.pts[20][
#                 1]):
#                 ch1 = 'W'
#             if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][
#                 1]) and self.pts[4][1] < self.pts[9][1]:
#                 ch1 = 'K'
#             if ((self.distance(self.pts[8], self.pts[12]) - self.distance(self.pts[6], self.pts[10])) < 8) and (
#                     self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
#                     self.pts[20][1]):
#                 ch1 = 'U'
#             if ((self.distance(self.pts[8], self.pts[12]) - self.distance(self.pts[6], self.pts[10])) >= 8) and (
#                     self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
#                     self.pts[20][1]) and (self.pts[4][1] > self.pts[9][1]):
#                 ch1 = 'V'
#
#             if (self.pts[8][0] > self.pts[12][0]) and (
#                     self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
#                     self.pts[20][1]):
#                 ch1 = 'R'
#
#         if ch1 == 1 or ch1 =='E' or ch1 =='S' or ch1 =='X' or ch1 =='Y' or ch1 =='B':
#             if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
#                 ch1=" "
#
#
#
#         print(self.pts[4][0] < self.pts[5][0])
#         if ch1 == 'E' or ch1=='Y' or ch1=='B':
#             if (self.pts[4][0] < self.pts[5][0]) and (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
#                 ch1="next"
#
#
#         if ch1 == 'Next' or 'B' or 'C' or 'H' or 'F' or 'X':
#             if (self.pts[0][0] > self.pts[8][0] and self.pts[0][0] > self.pts[12][0] and self.pts[0][0] > self.pts[16][0] and self.pts[0][0] > self.pts[20][0]) and (self.pts[4][1] < self.pts[8][1] and self.pts[4][1] < self.pts[12][1] and self.pts[4][1] < self.pts[16][1] and self.pts[4][1] < self.pts[20][1]) and (self.pts[4][1] < self.pts[6][1] and self.pts[4][1] < self.pts[10][1] and self.pts[4][1] < self.pts[14][1] and self.pts[4][1] < self.pts[18][1]):
#                 ch1 = 'Backspace'
#
#
#         if ch1=="next" and self.prev_char!="next":
#             if self.ten_prev_char[(self.count-2)%10]!="next":
#                 if self.ten_prev_char[(self.count-2)%10]=="Backspace":
#                     self.str=self.str[0:-1]
#                 else:
#                     if self.ten_prev_char[(self.count - 2) % 10] != "Backspace":
#                         self.str = self.str + self.ten_prev_char[(self.count-2)%10]
#             else:
#                 if self.ten_prev_char[(self.count - 0) % 10] != "Backspace":
#                     self.str = self.str + self.ten_prev_char[(self.count - 0) % 10]
#
#
#         if ch1=="  " and self.prev_char!="  ":
#             self.str = self.str + "  "
#
#         self.prev_char=ch1
#         self.current_symbol=ch1
#         self.count += 1
#         self.ten_prev_char[self.count%10]=ch1
#
#
#         if len(self.str.strip())!=0:
#             st=self.str.rfind(" ")
#             ed=len(self.str)
#             word=self.str[st+1:ed]
#             self.word=word
#             if len(word.strip())!=0:
#                 ddd.check(word)
#                 lenn = len(ddd.suggest(word))
#                 if lenn >= 4:
#                     self.word4 = ddd.suggest(word)[3]
#
#                 if lenn >= 3:
#                     self.word3 = ddd.suggest(word)[2]
#
#                 if lenn >= 2:
#                     self.word2 = ddd.suggest(word)[1]
#
#                 if lenn >= 1:
#                     self.word1 = ddd.suggest(word)[0]
#             else:
#                 self.word1 = " "
#                 self.word2 = " "
#                 self.word3 = " "
#                 self.word4 = " "
#
#
#     def destructor(self):
#         print(self.ten_prev_char)
#         self.root.destroy()
#         self.vs.release()
#         cv2.destroyAllWindows()
#
#
# print("Starting Application...")
#
# (Application()).root.mainloop()

#==================================================================================================================================
#
# # Importing Libraries
import threading
import numpy as np
import math
import cv2
import os
import traceback
import pyttsx3
from keras.models import load_model
from cvzone.HandTrackingModule import HandDetector
from string import ascii_uppercase
try:
    import enchant
    try:
        ddd = enchant.Dict("en_US")
    except:
        try:
            ddd = enchant.Dict("en-US")
        except:
            try:
                broker = enchant.Broker()
                ddd = broker.request_dict("en_US")
            except:
                ddd = None
                print("Warning: enchant dictionary not available. Word suggestions will be disabled.")
except ImportError:
    print("Warning: enchant module not installed. Install with: pip install pyenchant")
    ddd = None
import tkinter as tk
from PIL import Image, ImageTk
OFFSET = 29
STABILITY_FRAMES = 5  # Number of consecutive frames needed to confirm a letter (reduced for responsiveness)
WHITE_IMAGE_PATH = "white.jpg"  # Update this path if needed
MODEL_PATH = 'cnn8grps_rad1_model.h5'
PREDICTION_INTERVAL = 2
hd = HandDetector(maxHands=1)
hd2 = HandDetector(maxHands=1)
os.environ["THEANO_FLAGS"] = "device=cuda, assert_no_cpu_op=True"
class Application:
    def __init__(self):
        self.vs = cv2.VideoCapture(0)
        self.current_image = None
        self.model = load_model(MODEL_PATH)
        print("Loaded model from disk")
        self.speak_engine = pyttsx3.init()
        self.speak_engine.setProperty("rate", 100)
        voices = self.speak_engine.getProperty("voices")
        if voices:
            self.speak_engine.setProperty("voice", voices[0].id)
        self.current_letter = None
        self.stable_letter = None
        self.stable_count = 0
        self.last_confirmed_letter = None  # Track last confirmed letter to detect changes
        self.frames_since_confirmation = 0  # Cooldown period after confirmation
        self.current_word = ""
        self.sentence = ""
        self.palm_detected = False
        self.space_added = False  # Track if space was already added for current palm gesture
        self.white_image = self.load_white_image()
        self.frame_count = 0
        self.prev_char = ""
        self.count = -1
        self.ten_prev_char = [" "] * 10
        self.ct = {'blank': 0}
        for i in ascii_uppercase:
            self.ct[i] = 0
        self.root = tk.Tk()
        self.root.title("Sign Language To Text Conversion")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.root.geometry("1300x750")
        self.T = tk.Label(self.root, text="Sign Language To Text Conversion", font=("Courier", 24, "bold"))
        self.T.place(x=240, y=10)
        self.panel = tk.Label(self.root, bg="gray")
        self.panel.place(x=60, y=60, width=500, height=350)
        self.panel2 = tk.Label(self.root, bg="lightgray")
        self.panel2.place(x=700, y=60, width=400, height=350)
        self.T1 = tk.Label(self.root, text="Character :", font=("Courier", 22, "bold"))
        self.T1.place(x=60, y=430)
        self.panel3 = tk.Label(self.root, text="", font=("Courier", 30))
        self.panel3.place(x=250, y=430)
        self.T2 = tk.Label(self.root, text="Current Word :", font=("Courier", 22, "bold"))
        self.T2.place(x=60, y=470)
        self.panel4 = tk.Label(self.root, text="", font=("Courier", 20), bg="lightyellow", width=30, anchor="w")
        self.panel4.place(x=250, y=470)
        self.T3 = tk.Label(self.root, text="Sentence :", font=("Courier", 22, "bold"))
        self.T3.place(x=60, y=510)
        self.panel5 = tk.Text(self.root, font=("Courier", 18), wrap="word", height=2, width=45)
        self.panel5.place(x=260, y=510)
        self.T4 = tk.Label(self.root, text="Suggestions :", fg="red", font=("Courier", 22, "bold"))
        self.T4.place(x=60, y=540)
        btn_y = 580
        self.b1 = tk.Button(self.root, text="", font=("Courier", 16), width=10, command=self.action1)
        self.b1.place(x=120, y=btn_y)
        self.b2 = tk.Button(self.root, text="", font=("Courier", 16), width=10, command=self.action2)
        self.b2.place(x=350, y=btn_y)
        self.b3 = tk.Button(self.root, text="", font=("Courier", 16), width=10, command=self.action3)
        self.b3.place(x=580, y=btn_y)
        self.b4 = tk.Button(self.root, text="", font=("Courier", 16), width=10, command=self.action4)
        self.b4.place(x=810, y=btn_y)
        self.speak = tk.Button(self.root, text="Speak", font=("Courier", 18), width=8, command=self.speak_fun)
        self.speak.place(x=1100, y=480)
        self.clear = tk.Button(self.root, text="Clear", font=("Courier", 18), width=8, bg="red", fg="white",
                               command=self.clear_fun)
        self.clear.place(x=1100, y=580)
        self.word1 = " "
        self.word2 = " "
        self.word3 = " "
        self.word4 = " "
        self.word = " "  # Current word being typed (for suggestions)
        self.video_loop()
    def load_white_image(self):
        possible_paths = [
            WHITE_IMAGE_PATH,
            os.path.join(os.path.dirname(__file__), WHITE_IMAGE_PATH),
            "white.jpg"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                img = cv2.imread(path)
                if img is not None:
                    return img.copy()
        print(f"Warning: {WHITE_IMAGE_PATH} not found. Creating blank white image.")
        return np.ones((400, 400, 3), dtype=np.uint8) * 255
    def video_loop(self):
        try:
            ok, frame = self.vs.read()
            if not ok:
                return
            cv2image = cv2.flip(frame, 1)
            cv2image_copy = np.array(cv2image)
            cv2image_rgb = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)
            self.current_image = Image.fromarray(cv2image_rgb)
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)
            hands = hd.findHands(cv2image, draw=False, flipType=True)
            current_palm_detected = self.detect_palm(hands)
            self.handle_space_logic(current_palm_detected)
            if hands and len(hands) > 0 and hands[0]:
                hand = hands[0]
                hand_data = hand[0]
                x, y, w, h = hand_data['bbox']
                image = cv2image_copy[max(0, y - OFFSET):y + h + OFFSET,
                        max(0, x - OFFSET):x + w + OFFSET]
                if image.size > 0:
                    handz = hd2.findHands(image, draw=False, flipType=True)
                    self.frame_count += 1
                    if handz and len(handz) > 0 and handz[0]:
                        hand_detailed = handz[0]
                        handmap = hand_detailed[0]
                        self.pts = handmap['lmList']
                        white = self.white_image.copy()  # Use cached image
                        os_offset = ((400 - w) // 2) - 15
                        os1_offset = ((400 - h) // 2) - 15
                        self.draw_hand_skeleton(white, os_offset, os1_offset)
                        if self.frame_count % PREDICTION_INTERVAL == 0:
                            detected_letter = self.predict_letter(white.copy())
                            self.frames_since_confirmation += 1
                            if detected_letter is None:
                                self.current_letter = None
                                self.stable_count = 0
                            else:
                                if detected_letter == self.current_letter:
                                    self.stable_count += 1
                                else:
                                    self.current_letter = detected_letter
                                    self.stable_count = 1
                                    if detected_letter != self.last_confirmed_letter:
                                        self.stable_letter = None
                                if self.stable_count >= STABILITY_FRAMES and detected_letter:
                                    can_confirm = False
                                    if detected_letter != self.stable_letter:
                                        can_confirm = True
                                    elif self.frames_since_confirmation > STABILITY_FRAMES * 2:  # Cooldown period
                                        can_confirm = True
                                    if can_confirm:
                                        self.confirm_letter(detected_letter)
                                        self.stable_letter = detected_letter
                                        self.last_confirmed_letter = detected_letter
                                        # Reset for next letter
                                        self.stable_count = 0
                                        self.current_letter = None
                                        self.frames_since_confirmation = 0
                        self.current_image2 = Image.fromarray(white)
                        imgtk2 = ImageTk.PhotoImage(image=self.current_image2)
                        self.panel2.imgtk = imgtk2
                        self.panel2.config(image=imgtk2)
            self.update_gui()
        except Exception as e:
            print("Error in video_loop:", traceback.format_exc())
        finally:
            self.root.after(1, self.video_loop)
    def draw_hand_skeleton(self, white, os, os1):
        for t in range(0, 4, 1):
            cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1),
                     (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1), (0, 255, 0), 3)
        for t in range(5, 8, 1):
            cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1),
                     (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1), (0, 255, 0), 3)
        for t in range(9, 12, 1):
            cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1),
                     (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1), (0, 255, 0), 3)
        for t in range(13, 16, 1):
            cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1),
                     (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1), (0, 255, 0), 3)
        for t in range(17, 20, 1):
            cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1),
                     (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1), (0, 255, 0), 3)
        cv2.line(white, (self.pts[5][0] + os, self.pts[5][1] + os1),
                 (self.pts[9][0] + os, self.pts[9][1] + os1), (0, 255, 0), 3)
        cv2.line(white, (self.pts[9][0] + os, self.pts[9][1] + os1),
                 (self.pts[13][0] + os, self.pts[13][1] + os1), (0, 255, 0), 3)
        cv2.line(white, (self.pts[13][0] + os, self.pts[13][1] + os1),
                 (self.pts[17][0] + os, self.pts[17][1] + os1), (0, 255, 0), 3)
        cv2.line(white, (self.pts[0][0] + os, self.pts[0][1] + os1),
                 (self.pts[5][0] + os, self.pts[5][1] + os1), (0, 255, 0), 3)
        cv2.line(white, (self.pts[0][0] + os, self.pts[0][1] + os1),
                 (self.pts[17][0] + os, self.pts[17][1] + os1), (0, 255, 0), 3)
        for i in range(21):
            cv2.circle(white, (self.pts[i][0] + os, self.pts[i][1] + os1), 2, (0, 0, 255), 1)

    def detect_palm(self, hands):
        if not hands or len(hands) == 0 or not hands[0]:
            return False
        try:
            hand = hands[0][0]
            if 'lmList' not in hand:
                return False
            pts = hand['lmList']
            fingers_up = (
                    pts[8][1] < pts[6][1] and  # Index finger
                    pts[12][1] < pts[10][1] and  # Middle finger
                    pts[16][1] < pts[14][1] and  # Ring finger
                    pts[20][1] < pts[18][1]  # Pinky finger
            )
            return fingers_up
        except:
            return False
    def handle_space_logic(self, palm_detected):
        if palm_detected and not self.space_added:
            if self.current_word.strip():
                self.sentence += self.current_word + " "
                threading.Thread(target=self._speak_word, args=(self.current_word.strip(),)).start()
                self.current_word = ""
            else:
                if self.sentence and not self.sentence.endswith(" "):
                    self.sentence += " "
            self.space_added = True
        elif not palm_detected:
            self.space_added = False

    def confirm_letter(self, letter):
        if letter in [" ", "next", "Backspace", None]:
            return
        if letter == "Backspace":
            if self.current_word:
                self.current_word = self.current_word[:-1]
            elif self.sentence:
                self.sentence = self.sentence.rstrip()
                if self.sentence and not self.sentence.endswith(" "):
                    words = self.sentence.rsplit(" ", 1)
                    if len(words) > 1:
                        self.sentence = words[0] + " "
                        self.current_word = words[1]
                    else:
                        self.sentence = ""
            return
        if letter and len(letter) == 1 and letter.isalpha():
            self.current_word += letter
            print(f"Added letter '{letter}' to word. Current word: '{self.current_word}'")  # Debug output
            # Update suggestions for current word
            self.update_suggestions()

    def update_gui(self):
        display_letter = self.current_letter if self.current_letter else "None"
        if self.current_letter and self.stable_count < STABILITY_FRAMES:
            display_letter += f" ({self.stable_count}/{STABILITY_FRAMES})"
        self.panel3.config(text=display_letter)
        self.panel4.config(text=self.current_word if self.current_word else " ")
        if getattr(self, '_last_sentence', None) != self.sentence:
            self.panel5.delete('1.0', tk.END)
            self.panel5.insert(tk.END, self.sentence)
            self._last_sentence = self.sentence
        self.b1.config(text=self.word1, font=("Courier", 20), wraplength=825, command=self.action1)
        self.b2.config(text=self.word2, font=("Courier", 20), wraplength=825, command=self.action2)
        self.b3.config(text=self.word3, font=("Courier", 20), wraplength=825, command=self.action3)
        self.b4.config(text=self.word4, font=("Courier", 20), wraplength=825, command=self.action4)

    def predict_letter(self, test_image):
        try:
            white = test_image.reshape(1, 400, 400, 3)
            prob = np.array(self.model.predict(white, verbose=0)[0], dtype='float32')
            ch1 = np.argmax(prob, axis=0)
            prob[ch1] = 0
            ch2 = np.argmax(prob, axis=0)
            pl = [ch1, ch2]
            ch1 = self.apply_classification_rules(ch1, pl)
            return self.convert_to_letter(ch1)
        except Exception as e:
            print(f"Error in predict_letter: {e}")
            return None
    def distance(self, x, y):
        return math.sqrt(((x[0] - y[0]) ** 2) + ((x[1] - y[1]) ** 2))
    def apply_classification_rules(self, ch1, pl):
        l = [[5, 2], [5, 3], [3, 5], [3, 6], [3, 0], [3, 2], [6, 4], [6, 1], [6, 2], [6, 6], [6, 7], [6, 0], [6, 5],
             [4, 1], [1, 0], [1, 1], [6, 3], [1, 6], [5, 6], [5, 1], [4, 5], [1, 4], [1, 5], [2, 0], [2, 6], [4, 6],
             [1, 0], [5, 7], [1, 6], [6, 1], [7, 6], [2, 5], [7, 1], [5, 4], [7, 0], [7, 5], [7, 2]]
        if pl in l:
            if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] <
                    self.pts[16][1] and self.pts[18][1] < self.pts[20][1]):
                ch1 = 0
        l = [[2, 2], [2, 1]]
        if pl in l:
            if (self.pts[5][0] < self.pts[4][0]):
                ch1 = 0
        l = [[0, 0], [0, 6], [0, 2], [0, 5], [0, 1], [0, 7], [5, 2], [7, 6], [7, 1]]
        pl = [ch1, pl[1]]
        if pl in l:
            if (self.pts[0][0] > self.pts[8][0] and self.pts[0][0] > self.pts[4][0] and self.pts[0][0] > self.pts[12][
                0] and self.pts[0][0] > self.pts[16][0] and self.pts[0][0] > self.pts[20][0]) and self.pts[5][0] > \
                    self.pts[4][0]:
                ch1 = 2
        l = [[6, 0], [6, 6], [6, 2]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.distance(self.pts[8], self.pts[16]) < 52:
                ch1 = 2
        l = [[1, 4], [1, 5], [1, 6], [1, 3], [1, 0]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.pts[6][1] > self.pts[8][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][
                1] and self.pts[0][0] < self.pts[8][0] and self.pts[0][0] < self.pts[12][0] and self.pts[0][0] < \
                    self.pts[16][0] and self.pts[0][0] < self.pts[20][0]:
                ch1 = 3
        l = [[4, 6], [4, 1], [4, 5], [4, 3], [4, 7]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.pts[4][0] > self.pts[0][0]:
                ch1 = 3
        l = [[5, 3], [5, 0], [5, 7], [5, 4], [5, 2], [5, 1], [5, 5]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.pts[2][1] + 15 < self.pts[16][1]:
                ch1 = 3
        l = [[6, 4], [6, 1], [6, 2]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.distance(self.pts[4], self.pts[11]) > 55:
                ch1 = 4
        l = [[1, 4], [1, 6], [1, 1]]
        pl = [ch1, pl[1]]
        if pl in l:
            if (self.distance(self.pts[4], self.pts[11]) > 50) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] <
                    self.pts[16][1] and self.pts[18][1] < self.pts[20][1]):
                ch1 = 4
        l = [[3, 6], [3, 4]]
        pl = [ch1, pl[1]]
        if pl in l:
            if (self.pts[4][0] < self.pts[0][0]):
                ch1 = 4
        l = [[2, 2], [2, 5], [2, 4]]
        pl = [ch1, pl[1]]
        if pl in l:
            if (self.pts[1][0] < self.pts[12][0]):
                ch1 = 4
        l = [[3, 6], [3, 5], [3, 4]]
        pl = [ch1, pl[1]]
        if pl in l:
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] <
                self.pts[16][1] and self.pts[18][1] < self.pts[20][1]) and self.pts[4][1] > self.pts[10][1]:
                ch1 = 5
        l = [[3, 2], [3, 1], [3, 6]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.pts[4][1] + 17 > self.pts[8][1] and self.pts[4][1] + 17 > self.pts[12][1] and self.pts[4][1] + 17 > \
                    self.pts[16][1] and self.pts[4][1] + 17 > self.pts[20][1]:
                ch1 = 5
        l = [[4, 4], [4, 5], [4, 2], [7, 5], [7, 6], [7, 0]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.pts[4][0] > self.pts[0][0]:
                ch1 = 5
        l = [[0, 2], [0, 6], [0, 1], [0, 5], [0, 0], [0, 7], [0, 4], [0, 3], [2, 7]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.pts[0][0] < self.pts[8][0] and self.pts[0][0] < self.pts[12][0] and self.pts[0][0] < self.pts[16][
                0] and self.pts[0][0] < self.pts[20][0]:
                ch1 = 5
        l = [[5, 7], [5, 2], [5, 6]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.pts[3][0] < self.pts[0][0]:
                ch1 = 7
        l = [[4, 6], [4, 2], [4, 4], [4, 1], [4, 5], [4, 7]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.pts[6][1] < self.pts[8][1]:
                ch1 = 7
        l = [[6, 7], [0, 7], [0, 1], [0, 0], [6, 4], [6, 6], [6, 5], [6, 1]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.pts[18][1] > self.pts[20][1]:
                ch1 = 7
        l = [[0, 4], [0, 2], [0, 3], [0, 1], [0, 6]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.pts[5][0] > self.pts[16][0]:
                ch1 = 6
        l = [[7, 2]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.pts[18][1] < self.pts[20][1] and self.pts[8][1] < self.pts[10][1]:
                ch1 = 6
        l = [[2, 1], [2, 2], [2, 6], [2, 7], [2, 0]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.distance(self.pts[8], self.pts[16]) > 50:
                ch1 = 6
        l = [[4, 6], [4, 2], [4, 1], [4, 4]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.distance(self.pts[4], self.pts[11]) < 60:
                ch1 = 6
        l = [[1, 4], [1, 6], [1, 0], [1, 2]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.pts[5][0] - self.pts[4][0] - 15 > 0:
                ch1 = 6
        l = [[5, 0], [5, 1], [5, 4], [5, 5], [5, 6], [6, 1], [7, 6], [0, 2], [7, 1], [7, 4], [6, 6], [7, 2], [5, 0],
             [6, 3], [6, 4], [7, 5], [7, 2]]
        pl = [ch1, pl[1]]
        if pl in l:
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] >
                    self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
                ch1 = 1
        l = [[6, 1], [6, 0], [0, 3], [6, 4], [2, 2], [0, 6], [6, 2], [7, 6], [4, 6], [4, 1], [4, 2], [0, 2], [7, 1],
             [7, 4], [6, 6], [7, 2], [7, 5], [7, 2]]
        pl = [ch1, pl[1]]
        if pl in l:
            if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] >
                    self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
                ch1 = 1
        l = [[6, 1], [6, 0], [4, 2], [4, 1], [4, 6], [4, 4]]
        pl = [ch1, pl[1]]
        if pl in l:
            if (self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] >
                    self.pts[20][1]):
                ch1 = 1
        l = [[5, 0], [3, 4], [3, 0], [3, 1], [3, 5], [5, 5], [5, 4], [5, 1], [7, 6]]
        pl = [ch1, pl[1]]
        if pl in l:
            if ((self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] <
                 self.pts[16][1] and self.pts[18][1] < self.pts[20][1]) and (self.pts[2][0] < self.pts[0][0]) and
                    self.pts[4][1] > self.pts[14][1]):
                ch1 = 1
        l = [[4, 1], [4, 2], [4, 4]]
        pl = [ch1, pl[1]]
        if pl in l:
            if (self.distance(self.pts[4], self.pts[11]) < 50) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] <
                    self.pts[16][1] and self.pts[18][1] < self.pts[20][1]):
                ch1 = 1
        l = [[3, 4], [3, 0], [3, 1], [3, 5], [3, 6]]
        pl = [ch1, pl[1]]
        if pl in l:
            if ((self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] <
                 self.pts[16][1] and self.pts[18][1] < self.pts[20][1]) and (self.pts[2][0] < self.pts[0][0]) and
                    self.pts[14][1] < self.pts[4][1]):
                ch1 = 1

        l = [[6, 6], [6, 4], [6, 1], [6, 2]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.pts[5][0] - self.pts[4][0] - 15 < 0:
                ch1 = 1

        # con for [i][pqz]
        l = [[5, 4], [5, 5], [5, 1], [0, 3], [0, 7], [5, 0], [0, 2], [6, 2], [7, 5], [7, 1], [7, 6], [7, 7]]
        pl = [ch1, pl[1]]
        if pl in l:
            if ((self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] <
                 self.pts[16][1] and self.pts[18][1] > self.pts[20][1])):
                ch1 = 1

        # con for [yj][bfdi]
        l = [[1, 5], [1, 7], [1, 1], [1, 6], [1, 3], [1, 0]]
        pl = [ch1, pl[1]]
        if pl in l:
            if (self.pts[4][0] < self.pts[5][0] + 15) and ((
                    self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] <
                    self.pts[16][1] and self.pts[18][1] > self.pts[20][1])):
                ch1 = 7

        # con for [uvr]
        l = [[5, 5], [5, 0], [5, 4], [5, 1], [4, 6], [4, 1], [7, 6], [3, 0], [3, 5]]
        pl = [ch1, pl[1]]
        if pl in l:
            if ((self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] <
                 self.pts[16][1] and self.pts[18][1] < self.pts[20][1])) and self.pts[4][1] > self.pts[14][1]:
                ch1 = 1

        # con for [w]
        fg = 13
        l = [[3, 5], [3, 0], [3, 6], [5, 1], [4, 1], [2, 0], [5, 0], [5, 5]]
        pl = [ch1, pl[1]]
        if pl in l:
            if not (self.pts[0][0] + fg < self.pts[8][0] and self.pts[0][0] + fg < self.pts[12][0] and self.pts[0][
                0] + fg < self.pts[16][0] and self.pts[0][0] + fg < self.pts[20][0]) and not (
                    self.pts[0][0] > self.pts[8][0] and self.pts[0][0] > self.pts[12][0] and self.pts[0][0] >
                    self.pts[16][0] and self.pts[0][0] > self.pts[20][0]) and self.distance(self.pts[4],
                                                                                            self.pts[11]) < 50:
                ch1 = 1

        # con for [w]
        l = [[5, 0], [5, 5], [0, 1]]
        pl = [ch1, pl[1]]
        if pl in l:
            if self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][
                1]:
                ch1 = 1

        return ch1

    def convert_to_letter(self, ch1):
        """Convert gesture group number to specific letter based on hand position rules."""
        # Check for space gesture (palm open with thumb down)
        if ch1 == 1 or ch1 == 'E' or ch1 == 'S' or ch1 == 'X' or ch1 == 'Y' or ch1 == 'B':
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] <
                    self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
                return " "

        # Check for "next" gesture
        if ch1 == 'E' or ch1 == 'Y' or ch1 == 'B':
            if (self.pts[4][0] < self.pts[5][0]) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] >
                    self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
                return "next"

        # Check for backspace gesture
        if ch1 == 'B' or ch1 == 'C' or ch1 == 'H' or ch1 == 'F' or ch1 == 'X':
            if (self.pts[0][0] > self.pts[8][0] and self.pts[0][0] > self.pts[12][0] and self.pts[0][0] > self.pts[16][
                0] and self.pts[0][0] > self.pts[20][0]) and (
                    self.pts[4][1] < self.pts[8][1] and self.pts[4][1] < self.pts[12][1] and self.pts[4][1] <
                    self.pts[16][1] and self.pts[4][1] < self.pts[20][1]) and (
                    self.pts[4][1] < self.pts[6][1] and self.pts[4][1] < self.pts[10][1] and self.pts[4][1] <
                    self.pts[14][1] and self.pts[4][1] < self.pts[18][1]):
                return "Backspace"

        # Convert group numbers to letters
        if ch1 == 0:
            ch1 = 'S'
            if self.pts[4][0] < self.pts[6][0] and self.pts[4][0] < self.pts[10][0] and self.pts[4][0] < self.pts[14][
                0] and self.pts[4][0] < self.pts[18][0]:
                ch1 = 'A'
            if self.pts[4][0] > self.pts[6][0] and self.pts[4][0] < self.pts[10][0] and self.pts[4][0] < self.pts[14][
                0] and self.pts[4][0] < self.pts[18][0] and self.pts[4][1] < self.pts[14][1] and self.pts[4][1] < \
                    self.pts[18][1]:
                ch1 = 'T'
            if self.pts[4][1] > self.pts[8][1] and self.pts[4][1] > self.pts[12][1] and self.pts[4][1] > self.pts[16][
                1] and self.pts[4][1] > self.pts[20][1]:
                ch1 = 'E'
            if self.pts[4][0] > self.pts[6][0] and self.pts[4][0] > self.pts[10][0] and self.pts[4][0] > self.pts[14][
                0] and self.pts[4][1] < self.pts[18][1]:
                ch1 = 'M'
            if self.pts[4][0] > self.pts[6][0] and self.pts[4][0] > self.pts[10][0] and self.pts[4][1] < self.pts[18][
                1] and self.pts[4][1] < self.pts[14][1]:
                ch1 = 'N'
            return ch1

        if ch1 == 2:
            if self.distance(self.pts[12], self.pts[4]) > 42:
                return 'C'
            else:
                return 'O'

        if ch1 == 3:
            if (self.distance(self.pts[8], self.pts[12])) > 72:
                return 'G'
            else:
                return 'H'

        if ch1 == 7:
            if self.distance(self.pts[8], self.pts[4]) > 42:
                return 'Y'
            else:
                return 'J'

        if ch1 == 4:
            return 'L'

        if ch1 == 6:
            return 'X'

        if ch1 == 5:
            if self.pts[4][0] > self.pts[12][0] and self.pts[4][0] > self.pts[16][0] and self.pts[4][0] > self.pts[20][
                0]:
                if self.pts[8][1] < self.pts[5][1]:
                    return 'Z'
                else:
                    return 'Q'
            else:
                return 'P'

        if ch1 == 1:
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] >
                    self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
                return 'B'
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] <
                    self.pts[16][1] and self.pts[18][1] < self.pts[20][1]):
                return 'D'
            if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] >
                    self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
                return 'F'
            if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] <
                    self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
                return 'I'
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] >
                    self.pts[16][1] and self.pts[18][1] < self.pts[20][1]):
                return 'W'
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] <
                self.pts[16][1] and self.pts[18][1] < self.pts[20][1]) and self.pts[4][1] < self.pts[9][1]:
                return 'K'
            if ((self.distance(self.pts[8], self.pts[12]) - self.distance(self.pts[6], self.pts[10])) < 8) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] <
                    self.pts[16][1] and self.pts[18][1] < self.pts[20][1]):
                return 'U'
            if ((self.distance(self.pts[8], self.pts[12]) - self.distance(self.pts[6], self.pts[10])) >= 8) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] <
                    self.pts[16][1] and self.pts[18][1] < self.pts[20][1]) and (self.pts[4][1] > self.pts[9][1]):
                return 'V'
            if (self.pts[8][0] > self.pts[12][0]) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] <
                    self.pts[16][1] and self.pts[18][1] < self.pts[20][1]):
                return 'R'

        return None

    def update_suggestions(self):
        """Update word suggestions based on current word being typed."""
        word = self.current_word.strip().lower()
        self.word = word

        # Check if enchant dictionary is available
        if ddd is None:
            self.word1 = " "
            self.word2 = " "
            self.word3 = " "
            self.word4 = " "
            return

        if len(word) > 0:
            try:
                suggestions = ddd.suggest(word)
                lenn = len(suggestions)

                if lenn >= 4:
                    self.word4 = suggestions[3]
                else:
                    self.word4 = " "

                if lenn >= 3:
                    self.word3 = suggestions[2]
                else:
                    self.word3 = " "

                if lenn >= 2:
                    self.word2 = suggestions[1]
                else:
                    self.word2 = " "

                if lenn >= 1:
                    self.word1 = suggestions[0]
                else:
                    self.word1 = " "
            except:
                self.word1 = " "
                self.word2 = " "
                self.word3 = " "
                self.word4 = " "
        else:
            self.word1 = " "
            self.word2 = " "
            self.word3 = " "
            self.word4 = " "
    def _speak_word(self, word):
        try:
            self.speak_engine.say(word)
            self.speak_engine.runAndWait()
        except:
            pass
    def action1(self):
        if self.word1.strip():
            self.current_word = self.word1.upper()
            self.update_suggestions()
    def action2(self):
        if self.word2.strip():
            self.current_word = self.word2.upper()
            self.update_suggestions()

    def action3(self):
        if self.word3.strip():
            self.current_word = self.word3.upper()
            self.update_suggestions()
    def action4(self):
        if self.word4.strip():
            self.current_word = self.word4.upper()
            self.update_suggestions()
    def speak_fun(self):
        text_to_speak = self.sentence.strip()
        if text_to_speak:
            threading.Thread(target=self._speak_thread, args=(text_to_speak,)).start()
    def _speak_thread(self, text):
        try:
            self.speak_engine.say(text)
            self.speak_engine.runAndWait()
        except:
            pass
    def clear_fun(self):
        self.current_word = ""
        self.sentence = ""
        self.word1 = " "
        self.word2 = " "
        self.word3 = " "
        self.word4 = " "
    def destructor(self):
        print("Closing application...")
        self.root.destroy()
        self.vs.release()
        cv2.destroyAllWindows()
print("Starting Application...")
if __name__ == "__main__":
    (Application()).root.mainloop()

#
#
