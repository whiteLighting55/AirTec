# aquí va el code y mmas cosas
#wenas

import cv2
from djitellopy import Tello
import tkinter as tk
from PIL import Image, ImageTk

# Inicializar el dron Tello
tello = Tello()
tello.connect()
tello.streamoff()
tello.streamon()

# Crear una ventana de tkinter
root = tk.Tk()
root.title("Dron Tello Line Detection")

# Función para actualizar el fotograma
def update_frame():
    frame = tello.get_frame_read().frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_frame, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, cv2.CV_PI / 180, threshold=100, minLineLength=100, maxLineGap=50)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Convertir el fotograma de OpenCV a formato de imagen de PIL
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    panel.img = img
    panel.config(image=img)
    panel.after(10, update_frame)

# Crear un panel para mostrar la imagen en la ventana
panel = tk.Label(root)
panel.pack(padx=10, pady=10)

# Llamar a la función para actualizar el fotograma
update_frame()

# Función para cerrar la conexión del dron y salir del programa
def on_closing():
    tello.streamoff()
    tello.disconnect()
    root.destroy()

# Configurar la función para cerrar la ventana
root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
