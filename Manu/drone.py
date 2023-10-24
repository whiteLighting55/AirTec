import cv2
import pygame
from djitellopy import Tello
import numpy

# Inicializar el dron Tello
tello = Tello()
tello.connect()
tello.streamoff()
tello.streamon()

# Inicializar pygame
pygame.init()
win = pygame.display.set_mode((960, 720))
pygame.display.set_caption("Tello Line Detection")

running = True
while running:
    # Obtener el fotograma desde el dron Tello
    frame = tello.get_frame_read().frame
    #rotated_frame = cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
    # Convertir el fotograma a escala de grises
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicar detección de bordes para resaltar las líneas
    edges = cv2.Canny(gray_frame, 50, 150)

    # Buscar líneas en el fotograma
    lines = cv2.HoughLinesP(edges, 1, numpy.pi/180, threshold=100, minLineLength=100, maxLineGap=50)

    # Dibujar las líneas encontradas en el fotograma original
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Convertir el fotograma de OpenCV a formato de superficie de pygame
    frame_surface = pygame.surfarray.make_surface(cv2.flip(frame, 1)), 
    win.blit(frame_surface, (0, 0))
    pygame.display.update()

    # Verificar eventos de pygame para cerrar la ventana
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Liberar los recursos
tello.streamoff()
tello.disconnect()
pygame.quit()
