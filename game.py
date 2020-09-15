import pygame
from pygame import display
import game_objects
from config import Config, init_screen

config = Config()
screen = init_screen(config)
clock = pygame.time.Clock()
# images = Images(config)

# mode_surface = self.menu_font.render('{}'.format(mode), True, (225,225,225) )
# mode_rect = mode_surface.get_rect(center = (config.SCREEN_SIZE[0] / 2,  config.SCREEN_SIZE[1] / 2 + 44 ) )

high_score = None

button_start = game_objects.Texts(config.RUBIK_FONT, "START", 40, config.UI_WHITE, (config.SCREEN_SIZE[0] / 2, config.SCREEN_SIZE[1] - 70) )
button_exit = game_objects.Texts(config.RUBIK_FONT, "Exit", 40, config.UI_WHITE, (config.SCREEN_SIZE[0] / 2 + 200, config.SCREEN_SIZE[1] - 70 ) )
text_credits = game_objects.Texts(config.RUBIK_FONT, "JValtteri - 2020", 20, (205,205,205), (30, config.SCREEN_SIZE[1] - 30 ) )
button_fullscreen = game_objects.Texts(config.RUBIK_FONT, 'Fullscreen', 40, config.UI_WHITE, (config.SCREEN_SIZE[0] / 2,  config.SCREEN_SIZE[1] / 2 - 44 ) )
text_highscore = game_objects.Texts(config.RUBIK_FONT, 'Highscore: {}'.format(high_score), 40, config.UI_WHITE, (config.SCREEN_SIZE[0] / 2,  70 ) )

def play():
    running = True

    # DEFINE ACTORS
    bacground = game_objects.Object(config.BACKGROUND, expire=False, visible=True)
    bacground.scale(config.SCREEN_SIZE)
    disk = game_objects.Object(config.DISK, x=80, y=650, expire=False, visible=True, colorkey=config.BLUE)

    while running == True:
        bacground.draw(screen)
        disk.draw(screen)

        keys = pygame.key.get_pressed()  #checking pressed keys
        if keys[pygame.K_w]:
            disk.move_y(-0.4)
        elif keys[pygame.K_s]:
            disk.move_y(0.4)

        if keys[pygame.K_a]:
            disk.move_x(-0.4)
        elif keys[pygame.K_d]:
            disk.move_x(0.4)

        # EVENTS
        current_events = pygame.event.get()
        for event in current_events:

            # KEYBOARD
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE,
                                pygame.K_ESCAPE,
                                pygame.K_RETURN,
                                pygame.K_KP_ENTER
                                ):
                    running = False

                # if event.key == pygame.K_w:
                #     print( wraith.move_dist(config, +0.1) )

                # if event.key == pygame.K_s:
                #     print( wraith.move_dist(config, -0.1) )

            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        display.update()
        clock.tick(60)



if __name__ == "__main__":
    play()
