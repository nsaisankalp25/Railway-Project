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
        self.iml.place(x = 0, y = 0)
        
        cx = 900

        self.analy_l = tk.Label(window, font = ("consolas", 20), fg = '#E54601', text = 'ANALYSIS:')
        self.analy_l.place(x = cx, y = 40)

        self.tex_queue = tk.Label(window, font=("calibri", 20))
        self.tex_queue.place(x = cx, y = 200)

        self.tex_pol = tk.Label(window, font=("calibri", 20))
        self.tex_pol.place(x = cx, y = 300)

        self.tex_tracks = tk.Label(window, font=("calibri", 20))
        self.tex_tracks.place(x = cx, y = 400)


        self.model_Q = self.load_model_queue()
        self.class_names_Q = self.load_labels_queue()

        self.model_P = self.load_model_police()
        self.class_names_P = self.load_labels_police()

        self.model_T = self.load_model_tracks()
        self.class_names_T = self.load_labels_tracks()

        self.update()
        self.window.mainloop()



    def load_model_queue(self):
        try:
            model_queue = tf.keras.models.load_model(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\RailwaysAppV2\Queue_call.h5", compile=False)
            return model_queue
        except Exception as e:
            print(f"Error loading the model: {e}")
            return None
    
    def load_labels_queue(self):
        try:
            with open(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\RailwaysAppV2\Queue_call.txt", "r") as file:
                class_names = [line.strip() for line in file]
            return class_names
        except Exception as e:
            print(f"Error loading labels: {e}")
            return None
        



    def load_model_police(self):
        try:
            model_police = tf.keras.models.load_model(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\RailwaysAppV2\Pol_pass.h5", compile=False)
            return model_police
        except Exception as e:
            print(f"Error loading the model: {e}")
            return None
            
    def load_labels_police(self):
        try:
            with open(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\RailwaysAppV2\Pol_pass.txt", "r") as file:
                class_names = [line.strip() for line in file]
            return class_names
        except Exception as e:
            print(f"Error loading labels: {e}")
            return None



    def load_model_tracks(self):
        try:
            model_police = tf.keras.models.load_model(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\RailwaysAppV2\tracks.h5", compile=False)
            return model_police
        except Exception as e:
            print(f"Error loading the model: {e}")
            return None
            
    def load_labels_tracks(self):
        try:
            with open(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\RailwaysAppV2\tracks.txt", "r") as file:
                class_names = [line.strip() for line in file]
            return class_names
        except Exception as e:
            print(f"Error loading labels: {e}")
            return None
    

    def update(self):
        ret, frame = self.vid.read()

        if ret:
            # Resize the frame to the original size
            original_size_frame = cv2.resize(frame, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_AREA)

            # Resize the frame to the size expected by the Keras model
            resized_frame = cv2.resize(original_size_frame, (224, 224), interpolation=cv2.INTER_AREA)

            image = np.asarray(resized_frame, dtype=np.float32).reshape(1, resized_frame.shape[0], resized_frame.shape[1], resized_frame.shape[2])
            image = (image / 127.5) - 1

            try:

                prediction = self.model_Q.predict(image)
                index = np.argmax(prediction)
                class_name = self.class_names_Q[index]

                if class_name == "0":
                    self.tex_queue.config(text='Less Crowd', fg='green')
                else:
                    self.tex_queue.config(text='Workforce Required', fg='red')
                
                
                
                prediction = self.model_P.predict(image)
                index = np.argmax(prediction)
                class_name = self.class_names_P[index]
                if class_name == 'Pas':
                    self.tex_pol.config(text="RPF Required", fg = "red")
                else:
                    self.tex_pol.config(text = 'Crowd under Control', fg = 'green')
                    

                prediction = self.model_T.predict(image)
                index = np.argmax(prediction)
                class_inx = self.class_names_T[index][0]

                if class_inx == '0':
                    self.tex_tracks.config(text="Obstacles on Track", fg = "red")
                else:
                    self.tex_tracks.config(text="Tracks Clear", fg = "green")


                img = cv2.cvtColor(original_size_frame, cv2.COLOR_BGR2RGB)
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
