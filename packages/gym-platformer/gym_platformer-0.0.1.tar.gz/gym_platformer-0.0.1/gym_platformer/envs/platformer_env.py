import gym
import pygame
import numpy as np
from gym_platformer.envs import platformer
from gym_platformer import sprite
from pygame.locals import *
from gym import error, spaces, utils
from gym.utils import seeding

WIDTH = 1000
HEIGHT = 1000

class Platformer(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        platformer.create()


    def step(self, action):
        done, state, reward = platformer.step(action)
        return state, reward, done, {}

    def reset(self):
        platformer.reset()

    def render(self, mode='human'):
        self.reset()
        platformer.display()
        done = False
        while not done:
            pressed_keys = pygame.key.get_pressed()
            action = 0
            if(pressed_keys[K_LEFT]):
                action += 4
            if(pressed_keys[K_RIGHT]):
                action += 2
            if(pressed_keys[K_UP]):
                action += 1
            state, reward, done, info = self.step(action)
            platformer.display()
            platformer.clock.tick(60)
        platformer.close()
    def close(self):
        print('close')
