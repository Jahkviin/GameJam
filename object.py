import pygame

class Object:
    global objects
    objects = []

    def __init__(self, position, size, velocity):
        self.position = position
        self.size = size
        self.velocity = velocity

        objects.append(self)

    def changeVel(self, velocity):
        self.velocity = velocity