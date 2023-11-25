import pygame
import time
from pygame.locals import *
import random

# size of block, called in x and y of block
SIZE = 40
BACKGROUND = (3, 2, 2)
BACKGROUND_MUSIC = "Images/Hitman.mp3"

# draws apple and has to be *3 (multiple of size of snake block)


class Apple:
    def __init__(self, parent_screen):
        apple_pic = pygame.image.load("Images/apple.png")
        self.apple = pygame.transform.scale(apple_pic, (40, 40)).convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.update()

    # moves apple when snake hits it
    # Screen x divided by x size = x increments (1000/40=25)
    # Screen y divided by y size = y increments (800/40=20)
    # multiply by 40 to be multiple of 40
    # we restrict apple to appear on screen
    def move(self):
        self.x = random.randint(0, 24)*SIZE
        self.y = random.randint(2, 19)*SIZE


class Snake:
    # constructor has parameter parent_screen to show where snake is drawn
    def __init__(self, parent_screen, length):
        #  attribute to be used in draw func
        self.parent_screen = parent_screen
        # block of snake body loaded
        self.block = pygame.image.load("Images/block.jpg").convert()

        # length attribute for snake character
        self.length = length
        # initial position of snake block (top left), creates an array to make length of snake
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        # initial direction for snake
        self.direction = "down"

    # adds block everytime snake eats apple add element to array of coordinates
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        # background of screen everytime a new block is drawn (resets)
        # draws new block at updated position from each movement, updates display
        # draws 5 blocks of snake body from length array
        self.parent_screen.fill(BACKGROUND)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    def move_left(self):
        # this calls direction function which uses draw func
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def speed(self):
        # reverse for loop, to assign each block to previous one with step -1
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # new coordinates to draw depending on direction of snake
        # use size because distance between each block needs to be of the size before drawn
        if self.direction == "down":
            self.y[0] += SIZE
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "left":
            self.x[0] -= SIZE

        self.draw()


class Game:
    def __init__(self):
        # initializes pygame
        pygame.init()
        pygame.display.set_caption("SNAKE GAME")
        # sound module is initialized
        pygame.mixer.init()
        self.play_background_music()
        # creates window dimensions and fills background w/ color initially
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill(BACKGROUND)
        # calls snake class and passes into parent_screen parameter the self.surface
        self.snake = Snake(self.surface, 1)
        # calls the draw for it to happen
        self.snake.draw()
        # calls apple class and calls draw function of apple class
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_touch(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False


    def play_sound(self,sound):
        if sound == "sound1":
            sound1 = pygame.mixer.Sound("Images/eat.mp3")
            pygame.mixer.Sound.play(sound1)
        elif sound == "sound2":
            sound2 = pygame.mixer.Sound("Images/lose.mp3")
            pygame.mixer.Sound.play(sound2)

    def play_background_music(self):
        pygame.mixer.music.load(BACKGROUND_MUSIC)
        pygame.mixer.music.play()

    def play(self):
        # To have the snake moving by itself and wasd change direction
        # Is called when program is run and starts with direction down, moves with no user input
        self.snake.speed()
        self.apple.draw()
        self.display_score()
        pygame.display.update()

        # makes sure game over when hits bounds
        if self.snake.x[0] < 0 or self.snake.x[0] >= 1000:
            self.play_sound("sound2")
            raise Exception("Game Over")
        if self.snake.y[0] < 0 or self.snake.y[0] >= 800:
            self.play_sound("sound2")
            raise Exception("Game Over")

        # when snake hits the apple, snake head is at index 0
        if self.is_touch(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("sound1")
            self.snake.increase_length()
            self.apple.move()

        # snake hits itself, only does so when length is at least 3
        for i in range(3, self.snake.length):
            if self.is_touch(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("sound2")
                # raises the exception to be called later
                raise "Game Over"

    # calls font of score
    # This will show the length of the snake
    def display_score(self):
        font = pygame.font.SysFont('c', 30)
        score = font.render(f'Score: {self.snake.length}', True, (200, 200, 200))
        self.surface.blit(score, (890, 10))

    # this is called when user loses, displays text and renders it then calls it on screen using blit
    def show_game_over(self):
        self.surface.fill(BACKGROUND)
        font = pygame.font.SysFont('c', 30)
        line1 = font.render(f'Score: {self.snake.length}', True, (200, 200, 200))
        self.surface.blit(line1, (460, 300))
        line2 = font.render("TO RESTART THE GAME, PRESS SPACE!", True, (200, 200, 200))
        self.surface.blit(line2, (310, 350))  # Change line1 to line2
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    # when program is ran, we keep window open until exit or esc button hit
    # pause is when you lose, pauses to display, so game doesn't run again
    def run(self):
        running = True
        pause = False

        while running:
            # for every input of a user, perform an action
            for event in pygame.event.get():
                # if keyboard input
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_SPACE:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_w:
                            self.snake.move_up()
                        if event.key == K_s:
                            self.snake.move_down()
                        if event.key == K_a:
                            self.snake.move_left()
                        if event.key == K_d:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            # don't play game if it is paused, so doesn't take user keyboard input
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            # Slows down the speed of snake to make game playable
            time.sleep(0.07)

# main, starts game by calling game class and calling run


if __name__ == "__main__":
    game = Game()
    game.run()

