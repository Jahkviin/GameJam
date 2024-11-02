import item
import os
import pygame

class Pause(item.Item):
    def __init__(self, position):
        super().__init__(position)
        self.image = pygame.image.load(os.path.join("textures", "pause.png"))

    def use(self, vhsSpeed):
        vhsSpeed = -vhsSpeed
        return pygame.Vector2(0, 2) #0 speed for 2 seconds