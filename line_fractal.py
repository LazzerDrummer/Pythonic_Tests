import math
import os
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

x = 800
y = 600
max_iterations = 16
branch_angle = 15
starter_line_size = 140  # 100, 140
line_multiplier = 0.70   # 0.80, 0.70
frames = 40

size = [x, y]
window = pygame.display.set_mode(size)
pygame.display.set_caption('Fractal Tree')


def draw_lines(angle, decrease, point, length, length_multiplier, max_iteration, iterations=1):
    if iterations == 1:
        angle = math.radians(angle)
        decrease = math.radians(decrease)
    finish_point = [point[0] - length * math.sin(angle - decrease), point[1] - length * math.cos(angle - decrease)]
    pygame.draw.line(window, BLACK, point, finish_point, 1)
    if iterations < max_iteration:
        iterations += 1
        draw_lines(angle, decrease - angle, finish_point, length * length_multiplier, length_multiplier,
                   max_iteration, iterations)
        draw_lines(angle, decrease + angle, finish_point, length * length_multiplier, length_multiplier,
                   max_iteration, iterations)


done = False
clock = pygame.time.Clock()

while not done:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    window.fill(WHITE)
    for i in range(max_iterations):
        draw_lines(branch_angle, branch_angle, [x/2, y], starter_line_size, line_multiplier, i)
        pygame.display.flip()
        clock.tick(frames)
    clock.tick(2)

pygame.quit()
