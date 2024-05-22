# from keras.models import load_model  # TensorFlow is required for Keras to work
# import cv2  # Install opencv-python
# import numpy as np
# import threading
# import pyttsx3
# import tensorflow as tf
from tkinter import *
from PIL import Image, ImageTk
import os
rt = Tk()
rt.title("RAILWAY SAFETY-EFFICIENCY SYSTEM")
height = rt.winfo_screenheight()
width = rt.winfo_screenwidth()
rt.geometry(f"{width}x{height}")

# bgcolor = '#F5F5F5'
# fg2 = "#FFFFFF"
# fg3 = "#FFFFFF"
# Bbgcolor = '#0066cc'
# l1fg = '#0066cc'
# l2fg =  '#999999'

bgcolor = '#F0F0F0'
fg2 = "#FFFFFF"
fg3 = "#FFFFFF"
Bbgcolor = '#333333'
l1fg = '#0030A5'
l2fg =  '#FF6B6B'

rt.config(bg = bgcolor)
l1 = Label(rt, text = 'The RAILWAY SAFETY-EFFICIENCY SYSTEM',
           font = ("Berlin Sans FB", 35, "bold"), fg = l1fg, bg = bgcolor)
l1.place(x = 210, y = 20)


l2 = Label(rt, text = 'Providing a smooth and safe enviornment for the passengers by the help of AI',
           font = ("mooli", 15, "bold"), fg = l2fg, bg = bgcolor)
l2.place(x = 300, y = 100)

def pol_work_det():
    script = r'python "C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\Pol_pass.py"'
    os.system(script)
def Queue_crowd_manage():
    script = r'python "C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\Queue_call.py"'
    os.system(script)
def tracks_safety():
    script = r'python "C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\tracks.py"'
    os.system(script)

Q_b = Button(rt, text = "Crowd \n Management", fg = fg2, command = Queue_crowd_manage,
             borderwidth=5,activebackground= fg2, activeforeground=Bbgcolor,
             bg = Bbgcolor, font = ("Trebuchet MS", 35))
Q_b.place(x = 200, y = 200)

pol_B = Button(rt, text = 'RPF Work \nDetection', fg = fg3, command = pol_work_det,
               borderwidth=5,activebackground= fg3, activeforeground=Bbgcolor, 
                bg = Bbgcolor, font = ("Trebuchet MS", 35))
pol_B.place(x = 600, y = 200)


T_b = Button(rt, text = "Track \nMonitoring", fg = fg2, command = tracks_safety,
             borderwidth=5,activebackground= fg2, activeforeground=Bbgcolor,
             bg = Bbgcolor ,font = ("Trebuchet MS", 35))
T_b.place(x = 920, y = 200)

rpf = Image.open(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\RPF.png")
rpf = rpf.resize((140,140))
rpf_img = ImageTk.PhotoImage(rpf)

ppl = Image.open(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\ppl.png")
ppl = ppl.resize((100,100))
ppl_img = ImageTk.PhotoImage(ppl)

tracks = Image.open(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\t.png")
tracks = tracks.resize((100,100))
tracks_img = ImageTk.PhotoImage(tracks)

ppl_l = Label(rt, image = ppl_img)
ppl_l.place(x = 310, y = 400)

rpf_l = Label(rt, image = rpf_img)
rpf_l.place(x = 660, y = 400)

tracks_l = Label(rt, image = tracks_img)
tracks_l.place(x = 1000, y = 400)

rt.mainloop()