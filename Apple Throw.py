import pygame, sys
from pygame.locals import *
from assets.pgengine import *
from random import randint

pygame.init()

WINDOW_SIZE = (800, 640)
window = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
pygame.display.set_caption('Apple Throw')

#TO PG ENGINE
def load_img(path, colorkey= (255, 255, 255)):
    image = pygame.image.load('assets/images/' + path + '.png').convert()
    image.set_colorkey(colorkey)
    return image

class Player(Obj):
    def __init__(self, x, y, width, height, x_vel = 0.01, img= None):
        super().__init__(x, y, width, height, img)
        self.score = 0
        self.right = False
        self.left = False
        self.frame = 0
        self.x_momentum = 0
        self.x_vel = x_vel
        self.action = None

    def control(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.right = True
            if event.key == pygame.K_LEFT:
                self.left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.right = False
            if event.key == pygame.K_LEFT:
                self.left = False

    def move(self):
        if self.left:
            self.x_momentum -= self.x_vel
            if self.x_momentum > 0:
                self.x_momentum *= 0.9
            return True
        if self.right:
            self.x_momentum +=  self.x_vel
            if self.x_momentum < 0:
                self.x_momentum *= 0.9
            return True
        
        return False

    def update(self):
        self.x += self.x_momentum
        if self.move():
            if self.action !=  'run':
                self.action, self.frame = change_action_frame(self.action, self.frame,'run') 
        else:
            if self.action !=  'idle':
                self.action, self.frame = change_action_frame(self.action, self.frame,'idle')
            self.x_momentum = self.x_momentum * 0.9
        
        #TO PGENGINE   
        self.frame = frame_update(self.frame, len(animation_frame_data[self.action]))
        self.set_img(animation_img_data[animation_frame_data[self.action][self.frame]])

class Canon(Obj):
    def __init__(self, x, y, width, height, x_vel = 0.01, img= None):
        super().__init__(x, y, width, height, img= img)
        self.frame = 0
        self.action = 'shot'
        self.shot_timer = 0

    def shot_anim(self):
        self.shot_timer = len(animation_frame_data['shot'])

    def update(self):
        self.shot_timer -= 1
        if self.shot_timer > 0:
            if self.action != 'shot':
                self.action, self.frame = change_action_frame(self.action, self.frame,'shot')
        else:
            if self.action != 'canon_idle':
                self.action, self.frame = change_action_frame(self.action, self.frame, 'canon_idle')

        self.frame = frame_update(self.frame, len(animation_frame_data[self.action]))
        self.set_img(animation_img_data[animation_frame_data[self.action][self.frame]])

class Apple(Particle):
    def __init__(self, x, y, width, height, motion_x= 0, motion_y= 0, decrease = 0.1, gravity= 1, img= None, color= (255, 255,255)):
        super().__init__(x, y, width, height, img = img,  motion_x= motion_x, motion_y= motion_y, decrease = decrease, gravity= gravity, color= color)
        self.name = 'apple'

#load images
player_anim_imgs = [load_img('player_0'), load_img('player_1'), load_img('player_2')]
player_img = load_img('player_idle')
ground_img = load_img('ground')
canon_imgs = [load_img('canon_0'), load_img('canon_1')]
apple_img  = load_img('apple')
bomb_img   = load_img('bomb')

add_animation_frame(player_anim_imgs, 'run', [3, 2, 3])
add_animation_frame([player_img], 'idle', [60])

add_animation_frame([canon_imgs[1]], 'canon_idle', [60])
add_animation_frame([canon_imgs[1], canon_imgs[0]], 'shot', [3, 15])

#Objs
ground_size = (800, 84)
ground_pos = [0, WINDOW_SIZE[1] - ground_size[1]]
ground = Obj(ground_pos[0], ground_pos[1], ground_size[0], ground_size[1], img= ground_img)

canon_size = (100, 110)
canon_pos = [int(WINDOW_SIZE[0] * 0.01), ground_pos[1] - canon_size[1]]
canon = Canon(canon_pos[0], canon_pos[1], canon_size[0], canon_size[1], img= canon_imgs[0])
canon_xvel = 1

player_size = [100, 120]
player_pos = [WINDOW_SIZE[0] * 0.5, ground_pos[1] - player_size[1]]
player = Player(player_pos[0], player_pos[1], player_size[0], player_size[1], x_vel= 0.15, img= player_img)
player.action = 'idle'

apple_size = [25, 25]
apple_pos = [canon_pos[0] + canon_size[0], canon_pos[1]]

apple_list = []
apple_timer_range = [120, 240]
apple_timer = randint(apple_timer_range[0], apple_timer_range[1])
apple_ticks = 0

loop = True
while loop:

    window.fill((135, 206, 235))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        player.control(event)

    # Apples    
    apple_ticks += 1
    if apple_ticks >= apple_timer:
        apple_ticks = 0
        canon.shot_anim()
        apple_motion = xy_range((2, 15), (-20, -5))
        apple = Apple(canon.x + canon.width, canon.y, apple_size[0], apple_size[1], img= apple_img, motion_x = apple_motion[0], motion_y= apple_motion[1], gravity= 0.5)
        apple_list.append(apple)

    if len(apple_list) > 0:
        for i, apple in sorted(enumerate(apple_list), reverse= True):
            apple.update_img()
            apple.draw_img(window)
            
            #parede direita
            if apple.x >= WINDOW_SIZE[0] - apple.width:
                apple.motion_x *= -1
                apple.motion_x *= 0.99

            #parede esquerda        
            if apple.x <= 0:
                apple.motion_x *= -1
                apple.motion_x *= 0.99
            #teto
            if apple.y <= 0:
                apple.motion_y *= -1
            
            #colisão com chão e sair do mapa
            if apple.rect.colliderect(ground.rect) or apple.y > WINDOW_SIZE[1]:
                apple_list.pop(i)

            #colide player
            if apple.rect.colliderect(player.rect) and apple.motion_y > 0:
                apple_list.pop(i)
        
    ground.draw_img(window)
    canon.draw_img(window)

    # move canon
    canon.x += canon_xvel
    if canon.x >= WINDOW_SIZE[0] - canon.width:
        canon_xvel *= - 1
    elif canon.x <= 0:
        canon_xvel *= - 1

    canon.update()

    player.draw_img(window)
    player.update()
    


    pygame.display.update()
    clock.tick(fps)