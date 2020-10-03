import pygame
from pygame import display, mouse
import game_objects
from config import Config, init_screen, full_screen
import editor
import menu
import math
import os

print("""
Lucky-Kick Disk Golf, Copyright (C) 2020 JValtteri
Lucky-Kick comes with ABSOLUTELY NO WARRANTY; for details type check LICENSE file.
This is free software, and you are welcome to redistribute it
""")

config = Config()
screen, screen_size = init_screen(config)
config.update_screen_size(screen_size)
full_screen(config)
clock = pygame.time.Clock()

high_score = None

# TEXTS
button_start = game_objects.Texts(
    config.RUBIK_FONT,
    "START",
    size=40,
    color=config.UI_WHITE,
    xy=(config.SCREEN_SIZE[0] / 2, config.SCREEN_SIZE[1] - 70)
    )
button_exit = game_objects.Texts(
    config.RUBIK_FONT,
    "Exit",
    size=40,
    color=config.UI_WHITE,
    xy=(config.SCREEN_SIZE[0] / 2 + 200, config.SCREEN_SIZE[1] - 70 )
    )
text_credits = game_objects.Texts(
    config.RUBIK_FONT,
    "(c) 2020 JValtteri",
    size=20,
    color=(205,205,205),
    xy=(30, config.SCREEN_SIZE[1] - 30 )
    )
button_fullscreen = game_objects.Texts(
    config.RUBIK_FONT,
    'Fullscreen',
    size=40,
    color=config.UI_WHITE,
    xy=(config.SCREEN_SIZE[0] / 2,  config.SCREEN_SIZE[1] / 2 - 44 )
    )
text_highscore = game_objects.Texts(
    config.RUBIK_FONT,
    'Highscore: {}'.format(high_score),
    size=40,
    color=config.UI_WHITE,
    xy=(config.SCREEN_SIZE[0] / 2,  70 )
    )
text_score = game_objects.Texts(
    config.RUBIK_FONT,
    'Score: X',
    40,
    color=config.UI_WHITE,
    xy=(config.SCREEN_SIZE[0] / 2,  70 )
    )

# DEFINE ACTORS
#
# Background
bacground = game_objects.Object(
    config.BACKGROUND,
    x=config.SCREEN_SIZE[0]/2,
    y=config.SCREEN_SIZE[1]/2)
bacground.scale(config.SCREEN_SIZE)
#
# UI objects
power_scale = game_objects.Object(
    config.P_SCALE,
    x=config.SCREEN_SIZE[0]-20,
    y=config.SCREEN_SIZE[1]-60,
    colorkey=config.BLUE
    )
power_scale.rect.bottomright = (config.SCREEN_SIZE[0]-20, config.SCREEN_SIZE[1]-20)
power_bar = game_objects.Object(config.BAR)
power_bar.scale((32,1))
power_bar.rect.bottomright = (config.SCREEN_SIZE[0]-40, config.SCREEN_SIZE[1]-20)
turn_indicator = game_objects.Object(
    config.TURN_INDICATOR,
    x=config.SCREEN_SIZE[0]-120,
    y=config.SCREEN_SIZE[1]-60,
    colorkey=config.BLUE
    )

def load_track(track_number=0, hole_number=0):
    print("hole_number: {}".format(hole_number))
    track_data = {}
    track_data["is_track"] = False        # Status code to signal succass or failure
    try:
        f = open( os.path.join(
            config.TRACK_PATH,
            "track_{}".format(track_number),
            "track"),
            'r' )
        holes = f.readlines()

        track_data["total_holes"] = len(holes)

        try:
            hole = holes[hole_number].split(' ')
        except IndexError:
            print("Track file is EMPTY")
        print(hole)     # DEBUG
        track_data["par"] = int(hole.pop(0))

        track_data["track"] = [float(hole.pop(0)), float(hole.pop(0))]
        track_data["disk"] = [float(hole.pop(0)), float(hole.pop(0))]
        track_data["basket"] = [float(hole.pop(0)), float(hole.pop(0))]
        track_data["trees"] = []
        f.close()
        # for _ in hole:
        while hole != []:
            track_data["trees"].append( [ float(hole.pop(0)), float(hole.pop(0)) ] )
        track_data["is_track"] = True
    except FileNotFoundError:
        track_data["total_holes"] = 0
        return track_data
    return track_data

def throw_disk(power, vector, disk):
    disk.speed(power)
    disk.u_vector(vector)

def throw(throw_number, power, disk):
    throw_number += 1
    text_score.update(message='Throws: {}'.format(throw_number))
    text_score.get_rect()
    mouse_x, mouse_y = mouse.get_pos()
    vector = game_objects.vector(disk.rect.center, (mouse_x, mouse_y))
    throw_disk(power, vector, disk)
    return throw_number

def drag(turn, disk):
    if disk.v < 2:
        disk.v -= config.DRAG * config.MAX_POWER
    disk.v -= config.DRAG * disk.v
    mod_vector = vector_modifier((
        disk.u_vect,
        (disk.u_vect[1] * turn, -disk.u_vect[0] * turn)
        ))
    disk.u_vector(mod_vector)
    turn += config.TURN * 0.01
    return turn

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
        scored = score(disk)
    return scored

def camera_move(track, basket, disk, trees, dx=0, dy=0):
    # BUILD A LIST OF ENTITIES TO MOVE
    entities=[track, basket, disk]
    for tree in trees:
        entities.append(tree)
    # MOVE ENTITIES
    for entity in entities:
        entity.move_x(-dx)
        entity.move_y(-dy)

def score(disk):
    # play chink-sound
    print("score")
    disk.v = 0
    return True

def check_tree_collision(disk, trees):
    collision_vector = None
    for tree in trees:
        if disk.rect.collidepoint((tree.x, tree.y)):
            collision_vector = game_objects.vector(
                (tree.x, tree.y),
                (disk.x, disk.y)
                )
            break
    return collision_vector

def kick(disk, collision_vector):
    vect_0 = disk.u_vect
    vect_1 = collision_vector
    angle_0 = math.degrees( math.atan(vect_0[0]/vect_0[1]) )
    angle_1 = math.degrees( math.atan(vect_1[1]/-vect_1[0]) )
    new_angle = 2 * angle_1 - angle_0
    new_vect = (1, math.tan(new_angle))
    return new_vect

def play(track_data):
    # TRACK OBJECTS
    track = game_objects.Object(
        config.TRACK,
        path = os.path.join(config.TRACK_PATH, "track_{}".format(track_number)))
    track.scale(( round(track.asset_size[0]*2), round(track.asset_size[1]*2) ))
    track.pos(track_data["track"][0], track_data["track"][1])
    disk = game_objects.Object(
        config.DISK,
        colorkey=config.BLUE
        )
    disk.scale((disk.asset_size[0]//2, disk.asset_size[1]//2))
    disk.pos(track_data["disk"][0], track_data["disk"][1])    #(396, 574)
    basket = game_objects.Object(
        config.BASKET,
        x=track_data["basket"][0],
        y=track_data["basket"][1],
        colorkey=config.BLUE
        )
    basket.scale((64, 64))
    basket.draw(screen)
    trees = []
    for tree_xy in track_data["trees"]:
        trees.append(game_objects.Object(
            config.TREE,
            x=tree_xy[0],
            y=tree_xy[1],
            colorkey=config.BLUE
            ))
        trees[-1].scale(( round(trees[-1].asset_size[0]//1.5), round(trees[-1].asset_size[0]//1.5) ))

    scored = False
    running = True
    charging = False
    turn = config.TURN
    init_turn = 0
    angle = 0
    throw_number = 0
    text_score.update(message='Score: {}'.format(throw_number))
    text_score.get_rect()

    pygame.event.get()  #   Catch the MOUSEBUTTON_UP event from menu

    while scored == False and running:
        bacground.draw(screen)
        track.draw(screen)
        basket.draw(screen)
        for tree in trees:
            tree.draw(screen)
        disk.draw(screen)
        for tree in trees:
            tree.draw(screen)
        power_scale.draw(screen)
        power_bar.draw(screen)
        turn_indicator.draw(screen)
        text_score.draw(screen)

        # CHECK PRESSED KEYS
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            camera_move(track, basket, disk, trees, dy=-4)
        elif keys[pygame.K_s]:
            camera_move(track, basket, disk, trees, dy=4)

        if keys[pygame.K_a]:
            camera_move(track, basket, disk, trees, dx=-4)
        elif keys[pygame.K_d]:
            camera_move(track, basket, disk, trees, dx=4)

        if keys[pygame.K_RIGHT]:
            if angle > -90:
                init_turn -= config.TURN * 0.1
                angle = init_turn/config.TURN/0.1
                print(angle)
                turn_indicator.rotate((-math.tan(math.radians(angle)), -1 ))

        elif keys[pygame.K_LEFT]:
            if angle < 90:
                init_turn += config.TURN * 0.1
                angle = init_turn/config.TURN/0.1
                turn_indicator.rotate((-math.tan(math.radians(angle)), -1 ))
                print(angle)

        scored = check_basket_collision(disk, (basket.x, basket.y))
        collision_vector = check_tree_collision(disk, trees)
        if collision_vector is not None:
            kick_vector = kick(disk, collision_vector)
            disk.u_vector(kick_vector)

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

            if event.type == pygame.MOUSEBUTTONDOWN and disk.v == 0:
                # START CHARGING FOR THROW
                charging = True

            if event.type == pygame.MOUSEBUTTONUP and disk.v == 0:
                # THROW HAPPENS WHEN MOUSE IS RELEACED
                # AND
                # DISK IS STATIONARY
                charging = False
                throw_number = throw(throw_number, power, disk)
                turn = config.TURN + init_turn

        disk.move_2d()
        if disk.v > 0:
            turn = drag(turn, disk)

        elif disk.v < 0:
            disk.speed(0)
            init_turn = 0
            turn_indicator.rotate((0,-1))

        display.update()
        clock.tick(60)
    return throw_number

if __name__ == "__main__":

    while True:
        track_number, hole_number, mode = menu.menu(screen, clock, config)
        total_holes = 1
        scores = []

        if mode == 0:
            # PLAY MODE
            while hole_number <= total_holes:
                print("holenumber: {}, total holes: {}".format(
                    hole_number,
                    total_holes
                    ))
                track_data = load_track(track_number, hole_number)
                print("par: {}, track: {}, disk: {}, basket: {}, trees: {}".format(
                    track_data["par"],
                    track_data["track"],
                    track_data["disk"],
                    track_data["basket"],
                    track_data["trees"]
                    ))
                if track_data["is_track"] == True:
                    # START GAME
                    throw_number = play(track_data)
                    scores.append(str(throw_number))
                    menu.interm_screen(screen, config, throw_number, scores)
                hole_number += 1
            menu.end_screen()

        elif mode == 16:
            # EDITOR MODE
            # Check if the track exists
            track_number = menu.track_menu(screen, clock, config)
            track_data = load_track(track_number, 0)
            if track_data["is_track"] == True:
                # OLD TRACK: NEW/EDIT LANES
                hole_number = menu.track_menu(
                    screen, clock, config,
                    max_number = track_data["total_holes"] + 1
                    )
                track_path = os.path.join(config.TRACK_PATH, "track_{}".format(track_number))
                new_lane = editor.editor(screen, config, track_number, hole_number)
                editor.save_changes(config, track_number, hole_number, new_lane, track_path)
            elif track_data["is_track"] == False:
                # NEW TRACK
                print("New Track")
                track_path = os.path.join(config.TRACK_PATH, "track_{}".format(track_number))
                new_track = editor.editor(screen, config, track_number, 1)
                editor.save_track(track_data, track_path)
        else:
            break
