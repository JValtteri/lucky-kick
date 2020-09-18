import pygame
from pygame import display, mouse
import game_objects
from config import Config, init_screen
# from math import round

config = Config()
screen = init_screen(config)
clock = pygame.time.Clock()
# images = Images(config)

# mode_surface = self.menu_font.render('{}'.format(mode), True, (225,225,225) )
# mode_rect = mode_surface.get_rect(center = (config.SCREEN_SIZE[0] / 2,  config.SCREEN_SIZE[1] / 2 + 44 ) )

high_score = None

# TEXTS
button_start = game_objects.Texts(config.RUBIK_FONT, "START", 40, config.UI_WHITE, (config.SCREEN_SIZE[0] / 2, config.SCREEN_SIZE[1] - 70) )
button_exit = game_objects.Texts(config.RUBIK_FONT, "Exit", 40, config.UI_WHITE, (config.SCREEN_SIZE[0] / 2 + 200, config.SCREEN_SIZE[1] - 70 ) )
text_credits = game_objects.Texts(config.RUBIK_FONT, "JValtteri - 2020", 20, (205,205,205), (30, config.SCREEN_SIZE[1] - 30 ) )
button_fullscreen = game_objects.Texts(config.RUBIK_FONT, 'Fullscreen', 40, config.UI_WHITE, (config.SCREEN_SIZE[0] / 2,  config.SCREEN_SIZE[1] / 2 - 44 ) )
text_highscore = game_objects.Texts(config.RUBIK_FONT, 'Highscore: {}'.format(high_score), 40, config.UI_WHITE, (config.SCREEN_SIZE[0] / 2,  70 ) )

# DEFINE ACTORS
bacground = game_objects.Object(config.BACKGROUND, x=config.SCREEN_SIZE[0]/2, y=config.SCREEN_SIZE[1]/2)
bacground.scale(config.SCREEN_SIZE)
track = game_objects.Object(config.TRACK_0)
track.scale(( round(track.asset_size[0]*2), round(track.asset_size[1]*2) ))
track.pos(x=config.SCREEN_SIZE[0]/2, y=config.SCREEN_SIZE[1]/2)
disk = game_objects.Object(config.DISK, x=80, y=650, colorkey=config.BLUE)
disk.scale((disk.asset_size[0]//2, disk.asset_size[1]//2))
disk.pos(396, 574)
basket = game_objects.Object(config.BASKET, x=858, y=180, colorkey=config.BLUE)
basket.scale((64, 64))
power_scale = game_objects.Object(config.P_SCALE, x=config.SCREEN_SIZE[0]-20, y=config.SCREEN_SIZE[1]-60, colorkey=config.BLUE)
power_scale.rect.bottomright = (config.SCREEN_SIZE[0]-20, config.SCREEN_SIZE[1]-20)
power_bar = game_objects.Object(config.BAR)
power_bar.scale((32,1))
power_bar.rect.bottomright = (config.SCREEN_SIZE[0]-40, config.SCREEN_SIZE[1]-20)

turn_indicator = game_objects.Object(config.TURN_INDICATOR, x=config.SCREEN_SIZE[0]-120, y=config.SCREEN_SIZE[1]-60, colorkey=config.BLUE)

def throw(power, vector):
    disk.speed(power)
    disk.u_vector(vector)

def calc_power(point_a, point_b):
    dx = point_a[0] - point_b[0]
    dy = point_a[1] - point_b[1]
    power = ( (dx**2 + dy**2)**0.5 ) / 40
    if power > config.MAX_POWER:
        power = config.MAX_POWER
    return power

def vector_modifier(vectors):
    sum_x = 0
    sum_y = 0
    for vector in vectors:
        sum_x += vector[0]
        sum_y += vector[1]
    return (sum_x, sum_y)

def check_basket_collision(disk, basket):
    scored = False
    if disk.rect.collidepoint(basket):
        scored = score()
    return scored

def score():
    # play chink-sound
    print("score")
    disk.v = 0
    return True

# def check_tree_collision(bogeys, missiles):
#     hits = 0
#     for bogey in bogeys:
#         for missile in missiles:
#             if missile.rect.colliderect(bogey.rect) and missile.image is not images.splash_img:
#                 splash_it(missile, bogey)
#                 hits += 1
#     return hits

def play():
    scored = False
    running = True
    charging = False
    turn = config.TURN
    init_turn = 0

    while scored == False and running:
        bacground.draw(screen)
        track.draw(screen)
        disk.draw(screen)
        basket.draw(screen)
        power_scale.draw(screen)
        power_bar.draw(screen)
        turn_indicator.draw(screen)


        keys = pygame.key.get_pressed()  #checking pressed keys
        if keys[pygame.K_w]:
            print(('y', disk.move_y(-2)))
        elif keys[pygame.K_s]:
            print(('y', disk.move_y(2)))

        if keys[pygame.K_a]:
            print(('x', disk.move_x(-2)))
        elif keys[pygame.K_d]:
            print(('x', disk.move_x(2)))

        if keys[pygame.K_RIGHT]:
            init_turn -= config.TURN * 0.1
            turn_indicator.rotate((-init_turn, -turn*2))
        elif keys[pygame.K_LEFT]:
            init_turn += config.TURN * 0.1
            turn_indicator.rotate((-init_turn, -turn*2))

        scored = check_basket_collision(disk, (basket.x, basket.y))
        # check_tree_collision()

        if charging:
            # POWER INDICATOR ANIMATION
            mouse_x, mouse_y = mouse.get_pos()
            power = calc_power(disk.rect.center, (mouse_x, mouse_y))

            power_indication = round(power / config.MAX_POWER * 128)
            power_bar.scale((32,power_indication))
            power_bar.rect.bottomright = (config.SCREEN_SIZE[0]-40, config.SCREEN_SIZE[1]-20)

        # EVENTS
        current_events = pygame.event.get()
        for event in current_events:

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE,
                                pygame.K_ESCAPE,
                                pygame.K_RETURN,
                                pygame.K_KP_ENTER
                                ):
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # START CHARGING FOR THROW
                charging = True

            if event.type == pygame.MOUSEBUTTONUP:
                # THROW HAPPENS WHEN MOUSE IS RELEACED
                charging = False
                turn = config.TURN + init_turn
                mouse_x, mouse_y = mouse.get_pos()
                vector = game_objects.vector(disk.rect.center, (mouse_x, mouse_y))
                throw(power, vector)

        disk.move_2d()
        if disk.v > 0:
            if disk.v < 2:
                disk.v -= config.DRAG * config.MAX_POWER
            disk.v -= config.DRAG * disk.v
            mod_vector = vector_modifier(( disk.u_vect, (disk.u_vect[1] * turn, -disk.u_vect[0] * turn) ))
            disk.u_vector(mod_vector)
            turn += config.TURN * 0.01

        elif disk.v < 0:
            disk.speed(0)
            init_turn = 0
            turn_indicator.rotate((0,-1))

        display.update()
        clock.tick(60)



if __name__ == "__main__":
    play()
