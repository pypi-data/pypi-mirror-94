import random
import sys

import pygame
from pygame.locals import *
from pygame.math import *
import numpy as np

from gym_platformer import sprite


class EffectPlatform(sprite.Rect):
    def __init__(self, starting_pos, size, jump, speed, fric, effect_size):
        super().__init__(starting_pos, size, (255, 0, 255))
        self.jump = jump
        self.speed = speed
        self.fric = fric
        self.effect_size = effect_size


class Player(sprite.Rect):
    def __init__(self, starting_pos):
        self.spawn_pos = Vector2(starting_pos)
        self.defaults()
        super().__init__(starting_pos, (self.SIZE, self.SIZE), (0, 255, 0))
        self.prev_rect = self.rect
        self.bottom = False
        self.left = False
        self.right = False
        self.top = False
        self.platform = 0

    def defaults(self):
        self.ACC = 0.5
        self.GRAV = 0.5
        self.JUMP = 10
        self.FRIC = -0.12
        self.AIR_FRIC = -0.08
        self.SIZE = 30

    def update(self, action):
        left, right, up = action

        done = False
        reward = 0

        super().update(action)
        self.acc = Vector2(0, self.GRAV)

        if left:
            self.acc.x = -self.ACC
        if right:
            self.acc.x = self.ACC

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        hits = pygame.sprite.spritecollide(self, platforms, False)

        if hits and not self.bottom:
            for hit in hits:
                if self.rect.bottom >= hit.rect.top >= self.prev_rect.bottom:
                    self.bottom = hit
        elif self.bottom not in hits and self.bottom:
            self.bottom = False

        if hits and not self.left:
            for hit in hits:
                if self.rect.left <= hit.rect.right <= self.prev_rect.left:
                    self.left = hit
        elif self.left not in hits and self.left:
            self.left = False

        if hits and not self.top:
            for hit in hits:
                if self.rect.top <= hit.rect.bottom <= self.prev_rect.top:
                    self.top = hit
        elif self.top not in hits and self.top:
            self.top = False

        if hits and not self.right:
            for hit in hits:
                if self.rect.right >= hit.rect.left >= self.prev_rect.right:
                    self.right = hit
        elif self.right not in hits and self.right:
            self.right = False

        for i in range(self.platform + 1, len(platforms.sprites())):
            if platforms.sprites()[i] == self.bottom:
                self.platform = i
                reward = 10
            if platforms.sprites()[i] == self.left:
                self.platform = i
                reward = 3
            if platforms.sprites()[i] == self.right:
                self.platform = i
                reward = 3
            if platforms.sprites()[i] == self.top:
                self.platform = i
                reward = 1

        if self.bottom:
            self.pos.y = self.bottom.rect.top + 1 - self.SIZE / 2
            self.vel.y = min(self.vel.y, 0)
            self.acc.x += self.vel.x * self.FRIC
            if isinstance(self.bottom, EffectPlatform):
                self.ACC = self.bottom.speed
                self.JUMP = self.bottom.jump
                self.FRIC = self.bottom.fric
                self.AIR_FRIC = 3 * self.bottom.fric / 4
                self.SIZE = self.bottom.effect_size
            else:
                self.defaults()

            if up:
                self.vel.y = -self.JUMP
        else:
            self.acc.x += self.vel.x * self.AIR_FRIC

        if self.left:
            self.pos.x = self.left.rect.right + 1 + self.SIZE / 2
            self.vel.x = -self.vel.x

        if self.top:
            self.pos.y = self.top.rect.bottom - 1 + self.SIZE / 2
            self.vel.y = -self.vel.y

        if self.right:
            self.pos.x = self.right.rect.left - 1 - self.SIZE / 2
            self.vel.x = -self.vel.x

        if self.bottom == goal or self.top == goal or self.right == goal or self.left == goal:
            reward = 40
            done = True

        if self.pos[1] >= HEIGHT:
            reward = -5
            done = True

        self.prev_rect = self.rect

        return done, reward


def pos(x, y):
    return Vector2(x * WIDTH, (1 - y) * HEIGHT)


WIDTH = 1000
HEIGHT = 1000

sprites = []
platforms = pygame.sprite.Group()
player = Player(pos(0.5, 0.2))
goal = sprite.Rect(pos(0.55, 0.65), (30, 30), (255, 255, 0))

surf = None
clock = None


def create():
    global clock
    global surf

    pygame.init()

    clock = pygame.time.Clock()


def createMap():
    platforms.add(sprite.Rect(pos(0.5, 0.1), (100, 30), (0, 0, 255)))
    platforms.add(sprite.Rect(pos(0.7, 0.18), (100, 30), (0, 0, 255)))
    platforms.add(sprite.Rect(pos(0.5, 0.26), (170, 30), (0, 0, 255)))
    platforms.add(EffectPlatform(pos(0.12, 0.26), (100, 30), 15, 0.5, -0.12, 30))
    platforms.add(sprite.Rect(pos(0.39, 0.46), (30, 30), (0, 0, 255)))
    platforms.add(sprite.Rect(pos(0.6, 0.5), (30, 30), (0, 0, 255)))
    platforms.add(sprite.Rect(pos(0.79, 0.54), (30, 30), (0, 0, 255)))
    platforms.add(sprite.Rect(pos(0.01, 0.54), (30, 30), (0, 0, 255)))
    platforms.add(EffectPlatform(pos(0.2, 0.6), (100, 30), 10, 0.5, -0.06, 30))
    platforms.add(goal)


def observate():
    observations = [player.pos[1] - platforms.sprites()[player.platform].pos[1],
                    player.pos[0] - platforms.sprites()[player.platform].rect.right,
                    player.pos[0] - platforms.sprites()[player.platform].rect.left,
                    player.pos[0] - platforms.sprites()[player.platform + 1].pos[0],
                    player.pos[1] - platforms.sprites()[player.platform + 1].pos[1],
                    player.pos[0] - platforms.sprites()[player.platform + 1].rect.right,
                    player.pos[1] - platforms.sprites()[player.platform + 1].rect.left,
                    player.vel[0],
                    player.vel[1],
                    player.acc[0],
                    player.acc[1]]
    return np.array(observations)


def sample():
    return random.randint(0, 7)


def step(action):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    player_movement = [False, False, False]
    if action >= 4:
        action -= 4
        player_movement[0] = True
    if action >= 2:
        action -= 2
        player_movement[1] = True
    if action >= 1:
        action -= 1
        player_movement[2] = True

    state = observate()

    done, reward = player.update(player_movement)

    return done, state, reward


def reset():
    global platforms
    global player
    global goal
    platforms = pygame.sprite.Group()
    player = Player(pos(0.5, 0.2))
    goal = sprite.Rect(pos(0.55, 0.65), (30, 30), (255, 255, 0))
    createMap()
    return observate()


def display():
    global surf
    if(surf == None):
        surf = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game")

    surf.fill((0, 0, 0))
    for platform in platforms:
        platform.draw(surf)

    goal.draw(surf)
    player.draw(surf)
    pygame.display.update()

def close():
    global surf
    pygame.display.quit()
    surf = None