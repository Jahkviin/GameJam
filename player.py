import pygame
import object
import item
import math

class Player:
    global players #List of players
    players = []

    def __init__ (self, rect, texture):
        self.rect = rect
        self.velocity = pygame.Vector2(0,0)
        self.isGrounded = False
        self.item = None

        self.speedLimit = 250 #The fastest speed players can move.
        self.speed = 80 #The acceleration of players.
        self.airDeceleration = 0.8 #The deceleration of players (multiplicative).
        self.groundDeceleration = 0.5
        self.gravity = 4 #The gravity strength.
        self.jumpStrength = 150 #Jump height and speed

        self.isDead = False

        self.texture = texture

        players.append(self)
    
    def move(self, xdir):
        if (self.isDead == False):
            self.velocity.x += xdir * self.speed
            if (self.velocity.x.__abs__() > self.speedLimit):
                self.velocity.x *= 0.9

    def physicsUpdate(self, dt):
        #Horizontal movement
        self.rect.x += self.velocity.x * dt
        if (self.isGrounded):
            self.velocity.x *= self.groundDeceleration
        else:
            self.velocity.x *= self.airDeceleration

        self.isGrounded = False

        if (self.isDead == False):
            #Horizontal collision
            for r in object.objects:
                if (pygame.Rect.colliderect(r.rect, self.rect)):
                    self.velocity.x = r.velocity
                    if (r.rect.x > self.rect.x):
                        self.rect.x = r.rect.x - self.rect.width
                    else:
                        self.rect.x = r.rect.x + r.rect.width

            if (self.rect.x < 0):
                self.rect.x = 0
            elif (self.rect.x + self.rect.width > 640):
                self.rect.x = 640 - self.rect.width

        #Gravity
        self.velocity.y += self.gravity
        self.rect.y += self.velocity.y * dt

        if (self.isDead == False):
            #Vertical collision
            for r in object.objects:
                if (pygame.Rect.colliderect(r.rect, self.rect.inflate(0, 1))): 
                    if (self.velocity.y >= 0):   #Block below
                        self.isGrounded = True
                        self.velocity.y = 0
                        self.rect.y = r.rect.y - self.rect.height
                    else:                       #Block above
                        self.velocity.y = 0
                        self.rect.y = r.rect.y + r.rect.height

        #"Is grounded" logic
        if (self.rect.y + self.rect.height >= 400 and self.isGrounded == False and self.rect.x <= 550 and self.rect.x + self.rect.width >= 110):
            self.isGrounded = True
            self.velocity.y = 0
            self.rect.y = 400 - self.rect.height

        #Item pickup logic
        if (self.isDead == False):
            for i in item.items:
                if (math.hypot(self.rect.x + self.rect.width/2 - i.position.x, self.rect.y + self.rect.height/2 - i.position.y) < 15):
                    self.item = i
                    i.claimed()

        #Dead logic
        if (self.rect.y > 400):
            self.isDead = True

    def jump(self):
        if (self.isGrounded):
            self.velocity.y -= self.jumpStrength
            self.isGrounded = False

    def useItem(self, vhsSpeed):
        if (self.isDead == False and self.item != None):
            vhsMod = self.item.use(vhsSpeed)
            self.item = None
            return vhsMod
        else:
            return None