import pygame
from pygame import display, mouse
import game_objects
from config import full_screen
import webbrowser
import sys
import os
from time import sleep


def menu(screen, clock, config):

    bacground = game_objects.Object(
        config.BACKGROUND,
        x=config.SCREEN_SIZE[0]/2,
        y=config.SCREEN_SIZE[1]/2
        )
    bacground.scale(config.SCREEN_SIZE)
    track = game_objects.Object(
        config.TRACK,
        path=os.path.join(config.TRACK_PATH, "track_0")
        )
    track.scale(( round(track.asset_size[0]*2), round(track.asset_size[1]*2) ))
    track.pos(x=config.SCREEN_SIZE[0]/2, y=config.SCREEN_SIZE[1]/2)
    highlite = game_objects.Object(
        config.HIGHLITE,
        colorkey=(163,73,164)
        )
    title_text = game_objects.Texts(
        config.RUBIK_FONT,
        "Lucky Kick",
        xy=(config.SCREEN_SIZE[0]/2,
        config.SCREEN_SIZE[1]/2),
        size=80
        )
    start_button = game_objects.Texts(
        config.RUBIK_FONT,
        "PLAY",
        xy=(config.SCREEN_SIZE[0] / 2,
        config.SCREEN_SIZE[1]/2 + 100)
        )
    editor_button = game_objects.Texts(
        config.RUBIK_FONT,
        "Editor",
        xy=(config.SCREEN_SIZE[0]/2,
        config.SCREEN_SIZE[1]/2 + 160),
        size=30
        )
    exit_button = game_objects.Texts(
        config.RUBIK_FONT,
        "Exit",
        xy=(config.SCREEN_SIZE[0] / 2,
        config.SCREEN_SIZE[1]/2 + 220),
        size=30
        )
    credit_button = game_objects.Texts(
        config.RUBIK_FONT,
        "(c) 2020 JValtteri",
        size=20,
        color=(205,205,205),
        xy=(100, config.SCREEN_SIZE[1] - 30 )
        )
    buttons = (start_button, editor_button, exit_button, credit_button)

    track_number = 0
    hole_number = 0
    mode = 9
    in_menu = True
    while in_menu:

        bacground.draw(screen)
        track.draw(screen)
        title_text.draw(screen)
        start_button.draw(screen)
        editor_button.draw(screen)
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
                    track_number = track_menu(screen, clock, config)
                    #hole_number = track_menu(screen, clock, config)
                    in_menu = False

                elif exit_button.rect.collidepoint((mouse_x, mouse_y)):
                    in_menu = False

                elif editor_button.rect.collidepoint((mouse_x, mouse_y)):
                    in_menu = False
                    mode = 16

                # elif res_rect.collidepoint((mouse_x, mouse_y)):
                #     screen = full_screen(config)

                elif credit_button.rect.collidepoint((mouse_x, mouse_y)):
                    webbrowser.open('https://github.com/JValtteri/lucky-kick')

        display.update()
        clock.tick(30)

    return track_number, hole_number, mode

def track_menu(screen, clock, config, max_number=10):
    bacground = game_objects.Object(
        config.BACKGROUND,
        x=config.SCREEN_SIZE[0]/2,
        y=config.SCREEN_SIZE[1]/2
        )
    bacground.scale(config.SCREEN_SIZE)
    track = game_objects.Object(
        config.TRACK,
        path=os.path.join(config.TRACK_PATH, "track_0")
        )
    track.scale(( round(track.asset_size[0]*2), round(track.asset_size[1]*2) ))
    track.pos(x=config.SCREEN_SIZE[0]/2, y=config.SCREEN_SIZE[1]/2)
    exit_button = game_objects.Texts(
        config.RUBIK_FONT,
        "Exit",
        xy=(config.SCREEN_SIZE[0] / 2 + 200, config.SCREEN_SIZE[1] - 70),
        size=40
        )
    credit_button = game_objects.Texts(
        config.RUBIK_FONT,
        "(c) 2020 JValtteri",
        size=20,
        color=(205,205,205),
        xy=(100, config.SCREEN_SIZE[1] - 30 )
        )
    highlite = game_objects.Object(
        config.HIGHLITE,
        colorkey=(163,73,164)
        )
    font_size = 60
    buttons=[]
    for i in range(1, max_number+1):
        button = game_objects.Texts(
            config.SC_FONT,
            str(i),
            size=font_size,
            xy=(config.SCREEN_SIZE[0]/2+100-i%2*200, 100+(i-1)//2*100),
            tag=i
            )
        buttons.append(button)
    buttons.append(credit_button)
    buttons.append(exit_button)
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
                # START
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

def interm_screen(screen, config, throw_number, scores):
    final_throws = game_objects.Texts(
        config.SC_FONT,
        "Score: {}".format(throw_number),
        size=80,
        color=config.UI_WHITE,
        xy=(config.SCREEN_SIZE[0] / 2, config.SCREEN_SIZE[1] / 2)
        )
    final_throws.draw(screen)
    display.update()
    skip = False
    current_events = pygame.event.get()
    for event in current_events:
        # KEYBOARD
        if event.type == pygame.KEYDOWN:
            skip = True

        # APP CLOSE
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        # MOUSE CLICK
        if event.type == pygame.MOUSEBUTTONDOWN:
            skip = True
    if skip == False:
        sleep(3)
    bacground = game_objects.Object(
        config.BACKGROUND,
        x=config.SCREEN_SIZE[0]/2,
        y=config.SCREEN_SIZE[1]/2
        )
    bacground.scale(config.SCREEN_SIZE)
    bacground.draw(screen)
    # if len(scores) > 1:
    throw_list = '-'.join(scores)
    final_score = sum([int(i) for i in scores])
    throw_history = game_objects.Texts(
        config.SC_FONT,
        "{} = {}".format(throw_list, final_score),
        size=60,
        color=config.UI_WHITE,
        xy=(config.SCREEN_SIZE[0] / 2, config.SCREEN_SIZE[1] / 2)
        )
    throw_history.draw(screen)
    display.update()
    skip = False
    current_events = pygame.event.get()
    for event in current_events:
        # KEYBOARD
        if event.type == pygame.KEYDOWN:
            skip = True

        # APP CLOSE
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        # MOUSE CLICK
        if event.type == pygame.MOUSEBUTTONDOWN:
            skip = True
    if skip == False:
        sleep(5)

def end_screen():
    pass
