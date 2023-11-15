import cv2
import numpy as np

# Inicializa la cámara del dron. Reemplaza esto con la biblioteca adecuada para tu dron.
cap = cv2.VideoCapture(0)  # Usar 0 para la cámara predeterminada o la dirección de la cámara del dron si es diferente.

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convertir el frame a escala de grises.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicar un desenfoque a la imagen.
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Aplicar la transformada de Hough en la imagen desenfocada.
    detected_circles = cv2.HoughCircles(
        gray_blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=20,
        param1=50,
        param2=30,
        minRadius=1,
        maxRadius=40
    )

    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            cv2.circle(frame, (a, b), r, (0, 255, 0), 2)
            cv2.circle(frame, (a, b), 1, (0, 0, 255), 3)

    cv2.imshow("Detected Circle", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
