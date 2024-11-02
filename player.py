import pygame
import object

class Player:
    global players #List of players
    players = []

    def __init__ (self, rect, color):
        self.rect = rect
        self.velocity = pygame.Vector2(0,0)
        self.isGrounded = False

        self.speedLimit = 250 #The fastest speed players can move.
        self.speed = 80 #The acceleration of players.
        self.airDeceleration = 0.8 #The deceleration of players (multiplicative).
        self.groundDeceleration = 0.5
        self.gravity = 4 #The gravity strength.
        self.jumpStrength = 150 #Jump height and speed

        self.isDead = False

        self.color = color

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

        #Dead logic
        if (self.rect.y > 400):
            self.isDead = True

    def jump(self):
        if (self.isGrounded):
            self.velocity.y -= self.jumpStrength
            self.isGrounded = False