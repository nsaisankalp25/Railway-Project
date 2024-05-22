import cv2
import threading
import pyttsx3
from PIL import Image, ImageTk
from tkinter import Tk, Label
import sys
# Global variables
win = Tk()
win.title("Face Detection")
win.geometry('650x550')

tts_playing = False
label = Label(win)
label.place(x=0, y=0)

info_l = Label(win, font=("calibri", 20), fg = 'black')
info_l.place(x=250, y=500)
obstacle_detected = False
    
def detect_faces():
    global tts_playing, obstacle_detected

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            if not obstacle_detected:
                info_l.config(text="OBSTACLE DETECTED", fg = '#972200')
                obstacle_detected = True
                if not tts_playing:
                    message = "Obstacle Detected!"
                    tts_playing = True
                    tts_thread = threading.Thread(target=play_tts, args=(message,))
                    tts_thread.start()
        else:
            if obstacle_detected:
                info_l.config(text="ALL CLEAR", fg = '#008C06')
                obstacle_detected = False

        img = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        label.config(image=img)
        label.image = img

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # Add a delay to avoid rapid changes in label
        win.update()
        win.after(10)  # Adjust the delay as needed

    cap.release()
    cv2.destroyAllWindows()

def play_tts(message):
    global tts_playing
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()
    tts_playing = False

def main():
    # Start the face detection function in a separate thread
    detection_thread = threading.Thread(target=detect_faces)
    detection_thread.start()

    # Start the Tkinter main loop
    win.mainloop()

if True:
    main()
