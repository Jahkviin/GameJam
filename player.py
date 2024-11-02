import pygame

class Player:
    global players #List of players
    players = []

    def __init__ (self, position):
        self.position = position
        self.velocity = pygame.Vector2(0,0)
        self.isGrounded = False

        self.speedLimit = 250 #The fastest speed players can move.
        self.speed = 80 #The acceleration of players.
        self.decelaration = 0.8 #The deceleration of players (multiplicative).
        self.gravity = 4 #The gravity strength.
        self.jumpStrength = 100 #Jump height and speed

        players.append(self)
    
    def move(self, xdir):
        self.velocity.x += xdir * self.speed

        if (self.velocity.x.__abs__() > self.speedLimit):
            self.velocity.x = self.velocity.x / self.velocity.x.__abs__() * self.speedLimit

    def physicsUpdate(self, dt):
        #Horizontal movement
        self.position += self.velocity * dt
        self.velocity.x *= self.decelaration

        #Gravity
        if (self.isGrounded == False):
            self.velocity.y += self.gravity
            self.position.y += self.velocity.y * dt

        #"Is grounded" logic
        if (self.position.y >= 400 and self.isGrounded == False):
            self.isGrounded = True
            self.velocity.y = 0
            self.position.y = 400
        elif (self.position.y < 400 and self.isGrounded):
            self.isGrounded = False

    def jump(self):
        if (self.isGrounded):
            self.velocity.y -= self.jumpStrength