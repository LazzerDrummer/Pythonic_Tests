import math
import os
import pygame


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()

    black = (0, 0, 0)
    white = (255, 255, 255)

    x = 1100
    y = 1000
    max_iteration = 16
    left_angle = 20 * (math.pi / 180)
    # right_angle = 40 * (math.pi / 180)
    starter_line_size = 180  # 100, 140
    left_line_multiplier = 0.55  # 0.80, 0.70
    right_line_multiplier = 0.85
    y_position = 4 / 5
    frames = 60

    size = [x, y]
    window = pygame.display.set_mode(size)
    pygame.display.set_caption('Fractal Tree')

    def draw_line(point, length, iterations=1, branch_angle=0):
        finish_point = [point[0] + length * math.sin(branch_angle),
                        point[1] - length * math.cos(branch_angle)]
        pygame.draw.line(window, black, point, finish_point, 1)
        if iterations < max_iteration:
            iterations += 1
            draw_line(finish_point, length * left_line_multiplier, iterations, branch_angle=branch_angle - left_angle)
            draw_line(finish_point, length * right_line_multiplier, iterations, branch_angle=branch_angle + right_angle)

    done = False
    clock = pygame.time.Clock()

    while not done:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # for i_max_iteration in range(max_iteration):
        #     window.fill(white)
        #     draw_line([x/2, y*4/5], starter_line_size)
        #     pygame.display.flip()
        #     clock.tick(frames)
        # clock.tick(2)

        for i in range(360):
            window.fill(white)
            right_angle = i * (math.pi / 180)
            draw_line([x / 2, y * y_position], starter_line_size)
            pygame.display.flip()
            clock.tick(frames)

    pygame.quit()


if __name__ == '__main__':
    main()
