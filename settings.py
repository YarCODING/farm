import pygame as p
import sys
from random import*
from ctypes  import windll
p.init()


SCREENSIZE = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)) # ширина и высота экрана
SCREEN = p.display.set_mode(SCREENSIZE)

FPS = 60

CLOCK = p.time.Clock()

pos = (-1, -1)
bg = (0, 206, 209)
color1 = (255, 0, 0)
color2 = (0, 150, 0)
color3 = (255, 215, 0)
white = (255 ,255 ,255 )