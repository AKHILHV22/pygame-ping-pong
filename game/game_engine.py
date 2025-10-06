import pygame
import time
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        pygame.mixer.init()  # ✅ Initialize sound mixer

        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.winning_score = 5  # Default target

        # ✅ Load sounds
        try:
            self.sound_paddle = pygame.mixer.Sound("assets/sounds/paddle_hit.wav")
            self.sound_wall = pygame.mixer.Sound("assets/sounds/wall_bounce.wav")
            self.sound_score = pygame.mixer.Sound("assets/sounds/score.wav")
        except:
            print("⚠️ Sound files missing! Place them inside assets/sounds/.")
            self.sound_paddle = self.sound_wall = self.sound_score = None

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Move the ball
        prev_velocity_y = self.ball.velocity_y
        prev_velocity_x = self.ball.velocity_x
        self.ball.move()

        # Wall bounce sound
        if self.ball.velocity_y != prev_velocity_y and self.sound_wall:
            self.sound_wall.play()

        # Paddle collisions
        if self.ball.rect().colliderect(self.player.rect()):
            self.ball.x = self.player.x + self.player.width
            self.ball.velocity_x *= -1
            if self.sound_paddle:
                self.sound_paddle.play()

        elif self.ball.rect().colliderect(self.ai.rect()):
            self.ball.x = self.ai.x - self.ball.width
            self.ball.velocity_x *= -1
            if self.sound_paddle:
                self.sound_paddle.play()

        # Scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
            if self.sound_score:
                self.sound_score.play()

        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            self.ball.reset()
            if self.sound_score:
                self.sound_score.play()

        # Move AI
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    # 🧠 Game Over + Replay Menu
    def check_game_over(self, screen):
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            winner_text = "Player Wins!" if self.player_score >= self.winning_score else "AI Wins!"
            big_font = pygame.font.SysFont("Arial", 50)
            small_font = pygame.font.SysFont("Arial", 25)

            screen.fill(BLACK)
            winner_surface = big_font.render(winner_text, True, WHITE)
            screen.blit(winner_surface, winner_surface.get_rect(center=(self.width // 2, self.height // 2 - 80)))

            options = [
                "Select Mode:",
                "[3] Best of 3",
                "[5] Best of 5",
                "[7] Best of 7",
                "[ESC] Exit"
            ]
            for i, text in enumerate(options):
                opt_surface = small_font.render(text, True, WHITE)
                screen.blit(opt_surface, opt_surface.get_rect(center=(self.width // 2, self.height // 2 + i * 35 - 10)))

            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_3:
                            self.reset_game(3)
                            waiting = False
                            return False
                        elif event.key == pygame.K_5:
                            self.reset_game(5)
                            waiting = False
                            return False
                        elif event.key == pygame.K_7:
                            self.reset_game(7)
                            waiting = False
                            return False
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            quit()
            return True
        return False

    def reset_game(self, winning_score=None):
        if winning_score:
            self.winning_score = winning_score
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - self.player.height // 2
        self.ai.y = self.height // 2 - self.ai.height // 2
