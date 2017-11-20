import pygame
from pygame import display, draw, time, event
from random import randint

xmax = 960
ymax = 710


class Drop:
    def __init__(self):
        self.center = [randint(0, xmax), randint(0, ymax)]
        self.radius = 1
        self.rmax = randint(20, 50)
        channel = randint(0, 255)
        self.color = [channel, channel, channel]


def main():
    screen = display.set_mode([xmax, ymax])
    drops = []
    clock = time.Clock()
    animate = True

    while animate:
        screen.fill([0, 0, 0])
        for d in drops.copy():
            draw.circle(screen, d.color, d.center, d.radius, 1)
            d.radius += 1
            if d.radius >= d.rmax:
                drops.remove(d)
        drops.append(Drop())
        display.flip()
        clock.tick(60)
        if event.poll().type == pygame.KEYDOWN:
            break


if __name__ == "__main__":
    main()
