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
tello.start_video()

# Inicializar Pygame
pygame.init()
pygame.display.set_caption("Tello Video Stream")
win = pygame.display.set_mode((960, 720))

def detect_shapes(contour):
    epsilon = 0.04 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    if len(approx) == 3:
        return "Triángulo"
    elif len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = float(w) / h
        if 0.95 <= aspect_ratio <= 1.05:
            return "Cuadrado"
        else:
            return "Rectángulo"
    elif len(approx) == 5:
        return "Pentágono"
    else:
        return "Otro"

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
        shape = detect_shapes(contour)
        cv2.drawContours(frame, [contour], 0, (0, 255, 0), 3)
        x, y = contour[0][0]
        cv2.putText(frame, shape, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

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
