import cv2

# Inicializar la captura de video desde la cámara
cap = cv2.VideoCapture(0)  # Cambiar el valor a la ubicación de la cámara del dron si es necesario

while True:
    ret, frame = cap.read()  # Capturar un fotograma desde la cámara

    if not ret:
        break

    # Convertir el fotograma a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detección de círculos
    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=0, maxRadius=0)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)

    # Detección de rectángulos
    contours, _ = cv2.findContours(
        gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            cv2.drawContours(frame, [contour], 0, (0, 0, 255), 2)

    # Mostrar el video en tiempo real
    cv2.imshow('Detección de Figuras', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Presionar la tecla Esc para salir
        break

cap.release()
cv2.destroyAllWindows()
