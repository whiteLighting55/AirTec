import cv2
import numpy as np

# Cargamos una imagen
image = cv2.imread('tu_imagen.jpg')

# Convertir la imagen a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detección de círculos
circles = cv2.HoughCircles(
    gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=0, maxRadius=0)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)

# Detección de rectángulos
contours, _ = cv2.findContours(
    gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
    if len(approx) == 4:
        cv2.drawContours(image, [contour], 0, (0, 0, 255), 2)

# Mostrar la imagen con las figuras detectadas
cv2.imshow('Figuras Detectadas', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
