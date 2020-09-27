from pygame import display, mouse
import game_objects
from config import Config

def editor(screen, config):
    disk_placed = False
    basket_placed = False
    saved = False

    track = game_objects.Object(config.TRACK_1, path=os.path.join(config.TRACK_PATH, "track_1"))
    track.scale(( round(track.asset_size[0]*2), round(track.asset_size[1]*2) ))
    track.pos(x=config.SCREEN_SIZE[0]/2, y=config.SCREEN_SIZE[1]/2)

    disk = disk = game_objects.Object(config.DISK, colorkey=config.BLUE)
    disk.scale((disk.asset_size[0]//2, disk.asset_size[1]//2))

    trees = []

    while not saved:
        if disk_placed == False:
            mouse_x, mouse_y = mouse.get_pos()
            disk.pos(mouse_x, mouse_y)
            disk.draw(screen)
            current_events = pygame.event.get()
            for event in current_events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    disk_placed = True
                    basket = game_objects.Object(config.BASKET, x=basket_xy[0], y=basket_xy[1], colorkey=config.BLUE)
                    basket.scale((64, 64))
        elif basket_placed == False:
            mouse_x, mouse_y = mouse.get_pos()
            basket.pos(mouse_x, mouse_y)
            basket.draw(screen)
            current_events = pygame.event.get()
            for event in current_events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    basket_placed = True
                    trees.append(game_objects.Object(config.TREE, colorkey=config.BLUE))
        else:
            mouse_x, mouse_y = mouse.get_pos()
            trees[-1].pos(mouse_x, mouse_y)
            current_events = pygame.event.get()
            for event in current_events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    trees.append(game_objects.Object(config.TREE, colorkey=config.BLUE))
            
        if disk_placed and basket_placed:
            for tree in trees:
                tree.draw(screen)

        # entities=[track, basket, disk]
        # CHECK PRESSED KEYS
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                camera_move(dy=-2)
            elif keys[pygame.K_s]:
                camera_move(dy=2)
            if keys[pygame.K_a]:
                camera_move(dx=-2)
            elif keys[pygame.K_d]:
                camera_move(dx=2)
            
            if keys in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
                saved=True
        display.update()
        clock.tick(60)

def load_track(name="track_0", hole_number=0):
    f = open( os.path.join(config.TRACK_PATH, name, "track") ,'r' )
    holes = f.readlines()
    hole = holes[hole_number].split(' ')
    par = int(hole.pop(0))
    track = [int(i) for i in hole.pop(0).split(':', 1)]
    disk = [int(i) for i in hole.pop(0).split(':', 1)]
    basket = [int(i) for i in hole.pop(0).split(':', 1)]
    trees = []
    f.close()
    for _ in hole:
        trees.append( [int(i) for i in hole.pop(0).split(':')] )
    return par, track, disk, basket, trees

def camera_move(entities, trees, dx=0, dy=0):
    # BUILD A LIST OF ENTITIES TO MOVE
    for tree in trees:
        entities.append(tree)
    # MOVE ENTITIES
    for entity in entities:
        entity.move_x(-dx)
        entity.move_y(-dy)