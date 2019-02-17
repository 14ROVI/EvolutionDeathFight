from functools import reduce
import DeepLearning
from DeepLearning import Model as ML
import operator
import random
import pygame
import math
import time





#############################
p_p = [[30,30,315],[770,770,135],[770,30,225],[30,770,45],
       [400,30,0],[400,770,180],[30,400,270],[770,400,90]]
players = pygame.sprite.Group()
bullets = pygame.sprite.Group()
last_players = []
next_players = []
input_size = 200
player_count = 4
gens = 5
#############################





class main(object):
    def __init__(self, width, height):
        """Initialize pygame, window, background, font,...
        """
        self.width = width
        self.height = height
    
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Death Fight")
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        #self.S_font = pygame.font.SysFont('mono', 15, bold=True)
        #self.L_font = pygame.font.SysFont('mono', 100, bold=True)
        self.draw = False


    def start(self, p_m):
        ## Player(group, start_param, x limit, y limit, ai_model)
        ## please do controls in order "up down left right fire rotateLeft rotateRight"
        for val in range(0,len(p_m)):
            ai_player(players, p_p[val], self.width, self.height, p_m[val])


    def frame(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "end"
                if event.key == pygame.K_d:
                    self.draw = not self.draw

        players.update()

        for bullet in bullets:
            bullet.update()

            for player in players:
                dist = math.sqrt((bullet.x-player.x)**2 + (bullet.y-player.y)**2)
                if dist < 100 and bullet.owner != player:
                    player.score += 2
            
                if pygame.sprite.collide_circle(player, bullet):
                    bullet.owner.score += 750
                    player.score -= 500
                    player.save_score()
                    bullet.kill()
                    player.kill()     

        if self.draw:
            self.background.fill((150,150,255))
            bullets.draw(self.background)
            players.draw(self.background)
            
            pygame.display.update()
            self.screen.blit(self.background, (0, 0))
                

        if len(players.sprites()) == 1:
            players.sprites()[0].score += 1500
            players.sprites()[0].save_score()
            return "end"
            





############### player





class ai_player(pygame.sprite.Sprite):
    def __init__(self, group, startXYA, screen_width, screen_height, ai):
        pygame.sprite.Sprite.__init__(self, group)

        self.x, self.y, self.angle, self.speed = startXYA[0], startXYA[1], startXYA[2], 0.5
        self.xmax, self.ymax = screen_width, screen_height
        
        self.original = pygame.image.load("player.png")
        self.image = self.original
        self.rect = self.image.get_rect(center = [self.x, self.y])
        self.radius = 30
        
        self.ai = ai
        self.input_data = [0,0,0,0]

        self.elapsedTimeSinceEvent = 0
        self.tick = 0
        self.score = 0

        self.rotate()
        

    def artifical_intelegence(self):
        ai_data = []
        self_data = self.data()
        ai_data.append(self_data)

        for player in players:
            if player.data() != self_data:
                ai_data.append(player.data())
            
        ai_data.extend([[0,0,0,0,0]] * (player_count-len(ai_data)))
        
        
        for bullet in bullets:
            ai_data.append(bullet.data())
            
        ai_data = [item for sublist in ai_data for item in sublist]
        ai_data.extend([0] * (input_size - len(ai_data)))

        return self.ai.frame(ai_data)


    def update(self):
        self.tick += 1
        
        if self.angle > 360:
            self.angle = 0
        if self.angle < 0:
            self.angle = 360

        self.input_data = self.artifical_intelegence()

        if self.input_data[0] == 1 and self.y > 30: ##up
            self.y -= self.speed
        elif self.input_data[0] == 0 and self.y < self.ymax-30: ##down
            self.y += self.speed
        if self.input_data[1] == 1 and self.x > 30: ##left
            self.x -= self.speed
        elif self.input_data[1] == 0 and self.x < self.xmax-30: ##right
            self.x += self.speed

        if self.input_data[2] == 1: ## rotate left
            self.angle += self.speed
            self.rotate()
        elif self.input_data[2] == 0: ## rotate right
            self.angle -= self.speed
            self.rotate()

        if self.tick > 50:
            if self.input_data[3] == 1:
                self.fire_bullet()
            self.tick = 0

        self.rect = self.image.get_rect(center = [self.x,self.y])


    def rotate(self):
        self.image = pygame.transform.rotate(self.original, self.angle)


    def fire_bullet(self):
        self.score -= 20
        Bullet(bullets, self, self.x, self.y, self.angle)


    def save_score(self):
        entered = False
        index = 0
        for player in last_players:
            if player[1] == self.ai:
                last_players[index][0] = self.score
                entered = True
                    
        if entered == False:
            last_players.append([self.score, self.ai])


    def data(self):
        return [self.x, self.y, self.angle, self.input_data[0], self.input_data[1]]





################### bullet





class Bullet(pygame.sprite.Sprite):
    def __init__(self, group, owner, x, y, angle):
        pygame.sprite.Sprite.__init__(self, group)
        self.owner = owner
        
        self.speed = 1
        self.tick_span = 800
        
        self.angle = math.radians(angle)
        self.vector = [math.cos(self.angle) , math.sin(self.angle)]
        self.x , self.y = x + self.vector[0]*60,   y - self.vector[1]*60

        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect()


    def update(self): 
        self.x = self.x + self.vector[0] * self.speed
        self.y = self.y - self.vector[1] * self.speed

        self.rect = self.image.get_rect(center = [self.x, self.y])

        self.tick_span -= 1
        if self.tick_span <= 0:
            self.kill()


    def data(self):
        return [self.x, self.y, self.angle]




    
############################# epoch





def epoch(generations, player_number):
    game = main(800,800)
    
    for gen in range(0,generations):
        print(str(gen+1)+"....", end="")
        players_now = []

        for add in range(0,player_number):
            players_now.append(next_players[gen*player_number + add])

        game.start(players_now)
        for tick in range(0,10000):
            if game.frame() == "end":
                break

        players.empty()
        bullets.empty()
            
    pygame.quit()





############################# handle data   





def handle(p_count):
    global last_players
    global next_players
    next_players = []
    
    last_players.sort(key = lambda x: x[0], reverse = True)
    last_players[0][1].save(0)
    last_players[1][1].save(1)
    identifier = 2
    
    evolve_number = int(p_count/2 - identifier)
    
    for evolve in range(2, evolve_number, 2):
        last_players[evolve][1].evolve(last_players[evolve+1][1])
        last_players[evolve][1].save(identifier)
        identifier += 1
        

    time.sleep(1)
    DeepLearning.clear()
    time.sleep(1)
    

    for weight in range(0, identifier):
        next_players.append(ML(weight, input_size))

    for fill_up in range(0, p_count - len(next_players)):
        next_players.append(ML(-1, input_size))

    random.shuffle(next_players)





#### START UP!





if __name__ == '__main__':
    for start_new in range(0,5):
        next_players.append(ML(start_new ,input_size))

    for start_new in range(0, gens*player_count - len(next_players)):
        next_players.append(ML(-1, input_size))

    random.shuffle(next_players)
    

    for epochs in range(0, 100):
        last_players = []

        print("======================== EPOCH "+str(epochs+1)+" ========================")
        start = time.time()
        epoch(gens, player_count)
        handle(gens * player_count)
        _time = round(time.time() - start)
        print("\ntime taken:", _time ,"s | best player:", last_players[0][0], "| worst player:", last_players[-1][0])
