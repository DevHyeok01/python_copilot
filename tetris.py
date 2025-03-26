import pygame
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 500, 600
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = HEIGHT // GRID_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# 테트로미노 모양
TETROMINOS = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

COLORS = [CYAN, YELLOW, MAGENTA, RED, BLUE, WHITE, WHITE]

# 배경음 로드 (주석 처리)
# pygame.mixer.music.load("tetris_theme.mp3")  # 실제 파일 경로로 교체
# pygame.mixer.music.set_volume(0.5)
# pygame.mixer.music.play(-1)

# 게임 상태
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
score = 0
font = pygame.font.SysFont(None, 36)

class Tetromino:
    def __init__(self):
        self.type = random.choice(list(TETROMINOS.keys()))
        self.shape = TETROMINOS[self.type]
        self.color = COLORS[list(TETROMINOS.keys()).index(self.type)]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

    def flip(self):  # 좌우 반전 기능
        self.shape = [row[::-1] for row in self.shape]

    def drop_to_bottom(self):
        while valid_move(self, dy=1):
            self.move(0, 1)

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                pygame.draw.rect(SCREEN, grid[y][x], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))
    pygame.draw.line(SCREEN, WHITE, (GRID_WIDTH * GRID_SIZE, 0), (GRID_WIDTH * GRID_SIZE, HEIGHT))

def draw_tetromino(tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(SCREEN, tetromino.color,
                                 ((tetromino.x + x) * GRID_SIZE, (tetromino.y + y) * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

def valid_move(tetromino, dx=0, dy=0):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = tetromino.x + x + dx
                new_y = tetromino.y + y + dy
                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or (new_y >= 0 and grid[new_y][new_x]):
                    return False
    return True

def merge_tetromino(tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[tetromino.y + y][tetromino.x + x] = tetromino.color

def clear_lines():
    global grid, score
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    cleared = GRID_HEIGHT - len(new_grid)
    if cleared > 0:
        score += cleared * 100
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(cleared)] + new_grid
    return cleared

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    SCREEN.blit(score_text, (GRID_WIDTH * GRID_SIZE + 20, 20))

def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(GRAY)
    SCREEN.blit(overlay, (0, 0))
    game_over_text = font.render("Game Over", True, WHITE)
    restart_text = font.render("Press S to Restart", True, WHITE)
    SCREEN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 20))
    SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

def draw_buttons(paused):
    start_text = font.render("Start (S)", True, WHITE if not paused else GRAY)
    pause_text = font.render("Pause (P)", True, WHITE if paused else GRAY)
    flip_text = font.render("Flip (R)", True, WHITE)
    SCREEN.blit(start_text, (GRID_WIDTH * GRID_SIZE + 20, 60))
    SCREEN.blit(pause_text, (GRID_WIDTH * GRID_SIZE + 20, 100))
    SCREEN.blit(flip_text, (GRID_WIDTH * GRID_SIZE + 20, 140))

# 게임 루프
clock = pygame.time.Clock()
tetromino = Tetromino()
fall_time = 0
fall_speed = 50
running = True
game_over = False
paused = True

while running:
    fall_time += 1 if not paused and not game_over else 0
    SCREEN.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and (game_over or paused):
                paused = False
                if game_over:
                    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
                    score = 0
                    tetromino = Tetromino()
                    game_over = False
                    # pygame.mixer.music.play(-1)  # 주석 처리
            if event.key == pygame.K_p and not game_over:
                paused = not paused
                # if paused:
                #     pygame.mixer.music.pause()
                # else:
                #     pygame.mixer.music.unpause()
            if not paused and not game_over:
                if event.key == pygame.K_LEFT and valid_move(tetromino, dx=-1):
                    tetromino.move(-1, 0)
                if event.key == pygame.K_RIGHT and valid_move(tetromino, dx=1):
                    tetromino.move(1, 0)
                if event.key == pygame.K_DOWN and valid_move(tetromino, dy=1):
                    tetromino.move(0, 1)
                if event.key == pygame.K_UP:
                    original_shape = tetromino.shape
                    tetromino.rotate()
                    if not valid_move(tetromino):
                        tetromino.shape = original_shape
                if event.key == pygame.K_SPACE:
                    tetromino.drop_to_bottom()
                    merge_tetromino(tetromino)
                    clear_lines()
                    tetromino = Tetromino()
                    if not valid_move(tetromino):
                        game_over = True
                    fall_time = 0
                if event.key == pygame.K_r:
                    original_shape = list(tetromino.shape)
                    tetromino.flip()
                    if not valid_move(tetromino):
                        tetromino.shape = original_shape

    if not paused and not game_over and fall_time >= fall_speed:
        if valid_move(tetromino, dy=1):
            tetromino.move(0, 1)
        else:
            merge_tetromino(tetromino)
            clear_lines()
            tetromino = Tetromino()
            if not valid_move(tetromino):
                game_over = True
        fall_time = 0

    draw_grid()
    if not game_over:
        draw_tetromino(tetromino)
    draw_score()
    draw_buttons(paused)
    if game_over:
        draw_game_over()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()