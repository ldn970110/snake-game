import pygame
import random
from collections import deque # 導入 deque

# --- 1. Initialize Pygame ---
pygame.init()

# --- 2. Define Colors and Game Parameters ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)

GRID_SIZE = 20
GRID_WIDTH = 25
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_WIDTH * GRID_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * GRID_SIZE

# Game Direction Constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game Clock and FPS
clock = pygame.time.Clock()
FPS = 10 # Control snake speed

# --- 3. Create Game Window ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game - Pygame")

# --- 4. Snake Class ---
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2),
                     (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
                     (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0
        self.color = DARK_GREEN
        self.direction_queue = deque() # Initialize the direction queue

    def move(self):
        # Try to get the next direction from the queue
        if self.direction_queue:
            next_dir = self.direction_queue.popleft()
            self.direction = next_dir # Update actual snake direction

        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()

    def change_direction(self, new_dir):
        # Add new direction to the queue
        # Optional: Limit queue size to prevent too many buffered commands
        if len(self.direction_queue) >= 2: # Only buffer up to 2 commands
            return

        # Determine the effective current direction to check for 180-degree turn
        # If queue is not empty, use the last buffered direction for this check
        # Otherwise, use the snake's current actual direction
        effective_current_dir = self.direction
        if self.direction_queue:
            effective_current_dir = self.direction_queue[-1]

        # Prevent 180-degree turns
        if (new_dir[0] * -1, new_dir[1] * -1) != effective_current_dir:
            self.direction_queue.append(new_dir)

    def grow(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)

    def draw(self, surface):
        for segment in self.body:
            x, y = segment
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

    def get_head_pos(self):
        return self.body[0]

    def check_collision(self):
        head = self.get_head_pos()
        if not (0 <= head[0] < GRID_WIDTH and 0 <= head[1] < GRID_HEIGHT):
            return True
        if head in self.body[1:]:
            return True
        return False

# --- 5. Food Class ---
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self, snake_body=[]):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            new_pos = (x, y)
            if new_pos not in snake_body:
                self.position = new_pos
                break

    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.color, rect)

# --- 6. Game Main Loop ---
def main():
    snake = Snake()
    food = Food()
    food.randomize_position(snake.body)

    running = True
    game_over = False

    score_font = pygame.font.Font(None, 36)
    game_over_font = pygame.font.Font(None, 48)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(RIGHT)
                elif game_over:
                    if event.key == pygame.K_r:
                        snake = Snake()
                        food.randomize_position(snake.body)
                        game_over = False

        if not game_over:
            snake.move()

            if snake.get_head_pos() == food.position:
                snake.grow()
                snake.score += 1
                food.randomize_position(snake.body)

            if snake.check_collision():
                game_over = True
                print("Game Over! Score:", snake.score)

        screen.fill(BLACK)

        snake.draw(screen)
        food.draw(screen)

        score_text = score_font.render(f"Score: {snake.score}", True, WHITE)
        screen.blit(score_text, (5, 5))

        if game_over:
            game_over_message = game_over_font.render("GAME OVER!", True, RED)
            game_over_score = game_over_font.render(f"Final Score: {snake.score}", True, RED)
            restart_message = game_over_font.render("Press 'R' to Restart", True, RED)

            message_rect = game_over_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            score_rect = game_over_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            restart_rect = restart_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

            screen.blit(game_over_message, message_rect)
            screen.blit(game_over_score, score_rect)
            screen.blit(restart_message, restart_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()