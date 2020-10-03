from pygame import display, mouse
import pygame
import game_objects
import os
from config import Config
import sys

def editor(screen, config, track_number, hole_number=0):
    clock = pygame.time.Clock()
    disk_placed = False
    basket_placed = False
    save = False
    track_path = os.path.join(config.TRACK_PATH, "track_{}".format(track_number))
    track_file = "track.png"

    track = game_objects.Object(track_file, path=track_path)
    track.scale(( round(track.asset_size[0]*2), round(track.asset_size[1]*2) ))
    track.pos(x=config.SCREEN_SIZE[0]/2, y=config.SCREEN_SIZE[1]/2)

    disk = disk = game_objects.Object(config.DISK, colorkey=config.BLUE)
    disk.scale((disk.asset_size[0]//2, disk.asset_size[1]//2))

    trees = []
    entities = []
    entities.append(track)

    while save == False or disk_placed == False or basket_placed == False:

        ### EVENTS
        current_events = pygame.event.get()
        for event in current_events:
            ### UNIVERSAL
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE,
                                pygame.K_ESCAPE,
                                pygame.K_RETURN,
                                pygame.K_KP_ENTER
                                ):
                    save = True

            ### DISK
            if disk_placed == False:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # PLACE THE DISK
                    disk_placed = True
                    entities.append(disk)
                    basket = game_objects.Object(config.BASKET, colorkey=config.BLUE)
                    basket.scale((64, 64))

            ### BASKET
            elif disk_placed == True and basket_placed == False:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # PLACE THE BASKET
                    basket_placed = True
                    entities.append(basket)
                    trees.append(game_objects.Object(config.TREE, colorkey=config.BLUE))
                    trees[-1].scale(( round(trees[-1].asset_size[0]//1.5), round(trees[-1].asset_size[0]//1.5) ))

            ### TREES
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # PLACE A TREE
                    trees.append(game_objects.Object(config.TREE, colorkey=config.BLUE))
                    trees[-1].scale(( round(trees[-1].asset_size[0]//1.5), round(trees[-1].asset_size[0]//1.5) ))

        ### DRAWING
        track.draw(screen)
        if disk_placed == False:
            mouse_x, mouse_y = mouse.get_pos()
            disk.pos(mouse_x, mouse_y)
            disk.draw(screen)

        elif basket_placed == False:
            disk.draw(screen)
            mouse_x, mouse_y = mouse.get_pos()
            basket.pos(mouse_x, mouse_y)
            basket.draw(screen)

        else:
            mouse_x, mouse_y = mouse.get_pos()
            trees[-1].pos(mouse_x, mouse_y)

        if disk_placed and basket_placed:
            disk.draw(screen)
            basket.draw(screen)
            for tree in trees:
                tree.draw(screen)

        # CAMERA MOVE
        camera_keys(entities, trees)

        display.update()
        clock.tick(60)

    ### GENERATE THE TRACK DATA FOR THE NEW TRACK

    track_data = ['3']
    track_data.append(str(track.x))
    track_data.append(str(track.y))
    track_data.append(str(disk.x))
    track_data.append(str(disk.y))
    track_data.append(str(basket.x))
    track_data.append(str(basket.y))
    for tree in trees:
        track_data.append(str(tree.x))
        track_data.append(str(tree.y))

    print(track_data)
    track_data = ' '.join(track_data)
    return track_data


def save_track(track_data, track_path):
    f = open(os.path.join(track_path, "track"), 'w')
    f.write(track_data)
    f.close()


def save_changes(config, track_number, hole_number, new_lane, track_path):
    holes = load_track(config, track_number, hole_number)
    if hole_number - 1 in range(len(holes)):
        # IF EDITING EXISTING LANE
        holes[hole_number - 1] = new_lane
    else:
        # IF THE LANE IS NEW
        holes.append(new_lane)
    # SAVE
    holes = '\n'.join(holes)
    save_track(holes, track_path)


def load_track(config, track_number=0, hole_number=0):
    print("hole_number: {}".format(hole_number))
    try:
        f = open( os.path.join(config.TRACK_PATH, "track_{}".format(track_number), "track") ,'r' )
        holes = f.readlines()
        f.close()
        return holes
    except FileNotFoundError:
        return []


def camera_move(entities, trees, dx=0, dy=0):
    # BUILD A LIST OF ENTITIES TO MOVE
    for tree in trees:
        tree.move_x(-dx)
        tree.move_y(-dy)
    # MOVE ENTITIES
    for entity in entities:
        entity.move_x(-dx)
        entity.move_y(-dy)


def camera_keys(entities, trees):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera_move(entities, trees, dy=-4)
    elif keys[pygame.K_s]:
        camera_move(entities, trees, dy=4)
    if keys[pygame.K_a]:
        camera_move(entities, trees, dx=-4)
    elif keys[pygame.K_d]:
        camera_move(entities, trees, dx=4)
