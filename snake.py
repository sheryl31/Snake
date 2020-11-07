import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (192, 192, 192)
RED = (204, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 156, 0)

WIDTH = 400
HEIGHT = 400
FONT_SIZE = 20

SCORE = "Your Score: "
HIGH_SCORE = "High Score: "
GAME_LOST = "You lost! Press Q-Quit or P-Play again"
CALIBRI = "Calibri"


class Snake:
    snake_block_ = 10
    snake_speed_ = 10

    def __init__(self, display):
        self.x_ = display.width_ / 2
        self.y_ = display.height_ / 2
        self.snake_list_ = []
        self.snake_length_ = 1
        self.direction_ = pygame.KEYDOWN

    def draw_snake_body(self, dis):
        for x in self.snake_list_:
            pygame.draw.rect(
                dis, GREEN, [
                    x[0], x[1], self.snake_block_, self.snake_block_])

    def move_snake(self, x, y, direction):
        self.x_ += x
        self.y_ += y
        self.direction_ = direction

    def add_segment_to_snake(self, game):
        snake_head = [self.x_, self.y_]
        self.snake_list_.append(snake_head)

        if len(self.snake_list_) > self.snake_length_:
            del (self.snake_list_[0])

        for x in self.snake_list_[:-1]:
            if x == snake_head:
                game.set_game_close(True)

    def increment_snake_length(self):
        self.snake_length_ += 1


class Display:

    def __init__(self, width, height):
        self.width_ = width
        self.height_ = height
        self.dis_ = pygame.display.set_mode((width, height))
        self.font_ = pygame.font.SysFont(CALIBRI, FONT_SIZE)

    def show_message(self, msg, color):
        msg_tmp = self.font_.render(msg, True, color)
        self.dis_.blit(msg_tmp, [self.width_ / 8, self.height_ / 4])

    def show_score(self, score, high_score):
        msg_tmp = self.font_.render(SCORE + str(score), True, BLUE)
        msg_tmp2 = self.font_.render(HIGH_SCORE + str(high_score), True, BLUE)
        blit_list = [
            (msg_tmp, [
                10, 10]), (msg_tmp2, [
                    self.width_ - msg_tmp2.get_width() - 10, 10])]
        self.dis_.blits(blit_list)

    def check_if_snake_in_display(self, snake, game):
        if snake.x_ >= self.width_ or snake.x_ < 0 or snake.y_ >= self.height_ or snake.y_ < 0:
            game.set_game_close(True)


class Food:

    def __init__(self, display, snake_block):
        self.x_ = self.random_food_number(display.width_, snake_block)
        self.y_ = self.random_food_number(display.height_, snake_block)
        self.width_ = display.width_
        self.height_ = display.height_

    def random_food_number(self, dis_pos, snake_block):
        return round(random.randrange(snake_block * 2,
                                      dis_pos - (snake_block * 2)) / 10.0) * 10.0

    def draw_food(self, snake_block, dis):
        pygame.draw.rect(
            dis, RED, [
                self.x_, self.y_, snake_block, snake_block])

    def check_if_food_eaten(self, snake, game):
        if snake.x_ == self.x_ and snake.y_ == self.y_:
            self.x_ = self.random_food_number(self.width_, snake.snake_block_)
            self.y_ = self.random_food_number(self.height_, snake.snake_block_)
            snake.increment_snake_length()
            game.increment_high_score()
            game.increment_score()


class Game:

    def __init__(self):
        self.score_ = 0
        self.high_score_ = 0
        self.game_over_ = False
        self.game_close_ = False

    def set_game_over(self, param):
        self.game_over_ = param

    def set_game_close(self, param):
        self.game_close_ = param

    def increment_score(self):
        self.score_ += 10

    def increment_high_score(self):
        if self.score_ >= self.high_score_:
            self.high_score_ += 10

    def reset_score(self):
        self.score_ = 0
        self.set_game_over(False)
        self.set_game_close(False)

    def get_key_input(self, direction, x_change, y_change):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_game_over(True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != pygame.K_RIGHT:
                    x_change = -10
                    y_change = 0
                    direction = pygame.K_LEFT
                if event.key == pygame.K_RIGHT and direction != pygame.K_LEFT:
                    x_change = 10
                    y_change = 0
                    direction = pygame.K_RIGHT
                if event.key == pygame.K_UP and direction != pygame.K_DOWN:
                    x_change = 0
                    y_change = -10
                    direction = pygame.K_UP
                if event.key == pygame.K_DOWN and direction != pygame.K_UP:
                    x_change = 0
                    y_change = 10
                    direction = pygame.K_DOWN

        return x_change, y_change, direction


def game_loop(display, game):
    x_change = 0
    y_change = 0
    direction = pygame.KEYDOWN

    snake = Snake(display)
    food = Food(display, snake.snake_block_)
    clock = pygame.time.Clock()

    while not game.game_over_:

        while game.game_close_:
            display.dis_.fill(BLACK)
            display.show_message(GAME_LOST, RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.set_game_over(True)
                    game.set_game_close(False)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game.set_game_over(True)
                        game.set_game_close(False)
                    if event.key == pygame.K_p:
                        game.reset_score()
                        game_loop(display, game)  # new game

        x_change, y_change, direction = game.get_key_input(
            direction, x_change, y_change)
        display.check_if_snake_in_display(snake, game)

        snake.move_snake(x_change, y_change, direction)
        display.dis_.fill(GREY)

        food.draw_food(snake.snake_block_, display.dis_)
        snake.add_segment_to_snake(game)
        snake.draw_snake_body(display.dis_)

        display.show_score(game.score_, game.high_score_)
        pygame.display.update()

        food.check_if_food_eaten(snake, game)
        clock.tick(snake.snake_speed_)

    pygame.quit()
    quit()


def main():
    pygame.init()
    display = Display(WIDTH, HEIGHT)
    pygame.display.set_caption("Snake Game")
    game = Game()

    game_loop(display, game)


if __name__ == "__main__":
    main()
