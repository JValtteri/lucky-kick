import os
import pygame

# Lucky-Kick Disk Golf, Copyright (C) 2020 JValtteri
# Lucky-Kick comes with ABSOLUTELY NO WARRANTY; for details type check LICENSE file.
# This is free software, and you are welcome to redistribute it

class Config():

    FONT = 'assets/04B_19.TTF'

    def __init__(self):

        self.SCREEN_SIZE = [1360,768]
        self.ASSET_SIZE = (64, 64)
        self.ASSET_PATH = 'assets'
        self.TRACK_PATH = 'assets/tracks'
        self.BACKGROUND = 'bg.png'
        self.TRACK = 'track.png'
        self.HIGHLITE = 'highlite.png'
        self.BASKET = 'basket.png'
        self.DISK = 'disk.png'
        self.BLOB = 'blob.png'
        self.TREE = 'tree.png'
        self.P_SCALE = 'scale.png'
        self.BAR = 'bar.png'
        self.TURN_INDICATOR = 'turn.png'
        self.SC_FONT = 'SourceCodePro-Light.ttf'
        self.RUBIK_FONT = 'Rubik-Regular.ttf'

        self.HIGH_SCORE = 0

        # DISK PROPERTIES
        self.MAX_POWER = 5
        self.DRAG = 0.00417    # 0.025
        self.TURN = 0.004

        self.BLUE = (63,72,204)
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.PINK = (163,73,164)
        self.UI_WHITE =  (225,225,225)

    def update_screen_size(self, new_screen):
        self.SCREEN_SIZE = new_screen
        self.SHIP_LOCALE = ( self.SCREEN_SIZE[0] / 2, self.SCREEN_SIZE[1] - 100 )

def init_screen(config):
    pygame.init()
    monitor_info = pygame.display.Info()
    screen_size = (monitor_info.current_w, monitor_info.current_h)
    screen = pygame.display.set_mode((screen_size))   #((config.SCREEN_SIZE))#, pygame.FULLSCREEN)
    pygame.display.set_caption('Lucky Kick Frisbee Golf')
    return screen, screen_size

def full_screen(config):
    pygame.init()
    monitor_info = pygame.display.Info()
    # if monitor_info.current_h < 2024:
    #     print(monitor_info.current_h)                       # DEBUG
    #     config.update_screen_size(monitor_info.current_h)
    screen = pygame.display.set_mode((config.SCREEN_SIZE ), pygame.FULLSCREEN)#, pygame.FULLSCREEN)
    return screen


# class Images():

#     def __init__(self, config):
#         from pygame import image, transform

#         # IMAGES
#         self.background_img = image.load(config.BACKGROUND).convert()
#         self.background_img = transform.scale(self.background_img, config.SCREEN_SIZE)

#         # self.croshair_img = image.load(config.CROSHAIR).convert()
#         # self.croshair_img.set_colorkey((63,72,204))

#         ### Highlite
#         self.highlite_img = image.load(config.HIGHLITE).convert()
#         self.highlite_img.set_colorkey((163,73,164))
#         # self.highlite_img.set_alpha(95)

    # def draw_highlite(self, screen, position):
    #     # self.highlite_img = transform.scale(self.highlite_img, config.SCREEN_SIZE)
    #     highlite_rect = self.highlite_img.get_rect(center = (position) )
    #     screen.blit(self.highlite_img, highlite_rect)
    #     return highlite_rect
