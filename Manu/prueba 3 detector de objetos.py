import cv2
import pygame as pg
import numpy as np
from djitellopy import Tello

tello = Tello()
win = pg.display.set_mode((1080,720))

tello.connect()
tello.streamoff()
tello.streamon()

while True:
    # Leer un frame de la cámara
    frame = tello.get_frame_read().frame

    # Si el frame se lee correctamente, ret es True


    # Convertir el frame a escala de grises
    imagen_gris = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(imagen_gris,100,200)
    blur = cv2.GaussianBlur(imagen_gris,(7,7),0)
    _, thresholded = cv2.threshold(imagen_gris, 540, 320, cv2.THRESH_BINARY)
    contornos, _ = cv2.findContours(imagen_gris, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contorno in contornos:
        cv2.drawContours(frame, [contorno], 0, (0, 255, 0), 3)
        x, y = contorno[0][0]
        

    # Mostrar la imagen en escala de grises
    imagen_gris = np.rot90(imagen_gris)
    imagen_gris = np.flipud(imagen_gris)
    imagen_gris = cv2.merge([imagen_gris,imagen_gris,imagen_gris])
    imagen_gris = pg.surfarray.make_surface(imagen_gris)
    
    edges = np.rot90(edges)
    edges = np.flipud(edges)
    edges = pg.surfarray.make_surface(edges)
    
    blur = np.rot90(blur)
    blur = np.flipud(blur)
    blur = cv2.merge([blur,blur,blur])
    blur = pg.surfarray.make_surface(blur)
    
    frame = np.rot90(frame)
    frame = np.flipud(frame)
    frame = pg.surfarray.make_surface(frame)
    
    win.blit(frame, (0,0))
    win.blit(edges, (540,0))
    win.blit(blur,(0,360))
    win.blit(imagen_gris, (540,360))
    
    pg.display.update()
    if cv2.waitKey(1) == ord('q'):
        break
