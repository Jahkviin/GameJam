import pygame
import object
import item
import math

class Player:
    global players #List of players
    players = []

    def __init__ (self, position, textureForward, textureLeft, textureLeftUp):
        self.position = position
        self.size = pygame.Vector2(24, 36)
        self.velocity = pygame.Vector2(0,0)
        self.isGrounded = False
        self.item = None

        self.isFacingLeft = False

        self.textureForward = textureForward
        self.textureLeft = textureLeft
        self.textureLeftUp = textureLeftUp

        self.jumpTimer = 0
        self.jumpStun = 0.3 #Time between landing and jumping again

        self.speedLimit = 250 #The fastest speed players can move.
        self.speed = 80 #The acceleration of players.
        self.airDeceleration = 0.8 #The deceleration of players (multiplicative).
        self.groundDeceleration = 0.5
        self.gravity = 4 #The gravity strength.
        self.jumpStrength = 150 #Jump height and speed

        self.isDead = False

        self.texture = textureForward

        players.append(self)
    
    def move(self, xdir):
        if (self.isDead == False):
            self.velocity.x += xdir * self.speed
            if (self.velocity.x.__abs__() > self.speedLimit):
                self.velocity.x *= 0.9

    def physicsUpdate(self, dt):
        #Horizontal movement
        self.position.x += self.velocity.x * dt
        if (self.isGrounded):
            self.velocity.x *= self.groundDeceleration
        else:
            self.velocity.x *= self.airDeceleration

        self.isGrounded = False

        if (self.isDead == False):
            #Horizontal collision
            for r in object.objects:
                if (pygame.Rect.colliderect(pygame.Rect(r.position, r.size), pygame.Rect(self.position, self.size))):
                    self.velocity.x = r.velocity
                    if (r.position.x > self.position.x):
                        self.position.x = r.position.x - self.size.x
                    else:
                        self.position.x = r.position.x + r.size.x

            if (self.position.x < 0):
                self.position.x = 0
                for r in object.objects:
                    if (pygame.Rect.colliderect(pygame.Rect(r.position, r.size), pygame.Rect(self.position, self.size))):
                        self.isDead = True #Crushed
            elif (self.position.x + self.size.x > 640):
                self.position.x = 640 - self.size.x
                for r in object.objects:
                    if (pygame.Rect.colliderect(pygame.Rect(r.position, r.size), pygame.Rect(self.position, self.size))):
                        self.isDead = True #Crushed

        #Gravity
        self.velocity.y += self.gravity
        self.position.y += self.velocity.y * dt

        if (self.isDead == False):
            #Vertical collision
            for r in object.objects:
                if (pygame.Rect.colliderect(pygame.Rect(r.position, r.size), pygame.Rect(self.position, self.size).inflate(0, 1))): 
                    if (self.velocity.y >= 0):   #Block below
                        self.isGrounded = True
                        self.velocity.y = 0
                        self.position.y = r.position.y - self.size.y
                    else:                       #Block above
                        self.velocity.y = 0
                        self.position.y = r.position.y + r.size.y

        #"Is grounded" logic
        if (self.position.y + self.size.y >= 400 and self.isGrounded == False and self.position.x <= 550 and self.position.x + self.size.x >= 110):
            self.isGrounded = True
            self.velocity.y = 0
            self.position.y = 400 - self.size.y

        #Item pickup logic
        if (self.isDead == False):
            for i in item.items:
                if (math.hypot(self.position.x + self.size.x/2 - i.position.x, self.position.y + self.size.y/2 - i.position.y) < 15):
                    self.item = i
                    i.claimed()

        if (self.isGrounded and self.jumpTimer > 0):
            self.jumpTimer -= dt

        #Dead logic
        if (self.position.y > 400):
            self.isDead = True

        #Sprite logic
        if (self.isGrounded == False):
            self.texture = self.textureLeftUp
        elif (abs(self.velocity.x) > 1):
            self.texture = self.textureLeft
        else:
            self.texture = self.textureForward
        
        if (self.velocity.x > 0):
            self.isFacingLeft = False
        else:
            self.isFacingLeft = True

    def jump(self):
        if (self.isGrounded and self.jumpTimer <= 0):
            self.velocity.y -= self.jumpStrength
            self.isGrounded = False
            self.jumpTimer = self.jumpStun

    def useItem(self, vhsSpeed):
        if (self.isDead == False and self.item != None):
            vhsMod = self.item.use(vhsSpeed)
            self.item = None
            return vhsMod
        else:
            return None