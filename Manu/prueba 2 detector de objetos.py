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

    # Detectar círculos en la imagen
    circles = cv2.HoughCircles(
        gray_frame, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=10, maxRadius=50
    )

    # Detectar contornos en la imagen
    _, thresholded = cv2.threshold(gray_frame, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar círculos y detectar figuras geométricas
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            center = (circle[0], circle[1])
            radius = circle[2]
            cv2.circle(frame, center, radius, (0, 255, 0), 3)

    for contour in contours:
        cv2.drawContours(frame, [contour], 0, (0, 255, 0), 3)
        x, y = contour[0][0]

    # Mostrar el fotograma con los círculos y las figuras geométricas en la ventana de Pygame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, 0)
    frame = pygame.surfarray.make_surface(frame)
    win.blit(frame, (0, 0))
    pygame.display.update()

# Detener la transmisión de video y cerrar la ventana de Pygame
tello.stop_video()
tello.land()
pygame.quit()
