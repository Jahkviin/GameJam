import item
import os
import pygame

class FastForward(item.Item):
    def __init__(self, position):
        super().__init__(position)
        self.image = pygame.image.load(os.path.join("textures", "fastForward.png"))

    def use(self, vhsSpeed):
        return pygame.Vector2(2, 3) #times 2 speed for 3 seconds