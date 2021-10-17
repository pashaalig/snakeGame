import pygame
from pygame.locals import *
import  time
import random
SIZE = 40


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image= pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE*7
        self.y = SIZE*7

    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))
        pygame.display.flip()

    # movement of food to random location
    def move(self):
        self.x = random.randint(1,19)*SIZE
        self.y = random.randint(1,14)*SIZE



class Snake:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.block=pygame.image.load("resources/block.jpg").convert()
        self.length = 1
        self.x = [random.randint(1,19)*SIZE]*self.length
        self.y = [random.randint(1,14)*SIZE]*self.length
        self.direction = 'null'

    # turn of snake body
    def move_left(self):
        self.direction = 'left'
    def move_right(self):
        self.direction = 'right'
    def move_up(self):
        self.direction = 'up'
    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # movement of snake's body except snake's head
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # movement of snake's head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self. direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):

        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Play With Pasha")
        pygame.mixer.init()
        self.speed_increase = 0.3
        self.surface=pygame.display.set_mode((800,600))
        self.snake=Snake(self.surface)
        self.snake.draw()
        self.apple=Apple(self.surface)
        self.apple.draw()
        self.background_music()


    def game_over(self):
        self.background_image()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}",True, (207, 25, 46))
        self.surface.blit(line1,(150,150))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (207, 25, 46))
        self.surface.blit(line2,(150,200))

        pygame.display.flip()
        pygame.mixer.music.pause()

    def background_image(self):
        self.bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(self.bg,(0,0))

    def reset(self):
        self.snake=Snake(self.surface)
        self.apple=Apple(self.surface)

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length-1}", True, (252,3,136))

        self.surface.blit(score, (680, 10))

    def background_music(self):
        pygame.mixer.music.load("resources/bg.music.mp3")
        pygame.mixer.music.play(-1,0)

    def play_sound(self,sound_name):
            sound = pygame.mixer.Sound(f"resources/{sound_name}.mp3")
            pygame.mixer.Sound.play(sound)


    def increase_speed(self):
        if self.snake.length-1 == 10:
            self.speed_increase = 0.25
        elif self.snake.length-1 == 15:
            self.speed_increase = 0.20
        elif self.snake.length - 1 == 20:
            self.speed_increase = 0.15
        elif self.snake.length - 1 == 25:
            self.speed_increase = 0.10
        elif self.snake.length - 1 == 30:
            self.speed_increase = 0.08
        elif self.snake.length - 1 == 35:
            self.speed_increase = 0.06
        elif self.snake.length - 1 == 40:
            self.speed_increase = 0.05


    def play(self):
        self.background_image()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        self.increase_speed()
        pygame.display.flip()

        # snake colliding with food
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.play_sound("maza")


            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(2,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("marna")
                raise "collision occured"

        # when snake colliding with the boundries of the window then game is over
        # if not (0 <= self.snake.x[0] <= 800 and 0 <= self.snake.y[0] <= 600):
        #     self.play_sound('marna')
        #     raise "Hit the boundry error"


        """" when snake colliding with the boundries of the window then game is not over(means snake's head comes from 
             opposite boundaries )"""
        if self.snake.x[0] > 760:
            self.snake.x[0] = -40
        if self.snake.x[0] < -40:
            self.snake.x[0] = 800
        if self.snake.y[0] > 560:
            self.snake.y[0] = -40
        if self.snake.y[0] < -40:
            self.snake.y[0] = 600



    def is_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1>= y2 and y1 < y2 + SIZE:
                return True
        return  False


    def run(self):

        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()
                    if not pause:
                        if event.key == K_LEFT:
                            if self.snake.direction != "right":
                                self.snake.move_left()

                        if event.key == K_RIGHT:
                            if self.snake.direction != "left":
                                self.snake.move_right()

                        if event.key == K_UP:
                            if self.snake.direction != "down":
                                self.snake.move_up()

                        if event.key == K_DOWN:
                            if self.snake.direction != "up":
                                self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.game_over()
                self.speed_increase = 0.3
                pause = True
                self.reset()
            time.sleep(self.speed_increase)




if __name__ == "__main__":
    game=Game()
    game.run()