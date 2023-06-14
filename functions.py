import math
import random


def find_closest_food(fish_x, fish_y, foods_x, foods_y):
    closest_food_index = None
    closest_distance = float('inf')

    for i in range(len(foods_x)):
        distance = math.sqrt((fish_x - foods_x[i]) ** 2 + (fish_y - foods_y[i]) ** 2)
        if distance < closest_distance:
            closest_distance = distance
            closest_food_index = i

    return closest_food_index


def check_collision(fish_x, fish_y, fish_radius, food_x, food_y, food_radius):
    distance = math.sqrt((fish_x - food_x) ** 2 + (fish_y - food_y) ** 2)
    return distance < fish_radius + food_radius


def is_too_close(fish1_x, fish1_y, fish2_x, fish2_y, min_distance):
    distance = math.sqrt((fish1_x - fish2_x) ** 2 + (fish1_y - fish2_y) ** 2)
    return distance < min_distance


def generate_new_food(screen_width, screen_height, foods_x, foods_y):
    random_food_x = random.randint(0, screen_width - 50)
    random_food_y = random.randint(0, screen_height - 50)
    foods_x.append(random_food_x)
    foods_y.append(random_food_y)


