import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from tensorflow.keras.models import load_model

class WebcamApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("RAILWAY PROTECTION PROJECT")
        self.window.geometry("1200x800")

        self.vid = cv2.VideoCapture(0)
        self.iml = tk.Label(self.window)
        self.iml.place(x = 0, y = 0)
        
        cx = 900

        self.analy_l = tk.Label(self.window, font = ("consolas", 20), fg = '#E54601', text = 'ANALYSIS:')
        self.analy_l.place(x = cx, y = 40)

        self.tex_queue = tk.Label(self.window, font=("calibri", 20))
        self.tex_queue.place(x = cx, y = 200)

        self.tex_pol = tk.Label(self.window, font=("calibri", 20))
        self.tex_pol.place(x = cx, y = 300)

        self.tex_tracks = tk.Label(self.window, font=("calibri", 20))
        self.tex_tracks.place(x = cx, y = 400)


        self.model = self.load_models()
        self.model_Q = self.model[0]
        self.model_P = self.model[1]
        self.model_T = self.model[2]


        self.class_names = self.load_labels()
        self.class_names_Q = self.class_names[0]
        self.class_names_P = self.class_names[1]
        self.class_names_T = self.class_names[2]

        self.update()
        self.window.mainloop()


    def load_models(self):
        try:
            model_queue = load_model(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\RailwaysAppV2\Queue_call.h5", compile=False)
            model_police = load_model(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\RailwaysAppV2\Pol_pass.h5", compile=False)
            model_tracks = load_model(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\RailwaysAppV2\tracks.h5", compile=False)
            return (model_queue, model_police, model_tracks)
        except Exception as e:
            print(f"Error loading the model: {e}")
            return None

    def load_labels(self):
        try:
            with open(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\RailwaysAppV2\Queue_call.txt", "r") as file:
                Q_names = [line.strip() for line in file]        
            with open(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\RailwaysAppV2\Pol_pass.txt", "r") as file:
                P_name = [line.strip() for line in file]
            with open(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\RailwaysAppV2\tracks.txt", "r") as file:
                T_name = [line.strip() for line in file]
            return (Q_names, P_name, T_name)
        
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
                    self.tex_queue.config(text='Less Crowd', fg='green', font = ('calibri', 18))
                else:
                    self.tex_queue.config(text='Workforce Required', fg='red', font = ('calibri', 20, "bold"))
                
                
                
                prediction = self.model_P.predict(image)
                index = np.argmax(prediction)
                class_name = self.class_names_P[index]
                if class_name == 'Pas':
                    self.tex_pol.config(text="RPF Required", fg = "red", font = ('calibri', 20, "bold"))
                else:
                    self.tex_pol.config(text = 'Crowd under Control', fg = 'green', font = ('calibri', 18))
                    

                prediction = self.model_T.predict(image)
                index = np.argmax(prediction)
                class_inx = self.class_names_T[index][0]

                if class_inx == '0':
                    self.tex_tracks.config(text="Obstacles on Track", fg = "red", font = ('calibri', 20, "bold"))
                else:
                    self.tex_tracks.config(text="Tracks Clear", fg = "green", font = ('calibri', 18))


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




app = WebcamApp()
