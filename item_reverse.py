import item
import os
import pygame

class Reverse(item.Item):
    def __init__(self, position):
        super().__init__(position)
        self.image = pygame.image.load(os.path.join("textures", "rewind.png"))

    def use(self, vhsSpeed):
        return pygame.Vector2(-1, 4) #-1 speed for 4 seconds