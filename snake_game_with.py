import pygame
import random
import math
import array

# Snake Game: Easy / Medium / Hard + дыбыс
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

WIDTH, HEIGHT = 800, 600
CELL = 20
TOP = 60
FPS = {"Easy": 8, "Medium": 13, "Hard": 19}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 26, bold=True)
small = pygame.font.SysFont("arial", 19)
big = pygame.font.SysFont("arial", 48, bold=True)

BG = (18, 24, 34)
GRID = (32, 42, 55)
GREEN = (70, 220, 120)
DARK_GREEN = (35, 155, 85)
RED = (255, 80, 90)
WHITE = (245, 247, 250)
YELLOW = (255, 210, 75)
BLUE = (90, 170, 255)


def make_sound(notes, duration=0.10, volume=0.35):
    """Дыбысты файлсыз, кодтың ішінде жасайды."""
    sample_rate = 22050
    buf = array.array("h")
    for freq in notes:
        count = int(sample_rate * duration)
        for i in range(count):
            t = i / sample_rate
            fade = min(1, i / max(1, int(sample_rate * 0.01)),
                       (count - i) / max(1, int(sample_rate * 0.02)))
            sample = int(32767 * volume * fade *
                         math.sin(2 * math.pi * freq * t))
            buf.append(sample)
    return pygame.mixer.Sound(buffer=buf.tobytes())


try:
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    eat_sound = make_sound([660, 880], 0.08, 0.30)
    over_sound = make_sound([440, 330, 220], 0.16, 0.32)
except (pygame.error, ValueError):
    eat_sound = None
    over_sound = None


def text(message, fnt, color, x, y, center=True):
    image = fnt.render(message, True, color)
    rect = image.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(image, rect)


def new_food(snake):
    free = [
        (x, y)
        for x in range(0, WIDTH, CELL)
        for y in range(TOP, HEIGHT, CELL)
        if (x, y) not in snake
    ]
    return random.choice(free) if free else None


def new_game(level):
    x = (WIDTH // 2 // CELL) * CELL
    y = ((TOP + (HEIGHT - TOP) // 2) // CELL) * CELL
    snake = [(x, y), (x - CELL, y), (x - 2 * CELL, y)]
    direction = (CELL, 0)
    return snake, direction, direction, new_food(snake), 0, level


def draw_board():
    screen.fill(BG)
    pygame.draw.rect(screen, (12, 17, 25), (0, 0, WIDTH, TOP))
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRID, (x, TOP), (x, HEIGHT))
    for y in range(TOP, HEIGHT, CELL):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y))


def draw_game(snake, food, score, level):
    draw_board()
    text("Level: " + level, small, BLUE, 16, 18, False)
    text("Score: " + str(score), small, WHITE, WIDTH - 130, 18, False)
    if food is not None:
        pygame.draw.circle(screen, RED,
                           (food[0] + CELL // 2, food[1] + CELL // 2), CELL // 2 - 2)
    for i, part in enumerate(snake):
        color = GREEN if i == 0 else DARK_GREEN
        pygame.draw.rect(screen, color,
                         (part[0] + 1, part[1] + 1, CELL - 2, CELL - 2),
                         border_radius=5)
    pygame.display.flip()


def menu():
    while True:
        screen.fill(BG)
        text("SNAKE GAME", big, GREEN, WIDTH // 2, 145)
        text("Choose difficulty", font, WHITE, WIDTH // 2, 220)
        text("1 - EASY", small, GREEN, WIDTH // 2, 285)
        text("2 - MEDIUM", small, YELLOW, WIDTH // 2, 325)
        text("3 - HARD", small, RED, WIDTH // 2, 365)
        text("Arrow keys or WASD to move", small, WHITE, WIDTH // 2, 435)
        text("Press 1, 2 or 3 to start", small, BLUE, WIDTH // 2, 475)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.unicode == "1":
                    return "Easy"
                if event.unicode == "2":
                    return "Medium"
                if event.unicode == "3":
                    return "Hard"
        clock.tick(30)


def game_over(score):
    if over_sound:
        over_sound.play()
    while True:
        draw_board()
        text("GAME OVER", big, RED, WIDTH // 2, 220)
        text("Final score: " + str(score), font, WHITE, WIDTH // 2, 285)
        text("R - Restart", small, YELLOW, WIDTH // 2, 340)
        text("M - Menu     ESC - Quit", small, WHITE, WIDTH // 2, 375)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_m:
                    return "menu"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit
        clock.tick(30)


def main():
    level = menu()
    while True:
        snake, direction, last_direction, food, score, level = new_game(level)
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w) and last_direction != (0, CELL):
                        direction = (0, -CELL)
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and last_direction != (0, -CELL):
                        direction = (0, CELL)
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and last_direction != (CELL, 0):
                        direction = (-CELL, 0)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and last_direction != (-CELL, 0):
                        direction = (CELL, 0)
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

            last_direction = direction
            head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            hit_wall = (head[0] < 0 or head[0] >= WIDTH or
                        head[1] < TOP or head[1] >= HEIGHT)
            eating = food is not None and head == food
            body = snake if eating else snake[:-1]
            if hit_wall or head in body:
                running = False
                continue

            snake.insert(0, head)
            if eating:
                score += 1
                if eat_sound:
                    eat_sound.play()
                food = new_food(snake)
                if food is None:
                    draw_game(snake, food, score, level)
                    text("YOU WIN!", big, YELLOW, WIDTH // 2, HEIGHT // 2)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    running = False
            else:
                snake.pop()

            draw_game(snake, food, score, level)
            clock.tick(FPS[level])

        result = game_over(score)
        if result == "restart":
            continue
        level = menu()


if __name__ == "__main__":
    main()

