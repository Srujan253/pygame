import pygame
import random

# constants for the windows width and height values
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

# the RGB values for the colors used in the game
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED   = (255, 0, 0)

# max score before declaring winner
WINNING_SCORE = 5

# ball speed control
BALL_SPEED = 0.25          # starting speed
SPEED_INCREMENT = 1.1      # 10% increase after paddle hit
MAX_SPEED = 2.0            # cap the speed multiplier

def reset_ball(ball_rect):
    """Reset the ball to the center with random direction and reset speed"""
    ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_speed_x = random.choice([-BALL_SPEED, BALL_SPEED])
    ball_speed_y = random.choice([-BALL_SPEED, BALL_SPEED])
    return ball_speed_x, ball_speed_y, 1.0  # reset speed multiplier

def main(): 
    # GAME SETUP
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Pong')
    clock = pygame.time.Clock()
    
    # paddles
    paddle_1_rect = pygame.Rect(30, SCREEN_HEIGHT//2 - 50, 7, 100)
    paddle_2_rect = pygame.Rect(SCREEN_WIDTH - 50, SCREEN_HEIGHT//2 - 50, 7, 100)
    paddle_1_move = 0
    paddle_2_move = 0

    # ball
    ball_rect = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 25, 25)
    ball_accel_x, ball_accel_y, speed_multiplier = reset_ball(ball_rect)

    # scores
    player1_score = 0
    player2_score = 0
    font = pygame.font.SysFont('Consolas', 40)
    winner_font = pygame.font.SysFont('Consolas', 60)

    started = False
    game_over = False
    winner = ""

    # GAME LOOP
    while True:
        screen.fill(COLOR_BLACK)

        # before starting
        if not started:
            text = font.render('Press SPACE to Start', True, COLOR_WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    started = True
            continue  # skip the rest until started

        # after winner
        if game_over:
            winner_text = winner_font.render(f"{winner} Wins!", True, COLOR_WHITE)
            text_rect = winner_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(winner_text, text_rect)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            continue  # freeze game after winner

        delta_time = clock.tick(60)

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    paddle_1_move = -0.5
                if event.key == pygame.K_s:
                    paddle_1_move = 0.5
                if event.key == pygame.K_UP:
                    paddle_2_move = -0.5
                if event.key == pygame.K_DOWN:
                    paddle_2_move = 0.5
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_s):
                    paddle_1_move = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    paddle_2_move = 0

        # move paddles
        paddle_1_rect.top += paddle_1_move * delta_time
        paddle_2_rect.top += paddle_2_move * delta_time
        paddle_1_rect.clamp_ip(screen.get_rect())
        paddle_2_rect.clamp_ip(screen.get_rect())

        # move ball with speed multiplier
        ball_rect.left += ball_accel_x * delta_time * speed_multiplier
        ball_rect.top += ball_accel_y * delta_time * speed_multiplier

        # bounce top & bottom
        if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
            ball_accel_y *= -1

        # paddle collisions (increase speed slightly each hit)
        if paddle_1_rect.colliderect(ball_rect) and ball_accel_x < 0:
            ball_accel_x *= -1
            speed_multiplier = min(speed_multiplier * SPEED_INCREMENT, MAX_SPEED)

        if paddle_2_rect.colliderect(ball_rect) and ball_accel_x > 0:
            ball_accel_x *= -1
            speed_multiplier = min(speed_multiplier * SPEED_INCREMENT, MAX_SPEED)

        # scoring
        if ball_rect.left <= 0:  # Player 2 scores
            player2_score += 1
            ball_accel_x, ball_accel_y, speed_multiplier = reset_ball(ball_rect)
        if ball_rect.right >= SCREEN_WIDTH:  # Player 1 scores
            player1_score += 1
            ball_accel_x, ball_accel_y, speed_multiplier = reset_ball(ball_rect)

        # check winner
        if player1_score >= WINNING_SCORE:
            winner = "Player 1"
            game_over = True
        elif player2_score >= WINNING_SCORE:
            winner = "Player 2"
            game_over = True

        # draw paddles
        pygame.draw.rect(screen, COLOR_WHITE, paddle_1_rect)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_2_rect)

        # draw ball as red circle
        pygame.draw.circle(screen, COLOR_RED, ball_rect.center, ball_rect.width//2)

        # draw score
        score_text = font.render(f"{player1_score}   {player2_score}", True, COLOR_WHITE)
        text_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 40))
        screen.blit(score_text, text_rect)

        pygame.display.update()

# run the game
if __name__ == '__main__':
    main()
