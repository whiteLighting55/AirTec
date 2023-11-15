#detector de objetos, codigo escrito por manuel alejandro franco flores del tecnologico de monterrey campus tampico

#librerias necesarias

from djitellopy import Tello #libreria del dron tello
import pygame as pg #libreria para interfaces graficas
import numpy as np #funciones matematicas de alto nivel
import cv2 #manipulacion del video y camaras

'''configuraciones iniciales del dron'''

tello = Tello()
tello.connect()
tello.streamoff()
tello.streamon()
frame = tello.get_frame_read().frame #obtener frame de la camara
#tello.takeoff()




pg.init()
'''propiedades de la ventana de pygame:
    win-- nombre de la variable que almacena la ventana de pygame
    width--- ancho de la ventana
    height-- alto de la ventana
'''
width = 960
height = 720
win = pg.display.set_mode((width, height))

'''bucle infinito de ejeucion de codigo para que el dron
cumpla con lo que se le ha programadoi'''
while True:
    
    
    battery_text = "Battery {}%".format(tello.get_battery())
    font = pg.font.SysFont("comic sans ms", 32)
    battery = font.render(battery_text, True, (255,0,0), (255,255,255))
    batteryRect = battery.get_rect()
    batteryRect.center = (width/2, 600)
    
    frame = tello.get_frame_read().frame
    frame = np.rot90(frame) #rotar la camara 90 grados
    frame = np.flipud(frame) #retirar el efecto espejo
    
    cam1 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    cam1 = cv2.merge([cam1, cam1,cam1])
    
    '''dado que la camara capta un arreglo de colores y no una superficie pygame
    debemos transformarla a una '''
    
    frame = pg.surfarray.make_surface(frame) #transformacion de numpy.array a pygame.surfarray
    frame = pg.transform.scale(frame, (width/2, height/2))
    cam1 = pg.surfarray.make_surface(cam1)
    cam1 = pg.transform.scale(cam1, (width/2, height/2))
    
    
    win.blit(frame, (0,0)) #mostrar la ventana
    win.blit(cam1 , (width/2,0))
    win.blit(battery, batteryRect)
    pg.display.update() #actualizar la imagen
    