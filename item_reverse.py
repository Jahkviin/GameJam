import item
import os
import pygame

class reverse(item.Item):
    def __init__(self, position):
        super().__init__(position)
        self.image = pygame.image.load(os.path.join("textures", "rewind.png"))

    def use(self, vhsSpeed):
        vhsSpeed = -vhsSpeed
        return pygame.Vector2(-1, 4)