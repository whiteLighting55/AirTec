import pygame
import cv2
import numpy as np
from pygame.locals import *
from djitellopy import Tello

# Inicializar el dron Tello
tello = Tello()

# Conectar con el dron Tello
tello.connect()

# Iniciar la transmisión de video
tello.streamoff()
tello.streamon()

# Inicializar Pygame
pygame.init()
pygame.display.set_caption("Tello Video Stream")
win = pygame.display.set_mode((960, 720))

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Capturar el fotograma del video del dron
    frame = tello.get_frame_read().frame

    # Convertir el fotograma a escala de grises
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_frame, 100,200)


    # Detectar contornos en la imagen
    _, thresholded = cv2.threshold(edges, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar círculos y detectar figuras geométricas

    for contour in contours:
        cv2.drawContours(frame, [contour], 0, (0, 255, 0), 3)
        x, y = contour[0][0]

    # Mostrar el fotograma con los círculos y las figuras geométricas en la ventana de Pygame
    frame = np.rot90(frame)
    frame = np.flipud(frame)
    frame = pygame.surfarray.make_surface(frame)
    win.blit(frame, (0, 0))
    pygame.display.update()
    cv2.imshow("limites",edges)

# Detener la transmisión de video y cerrar la ventana de Pygame
tello.land()
pygame.quit()
