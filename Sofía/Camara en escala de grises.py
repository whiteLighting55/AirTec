import cv2

# Iniciar la captura de video. El '0' generalmente se refiere a la cámara integrada.
# Si tienes más cámaras, puedes probar con '1', '2', etc.
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    exit()

while True:
    # Leer un frame de la cámara
    ret, frame = cap.read()

    # Si el frame se lee correctamente, ret es True
    if not ret:
        print("No se pudo recibir el frame. Terminando ...")
        break

    # Convertir el frame a escala de grises
    imagen_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(imagen_gris,100,200)
    # Mostrar la imagen en escala de grises
    cv2.imshow('Imagen en escala de grises', imagen_gris)

    # Mostrar el frame original
    cv2.imshow('Camera Feed', frame)
    cv2.imshow("Fronteras",edges)
    # Romper el bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# Liberar el objeto VideoCapture y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()