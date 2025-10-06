import pygame
import time
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
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

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    
    # Task 1: Refine Ball Collision
    def update(self):
        # Move the ball first
        self.ball.move()

        # Check collision immediately after moving
        if self.ball.rect().colliderect(self.player.rect()):
            self.ball.x = self.player.x + self.player.width  # prevent overlap
            self.ball.velocity_x *= -1

        elif self.ball.rect().colliderect(self.ai.rect()):
            self.ball.x = self.ai.x - self.ball.width  # prevent overlap
            self.ball.velocity_x *= -1

        # Check if ball goes out of bounds (scoring)
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            self.ball.reset()

        # Wall collisions (top/bottom handled in Ball.move())
        # Update AI paddle movement
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))


    # Task 2: Implement Game Over Condition

    def check_game_over(self, screen):
        # If either player reaches 5 points
        if self.player_score >= 5 or self.ai_score >= 5:
            winner_text = "Player Wins!" if self.player_score >= 5 else "AI Wins!"

            # Render the message
            text_surface = self.font.render(winner_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()

            # Pause for a few seconds to display the result
            time.sleep(3)
            pygame.quit()
            quit()  # Exit program

            return True
        return False
