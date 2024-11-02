import pygame

class Item:
    global items
    items = []

    def __init__(self, position):
        self.position = position

        items.append(self)

    def claimed(self):
        items.remove(self)

    def use(self): #use the item
        pass