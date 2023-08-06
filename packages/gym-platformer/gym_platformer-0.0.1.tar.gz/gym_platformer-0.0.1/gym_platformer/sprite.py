import pygame
from pygame.math import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, starting_pos):
        super().__init__()
        self.pos = Vector2(starting_pos)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

    def draw(self, surface):
        return

    def update(self, inputs):
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

class Rect(Sprite):
    def __init__(self, starting_pos, size, color):
        super().__init__(starting_pos)
        self.color = color
        self.size = size
        self.rect = createRect(self.pos, self.size[0], self.size[1])

    def draw(self, surface):
        drawRect(surface, self.color, self.pos, self.size[0], self.size[1])

    def update(self, pressed_keys):
        super().update(pressed_keys)
        self.rect = createRect(self.pos, self.size[0], self.size[1])


def createRect(pos, s1, s2):
    return pygame.Rect((pos[0] - s1 / 2, pos[1] - s2 / 2), (s1, s2))


def drawRect(surface, color, pos, s1, s2):
    pygame.draw.rect(surface, color, createRect(pos, s1, s2))


