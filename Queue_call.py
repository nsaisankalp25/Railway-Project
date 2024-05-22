import cv2
import numpy as np
import threading
import tkinter as tk
from PIL import Image, ImageTk

import tensorflow as tf

class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        # Initialize canvas with default size (updated dynamically later)
        self.iml = tk.Label(window)
        self.tex = tk.Label(window, font=("calibri", 20))
        self.iml.pack()
        self.tex.pack()

        self.model = self.load_model()
        self.class_names = self.load_labels()

        self.update()
        self.window.mainloop()

    def load_model(self):
        try:
            model = tf.keras.models.load_model(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\Queue_call.h5", compile=False)
            return model
        except Exception as e:
            print(f"Error loading the model: {e}")
            return None

    def load_labels(self):
        try:
            with open(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\Queue_call.txt", "r") as file:
                class_names = [line.strip() for line in file]
            return class_names
        except Exception as e:
            print(f"Error loading labels: {e}")
            return None

    def update(self):
        ret, frame = self.vid.read()

        if ret:
            # Resize the frame to be 2 times bigger using cv2.resize
            frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)
            frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)

            image = np.asarray(frame, dtype=np.float32).reshape(1, 224, 224, 3)
            image = (image / 127.5) - 1

            try:
                prediction = self.model.predict(image)
                index = np.argmax(prediction)
                class_name = self.class_names[index]

                # Display the frame with class information
                if class_name == "0":
                    self.tex.config(text = 'Less Crowd', fg = 'green')
                else:
                    self.tex.config(text = 'Workforce Required', fg = 'red')

                # Convert the OpenCV BGR image to RGB
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)

                # Convert the NumPy array to a PhotoImage
                img = ImageTk.PhotoImage(img)

                # Update the Tkinter label with the new image
                self.iml.config(image=img)
                self.iml.image = img

            except Exception as e:
                print(f"Error processing frame: {e}")

        self.window.after(10, self.update)


root = tk.Tk()
app = WebcamApp(root, "Webcam App")
