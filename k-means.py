import pygame
import os
import math
import random

os.environ['SDL_VIDEO_CENTERED'] = '1'

nr_data = 350  # number of data points
nr_cen = 3  # number of centroids
edge = 500


class Data:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.flag = -1


class Average:
    def __init__(self):
        self.sum_x = 0
        self.sum_y = 0
        self.divisor = 0


def distance(centroid, data):
    x_difference = centroid.x - data.x
    y_difference = centroid.y - data.y
    return math.sqrt(x_difference*x_difference + y_difference*y_difference)


data_points = [Data(random.randint(1, edge), random.randint(1, edge))
               for i in range(nr_data)]
centroids = [Data(random.randint(1, edge), random.randint(1, edge))
             for i in range(nr_cen)]
averages = [Average() for i in range(nr_cen)]
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

pygame.init()

screen = pygame.display.set_mode([edge, edge])
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for x in range(100):
        screen.fill((255, 255, 255))
        for i in range(nr_cen):
            pygame.draw.circle(screen, colors[i],
                               (centroids[i].x, centroids[i].y), 5)
        for i in range(nr_data):
            if data_points[0].flag == -1:
                pygame.draw.circle(screen, (0, 0, 0),
                                   (data_points[i].x, data_points[i].y), 3)
            else:
                pygame.draw.circle(screen, colors[data_points[i].flag],
                                   (data_points[i].x, data_points[i].y), 3)
        pygame.display.flip()
        clock.tick(1)
        for i in range(nr_cen):
            averages[i].sum_x = 0
            averages[i].sum_y = 0
            averages[i].divisor = 0

        for i in range(nr_data):
            data = data_points[i]
            min = -1
            for j in range(nr_cen):
                centroid = centroids[j]
                dist = distance(centroid, data)
                if dist < min or min == -1:
                    min = dist
                    data.flag = j
            averages[data.flag].sum_x += data.x
            averages[data.flag].sum_y += data.y
            averages[data.flag].divisor += 1
        for i in range(nr_cen):
            centroids[i].x = averages[i].sum_x/averages[i].divisor
            centroids[i].y = averages[i].sum_y/averages[i].divisor
            centroids[i].x = int(round(centroids[i].x))
            centroids[i].y = int(round(centroids[i].y))
pygame.quit()
