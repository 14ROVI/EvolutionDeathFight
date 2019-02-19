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
all_players = pygame.sprite.Group()
active_players = pygame.sprite.Group()
bullets = pygame.sprite.Group()
menu_buttons = pygame.sprite.Group()
last_players = []
next_players = []
input_size = 200
player_count = 4
gens = 1
#############################





class main(object):
    def __init__(self, width, height, window_size):
        """Initialize pygame, window, background, font,...
        """
        self.width = width-window_size
        self.height = height
        self.window_size = window_size
    
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Death Fight")
        self.screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.S_font = pygame.font.SysFont('calibri', 20, bold=True)
        self.M_font = pygame.font.SysFont('centurygothic', 50, bold=True)
        self.L_font = pygame.font.SysFont('centurygothic', 100, bold=True)
        self.draw = False

        self.click = False
        button(menu_buttons, self.width+self.window_size*3/4, 150, 90, 40, [200,200,255], self.S_font, "add", "add_player")
        button(menu_buttons, self.width+self.window_size*1/4, 150, 90, 40, [200,200,255], self.S_font, "remove", "remove_player")
        button(menu_buttons, self.width+self.window_size*3/4, 250, 90, 40, [200,200,255], self.S_font, "add", "add_gen")
        button(menu_buttons, self.width+self.window_size*1/4, 250, 90, 40, [200,200,255], self.S_font, "remove", "remove_gen")



    def start(self, p_m):
        ## Player(group, start_param, x limit, y limit, ai_model)
        ## please do controls in order "up down left right fire rotateLeft rotateRight"
        for val in range(0,len(p_m)):
            ai_player([all_players, active_players], p_p[val], self.width, self.height, p_m[val])


    def frame(self, epoch, gen):
        global player_count
        global gens

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "end"

                if event.key == pygame.K_d:
                    self.draw = not self.draw
                    self.create_text(self.width + self.window_size/2, self.height-30, self.S_font, (200,200,255), "Drawing off")
                    self.screen.blit(self.background, (0, 0))
                    pygame.display.update()

        active_players.update()

        for bullet in bullets:
            bullet.update()

            for player in active_players:
                dist = math.sqrt((bullet.x-player.x)**2 + (bullet.y-player.y)**2)
                if dist < 100 and bullet.owner != player:
                    player.score += 1
            
                    if pygame.sprite.collide_circle(player, bullet):
                        bullet.owner.score += 750
                        player.score -= 500
                        bullet.kill()
                        active_players.remove(player)   

        if self.draw:
            self.background.fill((150,150,255))
            self.create_text(self.width/2, self.height/2, self.L_font, (200,200,255), str(epoch)+"."+str(gen))

            bullets.draw(self.background)
            active_players.draw(self.background)

            self.menu()

            self.screen.blit(self.background, (0, 0))
            pygame.display.update()
                

        if len(active_players.sprites()) == 1:
            active_players.sprites()[0].score += 1500
            return "end"


    def create_text(self, x, y, font, colour, text):
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect(center=(x, y))
        self.background.blit(text_surface,  text_rect.topleft)


    def menu(self):
        pygame.draw.rect(self.background, (100, 100, 100), (self.width,0,self.window_size,self.height))
        pygame.draw.line(self.background, (0, 0, 0), [self.width, 0], [self.width, self.height], 2)

        self.create_text(self.width+self.window_size/2, 30, self.M_font, (200,200,255), "Menu")
        self.create_text(self.width+self.window_size/2, 100, self.S_font, (200,200,255), "Players: "+str(player_count))
        self.create_text(self.width+self.window_size/2, 200, self.S_font, (200,200,255), "Gens: "+str(gens))

        self.create_text(self.width+self.window_size/2, self.height/2, self.M_font, (200,200,255), "Scores")
        for index in range(0, len(all_players)):
            self.create_text(self.width+self.window_size/2, self.height/2+35+20*index, self.S_font, (200,200,255), "Player "+str(index+1)+": "+str(all_players.sprites()[index].score))

        menu_buttons.update(self.background)
            




class button(pygame.sprite.Sprite):
    def __init__(self, group, x, y, width, height, colour, font, text, action):
        pygame.sprite.Sprite.__init__(self, group)
        
        self.x, self.y, self.width, self.height = x, y, width, height
        self.text, self.font, self.action = text, font, action
        self.click = False

        self.colour = colour
        self.hover_colour = []
        self.click_colour = []
        difference = 50
        for c in range(0, len(self.colour)):
            if self.colour[c] <= 255-difference:
                self.hover_colour.append(self.colour[c]+difference)
            else:
                self.hover_colour.append(255)
            if self.colour[c] >= difference:
                self.click_colour.append(self.colour[c]-difference)
            else:
                self.click_colour.append(0)

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.colour)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        

    def update(self, surface):
        self.image.fill(self.colour)

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image.fill(self.hover_colour)

            if pygame.mouse.get_pressed()[0] and self.click == False:
                self.actions()
                self.click = True

        if pygame.mouse.get_pressed()[0] == False:
            self.click = False

        if self.click:
            self.image.fill(self.click_colour)

        surface.blit(self.image, self.rect)
        game.create_text(self.x, self.y, self.font, (0,0,0), self.text)


    def actions(self):
        global player_count
        global gens

        if self.action == "add_player" and player_count < 8:
            player_count += 1
        elif self.action == "remove_player" and player_count > 2:
            player_count -= 1
        if self.action == "add_gen":
            gens += 1
        elif self.action == "remove_gen" and gens > 1:
            gens -= 1
            

############### player





class ai_player(pygame.sprite.Sprite):
    def __init__(self, groups, startXYA, screen_width, screen_height, ai):
        pygame.sprite.Sprite.__init__(self, groups[0], groups[1])

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

        for player in active_players:
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
        self.x , self.y = x + self.vector[0]*30,   y - self.vector[1]*30

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





def epoch(epoch):
    current_count = player_count
    current_gens = gens

    for gen in range(0,current_gens):
        print(str(gen+1)+"....", end="")
        players_now = []

        for add in range(0,current_count):
            players_now.append(next_players[gen*current_count + add])

        game.start(players_now)
        for tick in range(0,10000):
            if game.frame(epoch, gen+1) == "end":
                break

        for player in all_players.sprites():
            player.save_score()

        active_players.empty()
        all_players.empty()
        bullets.empty()

    handle(current_count*current_gens)





############################# handle data   





def handle(last_count):
    global last_players
    global next_players
    next_players = []
    
    last_players.sort(key = lambda x: x[0], reverse = True)
    last_players[0][1].save(0)
    last_players[1][1].save(1)
    identifier = 2
    
    evolve_number = int(last_count/2 - identifier)
    
    for evolve in range(2, evolve_number, 2):
        last_players[evolve][1].evolve(last_players[evolve+1][1])
        last_players[evolve][1].save(identifier)
        identifier += 1
        

    time.sleep(1)
    DeepLearning.clear()
    time.sleep(1)
    

    for weight in range(0, identifier):
        next_players.append(ML(weight, input_size))

    for fill_up in range(0, gens*player_count - len(next_players)):
        next_players.append(ML(-1, input_size))

    random.shuffle(next_players)





#### START UP!





if __name__ == '__main__':


    game = main(1000,800, 200)


    for start_new in range(0,5):
        next_players.append(ML(start_new ,input_size))

    for start_new in range(0, gens*player_count - len(next_players)):
        next_players.append(ML(-1, input_size))

    random.shuffle(next_players)


    for epochs in range(0, 100):
        last_players = []

        print("======================== EPOCH "+str(epochs+1)+" ========================")
        start = time.time()
        epoch(epochs+1)
        _time = round(time.time() - start)
        print("\ntime taken:", _time ,"s | best player:", last_players[0][0], "| worst player:", last_players[-1][0])
