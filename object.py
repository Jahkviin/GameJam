import pygame

class Object:
    global objects
    objects = []

    def __init__(self, rect, velocity):
        self.rect = rect
        self.velocity = velocity

        objects.append(self)

    def changeVel(self, velocity):
        self.velocity = velocity