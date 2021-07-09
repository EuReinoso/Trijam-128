import pygame
from pygame.locals import *

from random import randint

pygame.init()

# Utility Stuff ---------------------------------------------------------------------------------#
def xy_range(x_range: tuple, y_range : tuple):
    return [randint(x_range[0], x_range[1]), randint(y_range[0], y_range[0])]

class Obj:
    def __init__(self, x, y, width, height, img= None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img
        self.org_img = img

        if img != None:
            self.set_scale(width, height, original= True)

    def draw_img(self, surface):
        surface.blit(self.img, (self.x, self.y))

    def draw_rect(self, surface, color= (255, 255, 255)):
        pygame.draw.rect(surface, color, self.rect)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def set_scale(self, width, height, original= False):
        self.width = width
        self.height = height

        if self.img != None:
            self.img = pygame.transform.scale(self.org_img, (width, height))

            if original:
                self.org_img = pygame.transform.scale(self.org_img, (width, height))

    def set_img(self, img):
        self.img = img
        self.org_img = img
        self.set_scale(self.width, self.height, original= True)
    
    def set_colorkey(self, colorkey= (255, 255, 255)):
        self.img.set_colorkey(colorkey)
        self.org_img.set_colorkey(colorkey)

# Particles -------------------------------------------------------------------------------------------------#
def create_particles(quant, x, y, x_motion_range= (-10, 10), y_motion_range = (-10, -5), width_range= (5, 10), height_range =(5, 10), decrease= 0.1, gravity= 1, img=None, color= (255, 255, 255)):
    particles_list = []
    for i in range(quant):
        particle_size   = xy_range((width_range[0], width_range[1]), (height_range[0], height_range[1]))
        particle_motion = xy_range((x_motion_range[0], x_motion_range[1]), (y_motion_range[0], y_motion_range[1]))
        particle        = Particle(x, y, particle_size[0], particle_size[1], motion_x= particle_motion[0], motion_y= particle_motion[1], decrease= decrease, gravity= gravity, img= img, color= color)
        particles_list.append(particle)

    return particles_list

def create_particle(x, y, x_motion_range= (-5, 5), y_motion_range = (-10, -2), width_range= (5, 10), height_range =(5, 10), decrease= 0.1, gravity= 1, img= None, color= (255, 255, 255)):
    particle_size   = xy_range((width_range[0], width_range[1]), (height_range[0], height_range[1]))
    particle_motion = xy_range((x_motion_range[0], x_motion_range[1]), (y_motion_range[0], y_motion_range[1]))
    
    return Particle(x, y, particle_size[0], particle_size[1], motion_x= particle_motion[0], motion_y= particle_motion[1], decrease= decrease, gravity= gravity, img= img, color= color)
    

def particles_update(particles_list : list):
    for i, particle in sorted(enumerate(particles_list), reverse= True):
        particle.update()
        if particle.width < 0 or particle.height < 0:
                particles_list.pop(i)
    

class Particle(Obj):
    def __init__(self, x, y, width, height, motion_x= 0, motion_y= 0, decrease = 0.1, gravity= 1, img= None, color= (255, 255,255)):
        super().__init__(x, y, width, height, img)
        self.motion_x = motion_x
        self.motion_y = motion_y
        self.decrease = decrease
        self.gravity = gravity
        self.y_momentum = 0
        self.color = color

    def draw_circle(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), int((self.width + self.height)/2))
    
    def update(self):
        self.y_momentum += self.gravity
        self.x += self.motion_x
        self.y += self.motion_y + self.y_momentum
        self.width -= self.decrease
        self.height -= self.decrease

            


