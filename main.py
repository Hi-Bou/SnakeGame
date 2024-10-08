import pygame
import sys
import os
import random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.alive = True
        self.game_started = False
        print(self.alive)
        self.load_files()

    def load_files(self):
        self.head_up = pygame.image.load(resource_path('Graphics/snake/head_up.png')).convert_alpha()
        self.head_down = pygame.image.load(resource_path('Graphics/snake/head_down.png')).convert_alpha()
        self.head_right = pygame.image.load(resource_path('Graphics/snake/head_right.png')).convert_alpha()
        self.head_left = pygame.image.load(resource_path('Graphics/snake/head_left.png')).convert_alpha()

        self.tail_up = pygame.image.load(resource_path('Graphics/snake/tail_up.png')).convert_alpha()
        self.tail_down = pygame.image.load(resource_path('Graphics/snake/tail_down.png')).convert_alpha()
        self.tail_right = pygame.image.load(resource_path('Graphics/snake/tail_right.png')).convert_alpha()
        self.tail_left = pygame.image.load(resource_path('Graphics/snake/tail_left.png')).convert_alpha()

        self.body_vertical = pygame.image.load(resource_path('Graphics/snake/body_vertical.png')).convert_alpha()
        self.body_horizontal = pygame.image.load(resource_path('Graphics/snake/body_horizontal.png')).convert_alpha()

        self.body_tr = pygame.image.load(resource_path('Graphics/snake/body_tr.png')).convert_alpha()
        self.body_tl = pygame.image.load(resource_path('Graphics/snake/body_tl.png')).convert_alpha()
        self.body_br = pygame.image.load(resource_path('Graphics/snake/body_br.png')).convert_alpha()
        self.body_bl = pygame.image.load(resource_path('Graphics/snake/body_bl.png')).convert_alpha()
        self.crunch_sound = pygame.mixer.Sound(resource_path('Sounds/crunch.wav'))

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.alive and self.game_started:
            if self.new_block == True:
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:]
                self.new_block = False
            else:
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size), flags=pygame.RESIZABLE)
        self.end_is_playing = False
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.alive = True
        print(self.alive + self.end_is_playing)

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.load_files()
        self.end_is_playing = False

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def load_files(self):
        #images
        self.bob1 = pygame.image.load(resource_path('Graphics/end/bob1.png')).convert_alpha()
        self.bob2 = pygame.image.load(resource_path('Graphics/end/bob2.png')).convert_alpha()
        self.bob3 = pygame.image.load(resource_path('Graphics/end/bob3.png')).convert_alpha()
        self.bob4 = pygame.image.load(resource_path('Graphics/end/bob4.png')).convert_alpha()
        self.bob5 = pygame.image.load(resource_path('Graphics/end/bob5.png')).convert_alpha()
        self.bob6 = pygame.image.load(resource_path('Graphics/end/bob6.png')).convert_alpha()
        self.bob7 = pygame.image.load(resource_path('Graphics/end/bob7.png')).convert_alpha()
        self.bob8 = pygame.image.load(resource_path('Graphics/end/bob8.png')).convert_alpha()
        self.bob9 = pygame.image.load(resource_path('Graphics/end/bob9.png')).convert_alpha()
        self.cow1 = pygame.image.load(resource_path('Graphics/end/cow.png')).convert_alpha()
        self.flash = pygame.image.load(resource_path('Graphics/end/flash.png')).convert_alpha()
        self.beer = pygame.image.load(resource_path('Graphics/beer.png')).convert_alpha()
        #sounds
        self.bang = pygame.mixer.Sound(resource_path('Sounds/BANG.wav'))
        self.symphony = pygame.mixer.Sound(resource_path('Sounds/SYMPHONYYYYY.wav'))
        self.seeitcoming = pygame.mixer.Sound(resource_path('Sounds/youllNeverSeeItCOMIIIIING.wav'))

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not(self.snake.alive and self.snake.game_started):
            return
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    def game_over(self):
        pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size), flags=pygame.NOFRAME)
        self.snake.alive = False
        self.snake.game_started = False
        self.end_is_playing = True
        self.channel = self.end()

    def end(self):
        chance = random.randint(0, 100)
        if chance < 90:
            bob_images = [self.bob1, self.bob2, self.bob3, self.bob4, self.bob5, self.bob6, self.bob7, self.bob8, self.bob9, self.cow1]
            selected_bob = random.choice(bob_images)
            self.end_pic = selected_bob
            sound = pygame.mixer.Sound(self.seeitcoming)
            sound.set_volume(0.05)
            channel = sound.play()
        else:
            self.end_pic = self.beer
            sound = pygame.mixer.Sound(self.symphony)
            sound.set_volume(0.05)
            channel = sound.play()
        return channel

    def do_end(self):
        left = (screen.get_width() - self.end_pic.get_width()) // 2
        top = (screen.get_height() - self.end_pic.get_height()) // 2
        end_rect = pygame.Rect(left, top, screen.get_width(), screen.get_height())
        screen.blit(self.end_pic, end_rect)
        if not self.channel.get_busy():
            self.end_is_playing = False
            self.snake.reset()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load(resource_path('Graphics/apple.png')).convert_alpha()
game_font = pygame.font.Font(resource_path('Font/PoetsenOne-Regular.ttf'), 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN and main_game.snake.alive:
            main_game.snake.game_started = True
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1 and main_game.snake.direction != Vector2(0, 0):
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    if main_game.end_is_playing:
        main_game.do_end()
    else:
        main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)