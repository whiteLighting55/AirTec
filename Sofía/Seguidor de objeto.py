import cv2
import numpy as np

# Inicializa la cámara (asegúrate de que tu dron esté configurado correctamente)
cap = cv2.VideoCapture(0)

# Definir el rango de colores del objeto a seguir (ejemplo: color verde)
lower_color = np.array([35, 100, 100])
upper_color = np.array([85, 255, 255])

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convertir el fotograma a espacio de color HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Crear una máscara para el rango de colores del objeto a seguir
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Encontrar contornos en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Seleccionar el contorno más grande (posiblemente el objeto)
        largest_contour = max(contours, key=cv2.contourArea)

        # Encontrar el centro del contorno
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Dibuja un círculo en el centro del objeto
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Aquí puedes calcular la diferencia entre el centro del objeto y el centro del fotograma
            # y usar esta información para controlar el movimiento del dron.

    # Mostrar el fotograma con el objeto resaltado
    cv2.imshow("Object Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()