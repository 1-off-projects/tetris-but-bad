import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

# Colors for shapes
SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.current_shape = self.get_new_shape()
        self.next_shape = self.get_new_shape()
        self.score = 0
        self.game_over = False

    def get_new_shape(self):
        shape = random.choice(SHAPES)
        color = random.choice(SHAPE_COLORS)
        return {"shape": shape, "color": color, "x": SCREEN_WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2, "y": 0}

    def draw_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                pygame.draw.rect(self.screen, self.grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(self.screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_shape(self, shape, offset_x, offset_y):
        for y, row in enumerate(shape["shape"]):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, shape["color"], ((shape["x"] + x + offset_x) * BLOCK_SIZE, (shape["y"] + y + offset_y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    def check_collision(self, shape, offset_x, offset_y):
        for y, row in enumerate(shape["shape"]):
            for x, cell in enumerate(row):
                if cell:
                    new_x = shape["x"] + x + offset_x
                    new_y = shape["y"] + y + offset_y
                    if new_x < 0 or new_x >= SCREEN_WIDTH // BLOCK_SIZE or new_y < 0 or new_y >= SCREEN_HEIGHT // BLOCK_SIZE or self.grid[new_y][new_x] != BLACK:
                        return True
        return False

    def lock_shape(self, shape):
        for y, row in enumerate(shape["shape"]):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[shape["y"] + y][shape["x"] + x] = shape["color"]
        self.clear_lines()

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == BLACK for cell in row)]
        lines_cleared = len(self.grid) - len(new_grid)
        self.score += lines_cleared * 100
        self.grid = [[BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(lines_cleared)] + new_grid

    def rotate_shape(self, shape):
        return {"shape": [list(row) for row in zip(*shape["shape"][::-1])], "color": shape["color"], "x": shape["x"], "y": shape["y"]}

    def run(self):
        while not self.game_over:
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_shape(self.current_shape, 0, 0)
            self.draw_shape(self.next_shape, SCREEN_WIDTH // BLOCK_SIZE - len(self.next_shape["shape"][0]), 0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and not self.check_collision(self.current_shape, -1, 0):
                        self.current_shape["x"] -= 1
                    elif event.key == pygame.K_RIGHT and not self.check_collision(self.current_shape, 1, 0):
                        self.current_shape["x"] += 1
                    elif event.key == pygame.K_DOWN and not self.check_collision(self.current_shape, 0, 1):
                        self.current_shape["y"] += 1
                    elif event.key == pygame.K_UP:
                        rotated_shape = self.rotate_shape(self.current_shape)
                        if not self.check_collision(rotated_shape, 0, 0):
                            self.current_shape = rotated_shape

            if not self.check_collision(self.current_shape, 0, 1):
                self.current_shape["y"] += 1
            else:
                self.lock_shape(self.current_shape)
                self.current_shape = self.next_shape
                self.next_shape = self.get_new_shape()
                if self.check_collision(self.current_shape, 0, 0):
                    self.game_over = True

            pygame.display.flip()
            self.clock.tick(10)

        print(f"Game Over! Your score: {self.score}")
        pygame.quit()

if __name__ == "__main__":
    Tetris().run()