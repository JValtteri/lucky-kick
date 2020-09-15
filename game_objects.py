import math
import pygame
import random
# import config
import os


class Object():
    """
    class to track and manipulate rendered entities.
    """

    def __init__(
                self,
                image,
                x = 0,
                y = 0,
                v = 0,
                vect = (0,0),
                path = 'assets',
                expire = False,
                time = -1,
                visible = True,
                colorkey = False
                ):

        self.visible = visible
        self.asset = pygame.image.load( os.path.join(path, image) ).convert()
        self.asset_size = (self.asset.get_width(), self.asset.get_height())
        self.image = self.asset
        self.rect = self.image.get_rect(center = (x, y))
        self.colorkey = colorkey
        self.x = x
        self.y = y
        self.v = v
        self.u_vect = 0
        self.time = time
        self.expire = expire

        self.u_vector(vect)
        if colorkey != False:
            self.set_colorkey(colorkey)

    def pos(self, x, y):
        """set entity center to position (x, y)"""
        self.x = x
        self.y = y
        print('x:{} y:{}'.format(x, y))
        self.rect.centerx = x
        self.rect.centery = y

    def move_x(self, delta = None):
        """
        move entity in x-axis at predefined speed.
        Speed can be overriden with [delta]"""
        if delta == None:
            delta = self.v
        self.x += delta
        self.rect.centerx = self.x
        return self.x

    def move_y(self, delta = None):
        """
        move entity in y-axis at predefined speed.
        Speed can be overriden with [delta]"""
        if delta == None:
            delta = self.v
        self.y += delta
        self.rect.centery = self.y
        return self.y

    def move_2d(self):
        """updates the entity location according to
        its pre-defined speed and direction"""
        self.move_x(self.v * self.u_vect[0])
        self.move_y(self.v * self.u_vect[1])

    def scale(self, scale):
        """resize image to scale = (x, y)"""
        self.image = pygame.transform.scale(self.asset, scale)
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def rotate(self, vect):
        """returns a surface rotated along vect"""
        angle = math.degrees( math.atan(vect[0]/vect[1]) )
        self.image = pygame.transform.rotate(self.asset, angle)

    def speed(self, v = 0):
        """set entity speed"""
        self.v = v

    def u_vector(self, vect):
        """
        Updates the entity unit vector.
        Used to calculate entity speed in
        (x, y) plane: d(x, y) = u_vect(x,y) * v"""
        x = vect[0]
        y = vect[1]
        l = math.sqrt( x**2 + y**2 )
        try:
            vx = x / l
        except ZeroDivisionError:
            vx = 0
        try:
            vy = y / l
        except ZeroDivisionError:
            vy = 0

        self.u_vect = (vx, vy)
        return (vx, vy)

    def draw(self, screen):
        """render entities that are set to visible"""
        if self.visible == True and self.time is not 0:
            screen.blit(self.image,(self.rect))
            if self.time > 0:
                self.time -= 1

    def show(self, time=None):
        """
        set entity visibile for [time] frames.
        time: 0 = hide, -1 = does not expire, 0 != show
        """
        self.time = time
        self.visible = True

    def hide(self):
        """make entity invisible"""
        self.visible = False

    def splash(self, splash):
        """Changes entity graphic to [splash]"""
        self.image = splash

    def is_garbage(self):
        '''
        use:
        list_of_objects = [[object] for [object] in [objects] if not [object].is_garbage()]
        '''
        return self.expire == True and self.time == 0

    def set_colorkey(self, key=None):
        """set transparency colour"""
        if key != None:
            self.image.set_colorkey(key)
        else:
            self.image.set_colorkey(self.colorkey)


class Actor(Object):

    def __init__(self, image, config, dist= 10, angle= random.randrange(180)):

        Object.__init__(self, image)

        self.dist = None
        self.angle = angle
        self.scale_factor = None

        self.set_dist(config, 10)
        self.set_angle(config, angle)

    def set_angle(self, config, andgle=None):
        if andgle == None:
            andgle = self.angle
        print(config.SCREEN_SIZE[1] / 90 * andgle)
        self.pos(config.SCREEN_SIZE[1] / 90 * andgle, config.SCREEN_SIZE[1] / 5 * 3)

    def set_dist(self, config, meters):
        self.dist = meters
        if meters >= 0.5:
            self.scale_factor = 1 / self.dist
            result = True
        else:
            self.dist = 0.5
            self.scale_factor = 1 / self.dist
            result = False

        new_width = round(self.asset_size[0] * self.scale_factor)
        new_height = round(self.asset_size[0] * self.scale_factor)
        self.scale((new_width, new_height))
        self.rect = self.image.get_rect(center = (self.x, self.y))
        return result

    def move_dist(self, config, delta):
        dist = self.dist + delta
        self.set_dist(config, dist)
        return self.dist


class Texts():

    def __init__(self, font, message="[insert text]", size=40, color=(225,225,225), xy=(0, 0), path='assets' ):
        self.game_font = pygame.font.Font( os.path.join(path, font) , size)
        self.message = message
        self.surface = self.game_font.render(self.message, True, color)
        self.rect = self.get_rect(xy)

    def get_rect(self, xy):
        rect = self.surface.get_rect(center = xy )
        return rect

    def draw(self, screen):
        screen.blit(self.surface, self.rect)


def vector(end, start=(0, 0) ):
    """
    get a vector between from [start] to [end].
    If ommited, [start] == (0,0)
    """
    delta_x = end[0] - start[0]
    delta_y = end[1] - start[1]

    return (delta_x, delta_y)
