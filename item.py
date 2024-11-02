import pygame

class Item():
    global items
    items = []

    def __init__(self, position):
        self.position = position
        self.image = None

        items.append(self)

    def claimed(self):
        items.remove(self)

    def use(self, vhsSpeed): #use the item
        return vhsSpeed