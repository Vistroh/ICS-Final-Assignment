import pygame
import random
import math
from pygame.locals import *
from functions import *

pygame.init()
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), NOFRAME)
clock = pygame.time.Clock()
running = False  # Updated: Game starts when "Start" button is pressed
start_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2 - 25, 100, 50)  # Rect for the "Start" button
ball_size = [50, 25]
sword_size = [80, 80]  # Updated swordfish size
sword_hitbox_radius = 25  # Radius of the swordfish hitbox
random_ball_x = random.randint(0, screen_width - 50)
random_ball_y = random.randint(0, screen_height - 50)
random_food_x = random.randint(0, screen_width - 50)
random_food_y = random.randint(0, screen_height - 50)

sword_x = screen_width / 2
sword_y = screen_height / 2
x_change = 0
y_change = 0
balls_x = []
balls_y = []
num_balls = 20
num_foods = 50
ball_speed = 5
ball_speeds = []
foods_x = []
foods_y = []
food_assignments = []
fish_timers = []
fish_timeout = 2000  # Timeout in milliseconds

swordfish = pygame.image.load("sword0.png")
swordfish = pygame.transform.scale(swordfish, sword_size)

goldfish = pygame.image.load("goldfish.png")
goldfish = pygame.transform.scale(goldfish, ball_size)

increase_chance = 0.1  # Probability of speed increase
decrease_chance = 0.1  # Probability of speed decrease

# Game loop
while not running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Check if left mouse button is pressed
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    running = True

    screen.fill("black")

    # Draw the "Start" button
    pygame.draw.rect(screen, "green", start_button)
    start_font = pygame.font.SysFont(None, 30)
    start_text = start_font.render("Start", True, "black")
    start_text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_text_rect)

    pygame.display.update()
    clock.tick(60)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord("w"):
                y_change -= 3
            if event.key == pygame.K_DOWN or event.key == ord("s"):
                y_change += 3
            if event.key == pygame.K_LEFT or event.key == ord("a"):
                x_change -= 3
            if event.key == pygame.K_RIGHT or event.key == ord("d"):
                x_change += 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == ord("w"):
                y_change += 3
            if event.key == pygame.K_DOWN or event.key == ord("s"):
                y_change -= 3
            if event.key == pygame.K_LEFT or event.key == ord("a"):
                x_change += 3
            if event.key == pygame.K_RIGHT or event.key == ord("d"):
                x_change -= 3

    sword_x += x_change
    sword_y += y_change

    screen.fill("black")

    for i in range(len(balls_x)):
        closest_food_index = find_closest_food(balls_x[i], balls_y[i], foods_x, foods_y)
        if closest_food_index is not None:
            closest_food_x = foods_x[closest_food_index]
            closest_food_y = foods_y[closest_food_index]

            angle = math.atan2(closest_food_y - balls_y[i], closest_food_x - balls_x[i])
            dx = ball_speed * math.cos(angle)
            dy = ball_speed * math.sin(angle)

            new_x = balls_x[i] + dx
            new_y = balls_y[i] + dy
    

            # Check collision with other fish
            collided = False
            for j in range(len(balls_x)):
                if i != j and math.sqrt((new_x - balls_x[j]) ** 2 + (new_y - balls_y[j]) ** 2) < ball_size[0]:
                    collided = True
                    break

            if collided:
                # Random movement when collision occurs
                dx = random.uniform(-1, 1)
                dy = random.uniform(-1, 1)
            else:
                # Check collision with swordfish
                distance_to_swordfish = math.sqrt((new_x - sword_x) ** 2 + (new_y - sword_y) ** 2)
                if distance_to_swordfish+100 < sword_hitbox_radius:
                    # Avoid the swordfish
                    angle_to_swordfish = math.atan2(sword_y - balls_y[i], sword_x - balls_x[i])
                    dx = -ball_speed * math.cos(angle_to_swordfish)
                    dy = -ball_speed * math.sin(angle_to_swordfish)

            balls_x[i] += dx
            balls_y[i] += dy

            if check_collision(balls_x[i], balls_y[i], ball_size[0] // 2,
                               closest_food_x, closest_food_y, 2):
                del foods_x[closest_food_index]
                del foods_y[closest_food_index]
                generate_new_food(screen_width, screen_height, foods_x, foods_y)

                # Reset the fish timer
                fish_timers[i] = pygame.time.get_ticks()

                # Speed modification
                speed_modifier = random.choices([0.95, 1.0, 1.05], [decrease_chance, 1 - increase_chance - decrease_chance, increase_chance])[0]
                dx *= speed_modifier
                dy *= speed_modifier

        else:
            balls_x[i] += ball_speeds[i][0] * ball_speed
            balls_y[i] += ball_speeds[i][1] * ball_speed
            if balls_x[i] < 0 or balls_x[i] > screen_width - ball_size[0]:
                ball_speeds[i][0] *= -1
            if balls_y[i] < 0 or balls_y[i] > screen_height - ball_size[1]:
                ball_speeds[i][1] *= -1

        # Check if the fish has timed out
        if pygame.time.get_ticks() - fish_timers[i] > fish_timeout:
            del balls_x[i]
            del balls_y[i]
            del ball_speeds[i]
            del fish_timers[i]
            break

    # Check for collisions between balls
    for i in range(len(balls_x)):
        for j in range(i + 1, len(balls_x)):
            if is_too_close(balls_x[i], balls_y[i], balls_x[j], balls_y[j], 50):
                # Move the balls away from each other
                angle = math.atan2(balls_y[j] - balls_y[i], balls_x[j] - balls_x[i])
                dx = 2 * math.cos(angle)
                dy = 2 * math.sin(angle)
                balls_x[i] -= dx
                balls_y[i] -= dy
                balls_x[j] += dx
                balls_y[j] += dy

    # Collision detection between swordfish and goldfish
    for i in range(len(balls_x)):
        distance = math.sqrt((sword_x - balls_x[i]) ** 2 + (sword_y - balls_y[i]) ** 2)
        if distance < sword_hitbox_radius:
            del balls_x[i]
            del balls_y[i]
            del ball_speeds[i]
            del fish_timers[i]
            break

    # Draw goldfish on the screen
    for i in range(len(balls_x)):
        screen.blit(goldfish, (int(balls_x[i] - ball_size[0] // 2), int(balls_y[i] - ball_size[1] // 2)))

    for i in range(len(foods_x)):
        pygame.draw.circle(screen, "white", [int(foods_x[i]), int(foods_y[i])], 2)

    while len(foods_x) < num_foods:
        random_food_x = random.randint(0, screen_width - 50)
        random_food_y = random.randint(0, screen_height - 50)
        foods_x.append(random_food_x)
        foods_y.append(random_food_y)

    while len(balls_x) < num_balls:
        random_ball_x = random.randint(0, screen_width - 50)
        random_ball_y = random.randint(0, screen_height - 50)

        # Check if the new ball is too close to existing balls
        while any(is_too_close(random_ball_x, random_ball_y, bx, by, 50) for bx, by in zip(balls_x, balls_y)):
            random_ball_x = random.randint(0, screen_width - 50)
            random_ball_y = random.randint(0, screen_height - 50)

        balls_x.append(random_ball_x)
        balls_y.append(random_ball_y)
        ball_speeds.append([random.choice([-1, 1]), random.choice([-1, 1])])
        fish_timers.append(pygame.time.get_ticks())

    screen.blit(swordfish, (int(sword_x - sword_size[0] // 2), int(sword_y - sword_size[1] // 2)))

    pygame.display.update()
    clock.tick(60)

pygame.quit()