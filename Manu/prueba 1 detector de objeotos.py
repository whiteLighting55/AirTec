import pygame
import cv2
from pygame.locals import *
import numpy as np
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

    # Detectar contornos en la imagen
    _, thresholded = cv2.threshold(gray_frame, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar contornos en el fotograma original
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

    # Mostrar el fotograma con los contornos en la ventana de Pygame
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = np.flipud(frame)
    frame = pygame.surfarray.make_surface(frame)
    win.blit(frame, (0, 0))
    pygame.display.update()

# Detener la transmisión de video y cerrar la ventana de Pygame
tello.land()
pygame.quit()
