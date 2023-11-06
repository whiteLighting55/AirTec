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
frame = tello.get_frame_read().frame
def detect_geometric_shapes(contour):
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



    # Convertir el fotograma a escala de grises
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Detectar contornos en la imagen
    _, thresholded = cv2.threshold(gray_frame, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar contornos y detectar figuras geométricas
    for contour in contours:
        shape = detect_geometric_shapes(contour)
        cv2.drawContours(frame, [contour], 0, (0, 255, 0), 3)
        x, y = contour[0][0]
        cv2.putText(frame, shape, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Mostrar el fotograma con los contornos y las figuras geométricas en la ventana de Pygame
    frame = np.rot90(frame)
    frame = np.flipud(frame)
    frame = pygame.surfarray.make_surface(frame)
    win.blit(frame, (0, 0))
    pygame.display.update()

# Detener la transmisión de video y cerrar la ventana de Pygame
tello.stop_video()
tello.land()
pygame.quit()
