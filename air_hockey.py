import pygame, sys, random

# CONSTANTS
WIDTH, HEIGHT = 500, 900
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FPS = 40
TABLE_COLOR = (200, 200, 210)
BLUE = (0, 0, 255)
PUCK_COLOR = (50, 50, 50)

GOAL_WIDTH = 200
WALL_THICKNESS = 10

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Air Hockey')
clock = pygame.time.Clock()

class Paddle:
    """ Represents the paddle object in the Air Hockey game. """
    
    def __init__(self, x, y):
        """ Initialize the paddle with a specific position. """
        self.rect = pygame.Rect(x, y, 80, 15)

    def move(self, speed, direction):
        """ Move the paddle left or right by a given speed. """
        if direction == 'left':
            self.rect.x = max(WALL_THICKNESS, self.rect.x - speed)
        elif direction == 'right':
            self.rect.x = min(WIDTH - WALL_THICKNESS - self.rect.width, self.rect.x + speed)

    def draw(self):
        """ Draw the paddle on the screen. """
        pygame.draw.circle(screen, RED if self.rect.y < HEIGHT // 2 else BLUE, self.rect.center, self.rect.width // 2)

    def restart(self):
        """ Reset the paddle to its default horizontal position. """
        self.rect.centerx = WIDTH // 2

class Ball:
    """ Represents the ball object in the Air Hockey game. """
    
    def __init__(self):
        """ Initialize the ball at the center of the screen with a random direction. """
        self.rect = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
        self.dx = random.choice([-7, 7])
        self.dy = 20 if random.randint(0, 1) == 0 else -20
    
    def move(self):
        """ Move the ball by its speed in the x and y direction. """
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.left <= WALL_THICKNESS or self.rect.right >= WIDTH - WALL_THICKNESS:
            self.dx = -self.dx
        if self.rect.top <= WALL_THICKNESS:
            if not (WIDTH // 2 - GOAL_WIDTH // 2 < self.rect.centerx < WIDTH // 2 + GOAL_WIDTH // 2):
                self.dy = -self.dy
        if self.rect.bottom >= HEIGHT - WALL_THICKNESS:
            if not (WIDTH // 2 - GOAL_WIDTH // 2 < self.rect.centerx < WIDTH // 2 + GOAL_WIDTH // 2):
                self.dy = -self.dy

    def paddle_collision(self):
        """ Reverse y direction if the ball hits a paddle. """
        self.dy = -self.dy

    def draw(self):
        """ Draw the ball on the screen. """
        pygame.draw.ellipse(screen, PUCK_COLOR, self.rect)

    def restart(self):
        """ Reset the ball to the center of the screen with a random x direction and reversed y direction. """
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.dx = random.choice([-5, 5])
        self.dy *= -1

class Score:
    """ Represents the score for a player. """
    
    def __init__(self, x, y):
        """ Initialize score at a given position on the screen. """
        self.score = 0
        self.font = pygame.font.SysFont("monospace", 80, bold=True)
        self.x = x
        self.y = y

    def display(self):
        """ Display the current score on the screen. """
        score_display = self.font.render(str(self.score), 0, WHITE)
        screen.blit(score_display, (self.x - score_display.get_width() // 2, self.y))

    def increase(self):
        """ Increase the score by one point. """
        self.score += 1

    def reset(self):
        """ Reset the score to zero. """
        self.score = 0

def main():
    paddle_speed = 10
    paddle1 = Paddle(WIDTH // 2 - 60, 15)
    paddle2 = Paddle(WIDTH // 2 - 60, HEIGHT - 35)
    ball = Ball()
    score1 = Score(WIDTH // 4, 15)
    score2 = Score(3 * WIDTH // 4, 15)

    playing = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and not playing:
            playing = True
        if keys[pygame.K_r]:
            playing = False
            score1.reset()
            score2.reset()
            ball.restart()
            paddle1.restart()
            paddle2.restart()

        if keys[pygame.K_a]:
            paddle1.move(paddle_speed, 'left')
        if keys[pygame.K_d]:
            paddle1.move(paddle_speed, 'right')
        if keys[pygame.K_LEFT]:
            paddle2.move(paddle_speed, 'left')
        if keys[pygame.K_RIGHT]:
            paddle2.move(paddle_speed, 'right')

        screen.fill(TABLE_COLOR)
        
        # Drawing the walls
        pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, WALL_THICKNESS))
        pygame.draw.rect(screen, WHITE, (0, HEIGHT - WALL_THICKNESS, WIDTH, WALL_THICKNESS))
        pygame.draw.rect(screen, WHITE, (0, 0, WALL_THICKNESS, HEIGHT))
        pygame.draw.rect(screen, WHITE, (WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, HEIGHT))
        
        # Drawing the goals
        pygame.draw.rect(screen, TABLE_COLOR, (WIDTH // 2 - GOAL_WIDTH // 2, 0, GOAL_WIDTH, WALL_THICKNESS))
        pygame.draw.rect(screen, TABLE_COLOR, (WIDTH // 2 - GOAL_WIDTH // 2, HEIGHT - WALL_THICKNESS, GOAL_WIDTH, WALL_THICKNESS))

        pygame.draw.line(screen, WHITE, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 5)
        pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), 50, 5)  # Center circle

        if playing:
            ball.move()
            ball.draw()

            if ball.rect.colliderect(paddle1.rect) or ball.rect.colliderect(paddle2.rect):
                ball.paddle_collision()

            if ball.rect.top <= WALL_THICKNESS:
                if (WIDTH // 2 - GOAL_WIDTH // 2 < ball.rect.centerx < WIDTH // 2 + GOAL_WIDTH // 2):
                    score2.increase()
                    ball.restart()

            if ball.rect.bottom >= HEIGHT - WALL_THICKNESS:
                if (WIDTH // 2 - GOAL_WIDTH // 2 < ball.rect.centerx < WIDTH // 2 + GOAL_WIDTH // 2):
                    score1.increase()
                    ball.restart()

            paddle1.draw()
            paddle2.draw()
            score1.display()
            score2.display()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
