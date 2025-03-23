import pygame as p
import sys
from random import*
from ctypes  import windll
import random
import json
p.init()


SCREENSIZE = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
SCREEN = p.display.set_mode(SCREENSIZE)

menu_bg = p.transform.scale(p.image.load(f'img/menu.png'), (SCREENSIZE[0], SCREENSIZE[1]))

FPS = 30

sunny = True
time_of_day = 0

CLOCK = p.time.Clock()


#sounds
walk = p.mixer.Sound("sound/walk.wav")
walk.set_volume(0.5)

shovel_sound = p.mixer.Sound("sound/shovel.mp3")
shovel_sound.set_volume(0.2)

water_sound = p.mixer.Sound("sound/watering.mp3")
water_sound.set_volume(0.1)

walk_sound_time = 0

#fonts and texts
big_font = p.font.Font('font.ttf', 250)

title_txt = big_font.render('Throne of Roots', True, (255, 255, 255))

def write(x:int, y:int, text:str, color:tuple, size:int):    
    font = p.font.Font('font.ttf', size)
    txt = font.render(text, True, color)
    SCREEN.blit(txt, (x, y))

#colors
INVENTORYNUM = (85, 43, 25)
INVENTORYCOLOR = (243, 222, 167)
INVENTORYTAKE = (85, 43, 25)

bg = (0, 206, 209)
color1 = (255, 0, 0)
color2 = (0, 150, 0)
color3 = (255, 215, 0)
white = (255 ,255 ,255 )