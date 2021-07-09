import pygame
from pygame.locals import *

from random import randint

pygame.init()

#globals
animation_img_data = {}
animation_frame_data = {}
fps = 60
clock = pygame.time.Clock()

# Utility Stuff ---------------------------------------------------------------------------------#
def xy_range(x_range: tuple, y_range : tuple) -> list:
    return [randint(x_range[0], x_range[1]), randint(y_range[0], y_range[0])]

def load_img(path, colorkey= (255, 255, 255)):
    image = pygame.image.load('assets/images/' + path + '.png').convert()
    image.set_colorkey(colorkey)
    return image

def create_animation_data(images : list, anim_name : str, frames_sequence : list) -> list:
    global animation_img_data
    animation_data = []
    n = 0
    for seq in frames_sequence:
        anim_id = anim_name + '_' + str(n)
        animation_img_data[anim_id] = images[n].copy()
        for i in range(seq):
            animation_data.append(anim_id)
        n += 1
    
    return animation_data

def frame_update(frame, frames):
        frame += 1
        if frame >= frames:
            frame = 0
        return frame

def add_animation_frame(images : list, anim_name : str, frames_sequence : list):
    global animation_frame_data
    animation_frame_data[anim_name] = create_animation_data(images, anim_name, frames_sequence)

def change_action_frame(actual_action, frame, new_action):
    actual_action = new_action
    frame = 0
    return actual_action, frame

class Obj:
    def __init__(self, x, y, width, height, img= None, color= (255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img
        self.org_img = img
        self.color = color

        if img != None:
            self.set_scale(width, height, original= True)

    def draw_img(self, surface):
        surface.blit(self.img, (self.x, self.y))

    def draw_rect(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
    
    def draw_circle(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), int((self.width + self.height)/2))

    @property
    def rect(self) -> pygame.Rect:
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
    
    def collide_test(self, objs):
        hit_list = []
        for obj in objs:
            if self.rect.colliderect(obj.rect):
                hit_list.append(obj)
        return hit_list

class Particle(Obj):
    def __init__(self, x, y, width, height, motion_x= 0, motion_y= 0, decrease = 0.1, gravity= 1, img= None, color= (255, 255,255)):
        super().__init__(x, y, width, height, img)
        self.motion_x = motion_x
        self.motion_y = motion_y
        self.decrease = decrease
        self.gravity = gravity
        self.color = color

    def update_img(self):
        self.motion_y += self.gravity
        self.x += self.motion_x 
        self.y += self.motion_y
    
    def update_circle(self):
        self.motion_y += self.gravity
        self.x += self.motion_x
        self.y += self.motion_y 
        self.width -= self.decrease
        self.height -= self.decrease

# Particles Stuff -------------------------------------------------------------------------------------------------#

def create_particle(x, y, x_motion_range= (-5, 5), y_motion_range = (-10, -2), width_range= (5, 10), height_range =(5, 10), decrease= 0.1, gravity= 1, img= None, color= (255, 255, 255)) -> Particle:
    particle_size   = xy_range((width_range[0], width_range[1]), (height_range[0], height_range[1]))
    particle_motion = xy_range((x_motion_range[0], x_motion_range[1]), (y_motion_range[0], y_motion_range[1]))
    
    return Particle(x, y, particle_size[0], particle_size[1], motion_x= particle_motion[0], motion_y= particle_motion[1], decrease= decrease, gravity= gravity, img= img, color= color)
    
def create_particles(quant, x, y, x_motion_range= (-10, 10), y_motion_range = (-10, -5), width_range= (5, 10), height_range =(5, 10), decrease= 0.1, gravity= 1, img=None, color= (255, 255, 255)) -> list:
    particles_list = []
    for i in range(quant):
        particle_size   = xy_range((width_range[0], width_range[1]), (height_range[0], height_range[1]))
        particle_motion = xy_range((x_motion_range[0], x_motion_range[1]), (y_motion_range[0], y_motion_range[1]))
        particle        = Particle(x, y, particle_size[0], particle_size[1], motion_x= particle_motion[0], motion_y= particle_motion[1], decrease= decrease, gravity= gravity, img= img, color= color)
        particles_list.append(particle)

    return particles_list

def particles_update(particles_list : list):
    for i, particle in sorted(enumerate(particles_list), reverse= True):
        particle.update()
        if particle.width < 0 or particle.height < 0:
                particles_list.pop(i)
    



            


