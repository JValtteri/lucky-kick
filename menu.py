import pygame
from pygame import display, mouse
import game_objects
from config import full_screen
import webbrowser
import sys
import os

def menu(screen, clock, config):

    bacground = game_objects.Object(config.BACKGROUND, x=config.SCREEN_SIZE[0]/2, y=config.SCREEN_SIZE[1]/2)
    bacground.scale(config.SCREEN_SIZE)
    track = game_objects.Object(config.TRACK, path=os.path.join(config.TRACK_PATH, "track_0"))
    track.scale(( round(track.asset_size[0]*2), round(track.asset_size[1]*2) ))
    track.pos(x=config.SCREEN_SIZE[0]/2, y=config.SCREEN_SIZE[1]/2)
    highlite = game_objects.Object(config.HIGHLITE, colorkey=(163,73,164))
    start_button = game_objects.Texts(config.SC_FONT, "PLAY", xy=(config.SCREEN_SIZE[0] / 2, config.SCREEN_SIZE[1] - 70))
    exit_button = game_objects.Texts(config.SC_FONT, "Exit", xy=(config.SCREEN_SIZE[0] / 2 + 200, config.SCREEN_SIZE[1] - 70))
    credit_button = game_objects.Texts(config.RUBIK_FONT, "(c) 2020 JValtteri", size=20, color=(205,205,205), xy=(100, config.SCREEN_SIZE[1] - 30 ))
    buttons = (start_button, exit_button, credit_button)

    track_number = 0
    hole_number = 0
    mode = 9
    in_menu = True
    while in_menu:

        bacground.draw(screen)
        track.draw(screen)
        start_button.draw(screen)
        exit_button.draw(screen)
        credit_button.draw(screen)

        # HIGHLITE MOUSEOVER MENU ITEMS
        mouse_x, mouse_y = mouse.get_pos()
        for button in buttons:
            # HIGHLITE MOUSEOVER MENU ITEMS
            if button.rect.collidepoint((mouse_x, mouse_y)):
                highlite.pos(button.rect.midbottom[0], button.rect.midbottom[1])
                highlite.draw(screen)
            button.draw(screen)

        # EVENTS
        current_events = pygame.event.get()

        for event in current_events:
            # APP CLOSE
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

            # KEYBOARD
            if event.type == pygame.KEYDOWN:
                # START
                if event.key in (pygame.K_SPACE,
                                pygame.K_RETURN,
                                pygame.K_KP_ENTER
                                ):
                    in_menu = False

                # EXIT
                elif event.key in (pygame.K_ESCAPE,):
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

            # MOUSE CLICK
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = mouse.get_pos()
                if start_button.rect.collidepoint((mouse_x, mouse_y)):
                    mode = 0
                    track_number = track_menu(screen, clock, config, exit_button, credit_button, highlite)
                    #hole_number = track_menu(screen, clock, config, exit_button, credit_button, highlite)
                    in_menu = False

                elif exit_button.rect.collidepoint((mouse_x, mouse_y)):
                    # pygame.display.quit()
                    # pygame.quit()
                    # sys.exit()
                    pass

                # elif res_rect.collidepoint((mouse_x, mouse_y)):
                #     screen = full_screen(config)

                elif credit_button.rect.collidepoint((mouse_x, mouse_y)):
                    webbrowser.open('https://github.com/JValtteri/lucky-kick')

        display.update()
        clock.tick(30)

    return track_number, hole_number, mode

def track_menu(screen, clock, config, exit_button, credit_button, highlite):
    bacground = game_objects.Object(config.BACKGROUND, x=config.SCREEN_SIZE[0]/2, y=config.SCREEN_SIZE[1]/2)
    bacground.scale(config.SCREEN_SIZE)
    track = game_objects.Object(config.TRACK, path=os.path.join(config.TRACK_PATH, "track_0"))
    track.scale(( round(track.asset_size[0]*2), round(track.asset_size[1]*2) ))
    track.pos(x=config.SCREEN_SIZE[0]/2, y=config.SCREEN_SIZE[1]/2)
    font_size = 60
    button1 = game_objects.Texts(config.SC_FONT, "1", size=font_size, xy=(config.SCREEN_SIZE[0]/2-100, 100), tag=0)
    button2 = game_objects.Texts(config.SC_FONT, "2", size=font_size, xy=(config.SCREEN_SIZE[0]/2+100, 100), tag=1)
    button3 = game_objects.Texts(config.SC_FONT, "3", size=font_size, xy=(config.SCREEN_SIZE[0]/2-100, 200), tag=2)
    button4 = game_objects.Texts(config.SC_FONT, "4", size=font_size, xy=(config.SCREEN_SIZE[0]/2+100, 200), tag=3)
    button5 = game_objects.Texts(config.SC_FONT, "5", size=font_size, xy=(config.SCREEN_SIZE[0]/2-100, 300), tag=4)
    button6 = game_objects.Texts(config.SC_FONT, "6", size=font_size, xy=(config.SCREEN_SIZE[0]/2+100, 300), tag=5)
    button7 = game_objects.Texts(config.SC_FONT, "7", size=font_size, xy=(config.SCREEN_SIZE[0]/2-100, 400), tag=6)
    button8 = game_objects.Texts(config.SC_FONT, "8", size=font_size, xy=(config.SCREEN_SIZE[0]/2+100, 400), tag=7)
    button9 = game_objects.Texts(config.SC_FONT, "9", size=font_size, xy=(config.SCREEN_SIZE[0]/2-100, 500), tag=8)
    button10 = game_objects.Texts(config.SC_FONT, "10", size=font_size, xy=(config.SCREEN_SIZE[0]/2+100, 500), tag=9)
    buttons = (button1, button2, button3, button4, button5, button6, button7, button8,button9, button10, credit_button, exit_button)
    in_menu = True
    while in_menu:
        # DRAW
        bacground.draw(screen)
        track.draw(screen)
        mouse_x, mouse_y = mouse.get_pos()
        for button in buttons:
            # HIGHLITE MOUSEOVER MENU ITEMS
            if button.rect.collidepoint((mouse_x, mouse_y)):
                highlite.pos(button.rect.midbottom[0], button.rect.midbottom[1])
                highlite.draw(screen)
            button.draw(screen)

        # EVENTS
        current_events = pygame.event.get()
        for event in current_events:
            # KEYBOARD
            if event.type == pygame.KEYDOWN:
                START
                if event.key in (pygame.K_SPACE,
                                pygame.K_RETURN,
                                pygame.K_KP_ENTER
                                ):
                    in_menu = False

                # EXIT
                if event.key in (pygame.K_ESCAPE,):
                    in_menu = False

            # APP CLOSE
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

            # MOUSE CLICK
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = mouse.get_pos()
                if exit_button.rect.collidepoint((mouse_x, mouse_y)):
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

                for button in buttons:
                    if button.rect.collidepoint((mouse_x, mouse_y)):
                        track_number = button.tag
                        in_menu = False

                if credit_button.rect.collidepoint((mouse_x, mouse_y)):
                    webbrowser.open('https://github.com/JValtteri/lucky-kick')

        display.update()
        clock.tick(30)

    return track_number