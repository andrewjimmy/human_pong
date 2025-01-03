import pygame
import random
import sys
from PosDetector import PosDetector

pygame.init()
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Tennees")
clock = pygame.time.Clock()
CLOCK_TICK = 30

#Setup Components
screen_color = 'black' #Define the screen color (which happens toward the bottom)

min_color = 1
ball_color = pygame.Color(random.randint(min_color, 255), random.randint(min_color, 255), random.randint(min_color, 255)) #make not black
paddle_color = color = pygame.Color(random.randint(min_color, 255), random.randint(min_color, 255), random.randint(min_color, 255)) #Not black
x_pos = SCREEN_WIDTH // 2
y_pos = SCREEN_HEIGHT // 2

x_mov = random.randint(5,10)
y_mov = random.randint(5,10)

left_paddle_pos = SCREEN_HEIGHT // 2
right_paddle_pos = SCREEN_HEIGHT // 2

player1_score = 0
player2_score = 0

posDetector = PosDetector()

paddle_pos = [0, 0]
paddle_order = [0, 0]

#Begin Game!
running = True
end_running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #pygame.display.quit()
            #pygame.quit()
            running = False
            # Have to turn off end running when clicking close or it will require the user
            # to click close twice. There is probably a better fix for this, but needs
            # a rewrite of part of the game engine.
            end_running = False
            break

    results = posDetector.capture_faces()
    
    if results.detections:
            #print(results.detections)
            for i, detection in enumerate(results.detections):
                if(i < 2):
                    bboxC = detection.location_data.relative_bounding_box
                    x, y = int(SCREEN_WIDTH - (2*bboxC.xmin + bboxC.width)*SCREEN_WIDTH/2), int((2*bboxC.ymin + bboxC.height)*SCREEN_HEIGHT/2)
                    print(x, y)
                    paddle_pos[i] = y
                    paddle_order[i] = x
                    pygame.draw.circle(screen, pygame.Color(255, 0, 0), [x, y], 3)

    #Create Ball
    pygame.draw.circle(screen, ball_color, [x_pos, y_pos], 10)
    x_pos += x_mov
    y_pos += y_mov

    #Ball should bounce
    if y_pos >= SCREEN_HEIGHT or y_pos <= 0:
        y_mov *= -1
        ball_color = pygame.Color(random.randint(min_color, 255), random.randint(min_color, 255), random.randint(min_color, 255)) #not black

    if x_pos <= 0:
        player2_score += 1
        x_pos = SCREEN_WIDTH // 2
        y_pos = SCREEN_HEIGHT // 2

    if x_pos >= SCREEN_WIDTH:
        player1_score += 1
        x_pos = SCREEN_WIDTH // 2
        y_pos = SCREEN_HEIGHT // 2

    #Create Left Paddle
    pygame.draw.line(screen, paddle_color, [25, left_paddle_pos - 25], [25, left_paddle_pos + 25], 10)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
       left_paddle_pos -= 10
    if keys[pygame.K_s]:
        left_paddle_pos += 10
    #if paddle_order[0] < paddle_order[1]:
    #    left_paddle_pos = paddle_pos[0]
    #    right_paddle_pos = paddle_pos[1]
    #else:
    #    left_paddle_pos = paddle_pos[1]
    #    right_paddle_pos = paddle_pos[0]
    #Create Right Paddle
    pygame.draw.line(screen, paddle_color, [SCREEN_WIDTH - 25, right_paddle_pos - 25], [SCREEN_WIDTH - 25, right_paddle_pos + 25], 10)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        right_paddle_pos -= 10
    if keys[pygame.K_DOWN]:
        right_paddle_pos += 10
    

    #Ball Bounces off the paddles
    if (x_pos <= 35
            and y_pos <= left_paddle_pos + 25 and y_pos >= left_paddle_pos - 25 and x_mov < 0):
        x_mov *= -1
        paddle_color = pygame.Color(random.randint(30, 255), random.randint(30, 255), random.randint(30, 255)) #not black

    if (x_pos >= SCREEN_WIDTH - 35
            and y_pos <= right_paddle_pos + 25 and y_pos >= right_paddle_pos - 25 and x_mov > 0):
        x_mov *= -1
        paddle_color = pygame.Color(random.randint(30, 255), random.randint(30, 255), random.randint(30, 255)) #not black


    #Keep Score (If ball passes off screen, one point to player)
    text = pygame.font.SysFont("timensnewroman", 50).render("Catherine's Score = " + str(player1_score), True, "grey")
    screen.blit(text, [SCREEN_WIDTH // 2 - text.get_width(), 50])

    text = pygame.font.SysFont("timensnewroman", 50).render("Enemy's Score = " + str(player2_score), True, "grey")
    screen.blit(text, [SCREEN_WIDTH // 2 - text.get_width(), 100])

    if player1_score == 100 or player2_score == 100:
        text = pygame.font.SysFont("timensnewroman", 100).render("Winner!!!!", True, "darkgreen")
        screen.blit(text, [SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2])
        running = False

    pygame.display.flip()

    #screen.fill("black")
    screen.fill(screen_color)

    clock.tick(CLOCK_TICK)

# End game loop to wait for user to click X

while end_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # User clicked the window's X button
            end_running = False
pygame.quit()
sys.exit(1)