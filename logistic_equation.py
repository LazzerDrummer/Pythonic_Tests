import pygame

p0 = 0.02
r = 4
i = 900
clock = pygame.time.Clock()


def recursive_logistic_equation(x0, rm, iteration=10):
    if iteration == 0:
        return 0
    iteration -= 1
    x = rm*x0*(1 - x0)
    print(x)
    clock.tick(10)
    recursive_logistic_equation(x, r, iteration)


recursive_logistic_equation(p0, r, i)
