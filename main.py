import pygame
import player
import object

# pygame setup
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
running = True
dt = 0

#VHS stats
vhsSpeed = 0

object.Object(pygame.Rect(40, 380, 40, 40), vhsSpeed)
object.Object(pygame.Rect(40, 380, 40, 40), vhsSpeed)
object.Object(pygame.Rect(0, 360, 40, 40), vhsSpeed)
player1 = player.Player(pygame.Rect(screen.get_width()/2, screen.get_height()/2, 8, 8))

#Functions
def changeVHSspeed(speed):
    global vhsSpeed
    vhsSpeed = speed
    for o in object.objects:
        o.changeVel(speed)

#Gameloop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Logic here
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player1.move(-1)
    if keys[pygame.K_d]:
        player1.move(1)
    if keys[pygame.K_w]:
        player1.jump()

    #Temporary for testing
    if keys[pygame.K_j]:
        changeVHSspeed(-100)
    if keys[pygame.K_k]:
        changeVHSspeed(100)

    for o in object.objects:
        o.rect.x += vhsSpeed * dt

    for p in player.players:
        p.physicsUpdate(dt)
        if (p.isGrounded):
            p.rect.x += vhsSpeed * dt

    # Render game here
    screen.fill("purple")

    for o in object.objects:
        pygame.draw.rect(screen, "green", o.rect)

    for p in player.players:
        pygame.draw.rect(screen, p.color, p.rect)

    pygame.display.flip()

    dt = clock.tick(60) / 1000  # limits FPS and gives the delta time (dt)

pygame.quit()