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
        self.life = 3

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

class Bullet(Particle):
    def __init__(self, x, y, width, height, motion_x= 0, motion_y= 0, decrease = 0.1, gravity= 1, img= None, color= (255, 255,255)):
        super().__init__(x, y, width, height, img = img,  motion_x= motion_x, motion_y= motion_y, decrease = decrease, gravity= gravity, color= color)

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
canon_aceleration = 0.001

player_size = [100, 120]
player_pos = [WINDOW_SIZE[0] * 0.5, ground_pos[1] - player_size[1]]
player = Player(player_pos[0], player_pos[1], player_size[0], player_size[1], x_vel= 0.15, img= player_img)
player.action = 'idle'

apple_list = []
apple_size = [50, 50]
apple_timer_range = [120, 240]
apple_timer = randint(apple_timer_range[0], apple_timer_range[1])
apple_ticks = 0

bomb_list = []
bomb_size = [64, 60]
bomb_timer_range = [340, 560]
bomb_timer = randint(bomb_timer_range[0], bomb_timer_range[1])
bomb_ticks = 0

motion_range = [(2, 15), (-20, -5)]

particles = []
canon_particles = []

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
        apple_timer = randint(apple_timer_range[0], apple_timer_range[1])
        apple_motion = xy_range(motion_range[0], motion_range[1])
        apple = Bullet(canon.x + canon.width, canon.y, apple_size[0], apple_size[1], img= apple_img, motion_x = apple_motion[0], motion_y= apple_motion[1], gravity= 0.5)
        apple_list.append(apple)
        canon.shot_anim()
        canon_particles.append(create_particles(5, canon.x + canon.width, canon.y, x_motion_range= (2, 5), y_motion_range= (-2, 2), gravity= 0, decrease= 0.2))
        canon_particles.append(create_particles(5, canon.x + canon.width, canon.y, x_motion_range= (2, 5), y_motion_range= (0, 3), gravity= 0, decrease= 0.2))

    if len(apple_list) > 0:
        for i, apple in sorted(enumerate(apple_list), reverse= True):
            apple.update_img()
            apple.draw_img(window)
            particles.append(create_particle(apple.x + apple.width/2, apple.y + apple.height/2, width_range= (2, 3), height_range= (2,3), color= (255, 0, 0)))
            #parede direita
            if apple.x >= WINDOW_SIZE[0] - apple.width:
                apple.motion_x *= -1
                apple.motion_x *= 0.99
                apple.x = WINDOW_SIZE[0] - apple.width - 1

            #parede esquerda        
            if apple.x <= 0:
                apple.motion_x *= -1
                apple.motion_x *= 0.99
                apple.x = 1
            #teto
            if apple.y <= 0:
                apple.motion_y *= -1

            #colide player
            if apple.rect.colliderect(player.rect) and apple.motion_y > 0:
                apple_list.pop(i)
                player.score += 1
            else:
                #colisão com chão e sair do mapa
                if apple.rect.colliderect(ground.rect) or apple.y > WINDOW_SIZE[1]:
                    apple_list.pop(i)

    #bomb
    bomb_ticks += 1
    if bomb_ticks >= bomb_timer:
        bomb_ticks = 0
        bomb_timer = randint(bomb_timer_range[0], bomb_timer_range[1])
        bomb_motion = xy_range(motion_range[0], motion_range[1])
        bomb = Bullet(canon.x + canon.width, canon.y, bomb_size[0], bomb_size[1], img= bomb_img, motion_x = bomb_motion[0], motion_y= bomb_motion[1], gravity= 0.5)
        bomb_list.append(bomb)
        canon.shot_anim()
        canon_particles.append(create_particles(5, canon.x + canon.width, canon.y, x_motion_range= (2, 5), y_motion_range= (-2, 2), gravity= 0, decrease= 0.2))
        canon_particles.append(create_particles(5, canon.x + canon.width, canon.y, x_motion_range= (2, 5), y_motion_range= (0, 3), gravity= 0, decrease= 0.2))
    
    for i, bomb in sorted(enumerate(bomb_list)):
        bomb.update_img()
        bomb.draw_img(window)
        particles.append(create_particle(bomb.x + bomb.width/2, bomb.y + bomb.height/2, width_range= (3,4), height_range= (3,4)))

        #parede direita
        if bomb.x >= WINDOW_SIZE[0] - bomb.width:
            bomb.motion_x *= -1
            bomb.motion_x *= 0.99
            bomb.x = WINDOW_SIZE[0] - bomb.width - 1

        #parede esquerda        
        if bomb.x <= 0:
            bomb.motion_x *= -1
            bomb.motion_x *= 0.99
            bomb.x = 1
        #teto
        if bomb.y <= 0:
            bomb.motion_y *= -1

        #colide player
        if bomb.rect.colliderect(player.rect) and bomb.motion_y > 0:
            bomb_list.pop(i)
            player.life -= 1
        else:
            #colisão com chão e sair do mapa
            if bomb.rect.colliderect(ground.rect) or bomb.y > WINDOW_SIZE[1]:
                bomb_list.pop(i)

    #canon
    canon.draw_img(window)
    canon.update()
    particles.append(create_particle(canon.x, canon.y + canon.height/2 + 15, width_range= (2, 3), height_range= (2,3), gravity= 0))

    # move canon
    canon.x += canon_xvel
    canon_xvel += canon_aceleration
    if canon.x >= WINDOW_SIZE[0] - canon.width:
        canon_xvel *= - 1
        canon_aceleration *= -1
    elif canon.x <= 0:
        canon_xvel *= - 1
        canon_aceleration *= -1

    #particles
    for i, particle_list in sorted(enumerate(canon_particles), reverse= True):
        for j, particle in sorted(enumerate(particle_list), reverse= True):
            particle.draw_circle(window)
            particle.update_circle()

            if particle.width <= 0 or particle.height <= 0:
                particle_list.pop(j)
        if len(particle_list) <= 0:
            canon_particles.pop(i)

    for i, particle in sorted(enumerate(particles), reverse= True):
        particle.draw_circle(window)
        particle.update_circle()

        if particle.width <= 0 or particle.height <= 0:        
            particles.pop(i)

    #player
    player.draw_img(window)
    player.update()
    if player.x > WINDOW_SIZE[0] - player.width:
        player.x = WINDOW_SIZE[0] - player.width
        player.x_momentum = 0
    if player.x < 0:
        player.x = 0
        player.x_momentum = 0
    
    #ground
    ground.draw_img(window)


    draw_text(window, 'Score:' + str(player.score), 10, 10, 30, font= 'assets/Comodore64.TTF')
    pygame.display.update()
    clock.tick(fps)