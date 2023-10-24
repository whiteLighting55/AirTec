#Código hecho por ChatGPT-3.5
# Responsable del código: Sebastián León

import time
from djitellopy import Tello

# Crear una instancia del dron Tello
tello = Tello()

# Definir funciones para las acciones del dron
def takeoff_and_land():
    tello.takeoff()
    time.sleep(8)  # Esperar 8 segundos (puedes ajustar el tiempo)
    tello.land()

def fly_straight():
    tello.takeoff()
    tello.move_forward(50)  # Volar hacia adelante 50 cm (puedes ajustar la distancia)
    tello.land()

# Iniciar la rutina autónoma al presionar "g"
def main():
    while True:
        user_input = input("Presiona 'g' para comenzar la rutina: ")
        if user_input == "g":
            print("Iniciando la rutina autónoma...")
            fly_straight()
        elif user_input == "q":
            print("Saliendo del programa.")
            break
        else:
            print("Presiona 'g' para comenzar la rutina o 'q' para salir.")

if __name__ == "__main__":
    main()