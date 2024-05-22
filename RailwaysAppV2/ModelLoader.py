from tensorflow.keras.models import load_model


def load_models():
    try:
        model_queue = load_model(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\RailwaysAppV2\Queue_call.h5", compile=False)
        model_police = load_model(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\RailwaysAppV2\Pol_pass.h5", compile=False)
        model_tracks = load_model(r"C:\Users\saisa\Desktop\Coding\Python Codes\T HUB\RailwaysAppV2\tracks.h5", compile=False)
        return (model_queue, model_police, model_tracks)
    except Exception as e:
        print(f"Error loading the model: {e}")
        return None

def load_labels():
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

