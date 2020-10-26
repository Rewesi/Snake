"""
Snake game, created at python workshop for high-school students
Done by Lukas Brazdil
"""

import pygame, sys, time
from random import randint

# --- Defining constants ---

FPS = 10
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

if WINDOW_WIDTH < 640:
    WINDOW_WIDTH = 640

if WINDOW_HEIGHT < 480:
    WINDOW_HEIGHT = 480

CELL_SIZE = 20
assert WINDOW_WIDTH % CELL_SIZE == 0, """Window width must be a multiple of cell size."""
assert WINDOW_HEIGHT % CELL_SIZE == 0, """Window height must be a multiple of cell size."""
NUM_CELLS_X = WINDOW_WIDTH // CELL_SIZE
NUM_CELLS_Y = (WINDOW_HEIGHT - 2*CELL_SIZE) // CELL_SIZE

BG_COLOR = (0, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (80, 80, 80)
LIGHT_GRAY = (127, 127, 127)
RED = (255, 0, 0)
LIGHT_RED = (255, 99, 71)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
LIME_GREEN = (50, 205, 50)
BROWN = (139, 69, 19)

SNAKE_COLOR_INSIDE = GREEN
SNAKE_COLOR_OUTSIDE = LIME_GREEN
APPLE_COLOR_INSIDE = LIGHT_RED
APPLE_COLOR_OUTSIDE = RED

BASIC_FONT_SIZE = WINDOW_WIDTH // 30

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


# --- Functions ---

def main():
    global FPS_CLOCK, DISPLAY_SURFACE, BASIC_FONT, HEADLINE_FONT, SMALL_FONT

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Snake')
    # pygame.display.set_icon(pygame.image.load('images/snake.png'))
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)
    HEADLINE_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE * 2)
    SMALL_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE - (WINDOW_WIDTH // 100))

    wait_for_key_pressed()

    while True:
        if was_key_pressed():
            show_start_screen()
            break
        FPS_CLOCK.tick(FPS)

    while True:
        score = run_game()
        game_over_screen(score)
        while True:
            if was_key_pressed():
                show_start_screen()
                break

        was_key_pressed()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def wait_for_key_pressed():
    DISPLAY_SURFACE.fill(BG_COLOR)

    msg_surface = HEADLINE_FONT.render('Snake', True, WHITE)
    msg_rect = msg_surface.get_rect()
    msg_rect.center = ((WINDOW_WIDTH // 2), (WINDOW_HEIGHT // 2) - (WINDOW_WIDTH // 8))
    DISPLAY_SURFACE.blit(msg_surface, msg_rect)

    msg_surface = BASIC_FONT.render("Use arrow keys or 'wsad' keys", True, LIGHT_GRAY)
    msg_rect = msg_surface.get_rect()
    msg_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    DISPLAY_SURFACE.blit(msg_surface, msg_rect)

    msg_surface = BASIC_FONT.render("to control snake direction", True, LIGHT_GRAY)
    msg_rect = msg_surface.get_rect()
    msg_rect.center = (WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) + BASIC_FONT_SIZE + (BASIC_FONT_SIZE // 2))
    DISPLAY_SURFACE.blit(msg_surface, msg_rect)

    msg_surface = SMALL_FONT.render('Press any key to play, Esc to exit', True, LIGHT_GRAY)
    msg_rect = msg_surface.get_rect()
    msg_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)
    DISPLAY_SURFACE.blit(msg_surface, msg_rect)

    pygame.display.update()


def was_key_pressed():
    """Check whether key was pressed and if exit key was triggered"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            terminate()
        elif event.type == pygame.KEYUP:
            return True
        else:
            return False


def show_start_screen():
    """Show countdown screen before snake game starts"""
    option = [3, 2, 1]
    for i in option:
        msg_surface = BASIC_FONT.render("Snake in " + str(i), True, WHITE)
        msg_rect = msg_surface.get_rect()
        msg_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        DISPLAY_SURFACE.fill(BG_COLOR)
        DISPLAY_SURFACE.blit(msg_surface, msg_rect)

        pygame.display.update()
        time.sleep(1)

    DISPLAY_SURFACE.fill(BG_COLOR)


def get_new_snake():
    """Set a random start point for a new snake and return its coordinates"""
    x = 4
    random_y = randint(5, NUM_CELLS_Y - 2)
    position = [[x, random_y], [x - 1, random_y], [x - 2, random_y]]
    return position, "right"


def get_random_apple_location(snake):
    """Return random location for apple"""
    while True:
        random_x = randint(1, NUM_CELLS_X - 2)
        random_y = randint(3, NUM_CELLS_Y)
        position = [random_x, random_y]
        if position in snake:
            continue
        break
    return position


def run_game():
    """Main game function, where game logic happens"""
    DISPLAY_SURFACE.fill(BG_COLOR)
    snake, direction = get_new_snake()
    apple = get_random_apple_location(snake)
    score = 0
    initial_time = time.time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                terminate()
            elif event.type == pygame.KEYUP and (event.key == pygame.K_RIGHT or event.key == ord("d")):
                if direction != "left":
                    direction = "right"
            elif event.type == pygame.KEYUP and (event.key == pygame.K_UP or event.key == ord("w")):
                if direction != "down":
                    direction = "up"
            elif event.type == pygame.KEYUP and (event.key == pygame.K_LEFT or event.key == ord("a")):
                if direction != "right":
                    direction = "left"
            elif event.type == pygame.KEYUP and (event.key == pygame.K_DOWN or event.key == ord("s")):
                if direction != "up":
                    direction = "down"

        if direction == "left":
            new_head = [(snake[0][0] - 1), (snake[0][1])]
        elif direction == "right":
            new_head = [(snake[0][0] + 1), (snake[0][1])]
        elif direction == "up":
            new_head = [(snake[0][0]), (snake[0][1] - 1)]
        elif direction == "down":
            new_head = [(snake[0][0]), (snake[0][1] + 1)]

        snake.reverse()
        snake.append(new_head)
        snake.reverse()

        apple, apple_eaten, score = apple_eaten_by_snake(snake, apple, score)

        if apple_eaten == False:
            snake.pop(len(snake) - 1)

        DISPLAY_SURFACE.fill(BG_COLOR)
        draw_surface()
        draw_snake(snake, direction)
        draw_apple(apple)
        draw_info_panel(score, initial_time)

        if snake[0] in snake[1:] or (snake[0][0] < 0 or snake[0][0] >= NUM_CELLS_X) or (
                snake[0][1] < 2 or snake[0][1] >= NUM_CELLS_Y + 2):
            return score

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def draw_snake(snake, direction):
    """Draw snake body at coordinates in snake variable"""
    head = True
    for i in snake:
        left = i[0] * CELL_SIZE
        top = i[1] * CELL_SIZE
        pygame.draw.rect(DISPLAY_SURFACE, SNAKE_COLOR_OUTSIDE, (left, top, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(DISPLAY_SURFACE, SNAKE_COLOR_INSIDE, (left + 2, top + 2, CELL_SIZE - 4, CELL_SIZE - 4))
        if head:
            head = False
            if direction == 'right':
                pygame.draw.rect(DISPLAY_SURFACE, APPLE_COLOR_INSIDE, (left + 16, top + 9, 4, 2))

                pygame.draw.rect(DISPLAY_SURFACE, WHITE, (left + 4, top + 3, 5, 6))
                pygame.draw.rect(DISPLAY_SURFACE, BLACK, (left + 6, top + 5, 3, 3))

                pygame.draw.rect(DISPLAY_SURFACE, WHITE, (left + 4, top + 11, 5, 6))
                pygame.draw.rect(DISPLAY_SURFACE, BLACK, (left + 6, top + 12, 3, 3))
            elif direction == 'up':
                pygame.draw.rect(DISPLAY_SURFACE, APPLE_COLOR_INSIDE, (left + 9, top, 2, 4))

                pygame.draw.rect(DISPLAY_SURFACE, WHITE, (left + 3, top + 11, 6, 5))
                pygame.draw.rect(DISPLAY_SURFACE, BLACK, (left + 5, top + 11, 3, 3))

                pygame.draw.rect(DISPLAY_SURFACE, WHITE, (left + 11, top + 11, 6, 5))
                pygame.draw.rect(DISPLAY_SURFACE, BLACK, (left + 12, top + 11, 3, 3))
            elif direction == 'left':
                pygame.draw.rect(DISPLAY_SURFACE, APPLE_COLOR_INSIDE, (left, top + 9, 4, 2))

                pygame.draw.rect(DISPLAY_SURFACE, WHITE, (left + 11, top + 3, 5, 6))
                pygame.draw.rect(DISPLAY_SURFACE, BLACK, (left + 11, top + 5, 3, 3))

                pygame.draw.rect(DISPLAY_SURFACE, WHITE, (left + 11, top + 11, 5, 6))
                pygame.draw.rect(DISPLAY_SURFACE, BLACK, (left + 11, top + 12, 3, 3))
            elif direction == 'down':
                pygame.draw.rect(DISPLAY_SURFACE, APPLE_COLOR_INSIDE, (left + 9, top + 16, 2, 4))

                pygame.draw.rect(DISPLAY_SURFACE, WHITE, (left + 3, top + 4, 6, 5))
                pygame.draw.rect(DISPLAY_SURFACE, BLACK, (left + 5, top + 6, 3, 3))

                pygame.draw.rect(DISPLAY_SURFACE, WHITE, (left + 11, top + 4, 6, 5))
                pygame.draw.rect(DISPLAY_SURFACE, BLACK, (left + 12, top + 6, 3, 3))


def draw_info_panel(score, initial_time):
    """Draw top info panel with time and score information"""
    time_passed = ((time.time() - initial_time) // 1)
    seconds = int(time_passed % 60)
    minutes = int((time_passed // 60) % 60)
    hours = int((time_passed // 60) // 60)

    info_panel_font = pygame.font.Font('freesansbold.ttf', (CELL_SIZE + CELL_SIZE // 3))

    if hours < 1:
        msg_surface = info_panel_font.render('Time: ' + number_complete(minutes) + ':' + number_complete(seconds),
                                             True, WHITE)
    else:
        msg_surface = info_panel_font.render('Time: ' + number_complete(hours) + ':' + number_complete(minutes) +
                                             ':' + number_complete(seconds), True, LIGHT_GRAY)
    msg_rect = msg_surface.get_rect()
    msg_rect.topleft = (CELL_SIZE // 2, (CELL_SIZE // 2) - (CELL_SIZE // 11))
    DISPLAY_SURFACE.blit(msg_surface, msg_rect)

    msg_surface = info_panel_font.render('Score: ' + str(score), True, WHITE)
    msg_rect = msg_surface.get_rect()
    msg_rect.topleft = (WINDOW_WIDTH - (CELL_SIZE * 9), (CELL_SIZE // 2) - (CELL_SIZE // 11))
    DISPLAY_SURFACE.blit(msg_surface, msg_rect)


def number_complete(number):
    """Return number as a two character string"""
    if number < 10:
        number = '0' + str(number)
    else:
        number = str(number)
    return number


def apple_eaten_by_snake(snake, apple, score):
    """Check whether apple was eaten by snake's head"""
    eaten = False
    if apple == snake[0]:
        apple = get_random_apple_location(snake)
        eaten = True
        score = score + 1
    return apple, eaten, score


def draw_apple(apple):
    """Draw apple at coordinates in apple variable"""
    left = apple[0] * CELL_SIZE
    top = apple[1] * CELL_SIZE
    pygame.draw.rect(DISPLAY_SURFACE, APPLE_COLOR_OUTSIDE, (left, top, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(DISPLAY_SURFACE, APPLE_COLOR_INSIDE, (left + 2, top + 2, CELL_SIZE - 4, CELL_SIZE - 4))
    return


def draw_surface():
    """Draw grid of rectangles, where snake can move"""
    if NUM_CELLS_X > NUM_CELLS_Y:
        num_x = NUM_CELLS_X
        num_y = NUM_CELLS_Y
    else:
        num_x = NUM_CELLS_Y
        num_y = NUM_CELLS_X

    pygame.draw.rect(DISPLAY_SURFACE, DARK_GRAY, (0, 0, WINDOW_WIDTH, 2 * CELL_SIZE))

    for x in range(num_y):
        for y in range(num_x):
            pygame.draw.rect(DISPLAY_SURFACE, DARK_GRAY,
                             (y * CELL_SIZE, (2*CELL_SIZE) + (x * CELL_SIZE), CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(DISPLAY_SURFACE, BG_COLOR,
                             (y * CELL_SIZE + 1, (2*CELL_SIZE) + (x * CELL_SIZE) + 1, CELL_SIZE - 2, CELL_SIZE - 2))


def game_over_screen(score):
    """Show game over screen with score information"""
    DISPLAY_SURFACE.fill(BG_COLOR)

    msg_surface = HEADLINE_FONT.render("Game Over!", True, WHITE)
    msg_rect = msg_surface.get_rect()
    msg_rect.center = (WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) - (BASIC_FONT_SIZE * 3))
    DISPLAY_SURFACE.blit(msg_surface, msg_rect)

    msg_surface = BASIC_FONT.render("You're score is " + str(score), True, WHITE)
    msg_rect = msg_surface.get_rect()
    msg_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + BASIC_FONT_SIZE // 2)
    DISPLAY_SURFACE.blit(msg_surface, msg_rect)

    msg_surface = SMALL_FONT.render('Press any key to play again, Esc to exit', True, LIGHT_GRAY)
    msg_rect = msg_surface.get_rect()
    msg_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)
    DISPLAY_SURFACE.blit(msg_surface, msg_rect)

    pygame.display.update()


if __name__ == '__main__':
    main()
