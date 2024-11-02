import pygame
import player
import object
import os
import item

# pygame setup
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
running = True
dt = 0

#VHS stats
vhsSpeed = 0
vhsTapePos = 0
vhsWheelRot = 0

player1 = player.Player(pygame.Rect(screen.get_width()/2, screen.get_height()/2, 24, 36), "red")
player2 = player.Player(pygame.Rect(screen.get_width()/2, screen.get_height()/2, 24, 36), "orange")

#Temp
object.Object(pygame.Rect(90, 370, 70, 10), vhsSpeed)
object.Object(pygame.Rect(40, 350, 30, 30), vhsSpeed)
object.Object(pygame.Rect(0, 330, 40, 40), vhsSpeed)
item.Item(pygame.Vector2(240, 370))
item.Item(pygame.Vector2(470, 370))

tapeTexture = pygame.image.load(os.path.join("textures", "vhs tape.png"))
wheelTexture = pygame.image.load(os.path.join("textures", "vhs wheel.png"))

#Functions
def changeVHSspeed(speed):
    global vhsSpeed
    vhsSpeed = speed
    for o in object.objects:
        o.changeVel(speed)

def blitRotateCenter(surf, image, topleft, angle): #Rotates an image around its centre and draws it

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect)

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
    if keys[pygame.K_e]:
        player1.useItem()

    if keys[pygame.K_LEFT]:
        player2.move(-1)
    if keys[pygame.K_RIGHT]:
        player2.move(1)
    if keys[pygame.K_UP]:
        player2.jump()
    if keys[pygame.K_RSHIFT]:
        player2.useItem()

    #Temporary for testing
    if keys[pygame.K_j]:
        changeVHSspeed(-100)
    if keys[pygame.K_k]:
        changeVHSspeed(100)

    #Physics/movement and such
    for o in object.objects:
        o.rect.x += vhsSpeed * dt

    for p in player.players:
        p.physicsUpdate(dt)
        if (p.isGrounded):
            p.rect.x += vhsSpeed * dt

    for i in item.items:
        i.position.x += vhsSpeed * dt

    vhsTapePos += vhsSpeed * dt
    vhsWheelRot -= vhsSpeed * dt

    # Render game here
    screen.fill("purple")

    pygame.draw.rect(screen, "gray", pygame.Rect(25, 380, 600, 100)) #Case

    screen.blit(tapeTexture, pygame.Vector2(vhsTapePos % tapeTexture.get_width(), 395))
    screen.blit(tapeTexture, pygame.Vector2(vhsTapePos % tapeTexture.get_width() + tapeTexture.get_width(), 395))
    screen.blit(tapeTexture, pygame.Vector2(vhsTapePos % tapeTexture.get_width() - tapeTexture.get_width(), 395))

    pygame.draw.rect(screen, "gray", pygame.Rect(25, 380, 75, 100)) #Case edge
    pygame.draw.rect(screen, "gray", pygame.Rect(550, 380, 75, 100)) #Case edge

    pygame.draw.rect(screen, "purple", pygame.Rect(0, 380, 25, 100)) #BG
    pygame.draw.rect(screen, "purple", pygame.Rect(615, 380, 25, 100)) #BG

    for o in object.objects:
        pygame.draw.rect(screen, "green", o.rect)

    for p in player.players:
        pygame.draw.rect(screen, p.color, p.rect)

    for i in item.items:
        pygame.draw.circle(screen, "black", i.position, 10) #Add powerup texture

    blitRotateCenter(screen, wheelTexture, pygame.Vector2(450, 390), vhsWheelRot)
    blitRotateCenter(screen, wheelTexture, pygame.Vector2(50, 390), vhsWheelRot)

    #UI
    if (player1.item != None):
        pygame.draw.circle(screen, "black", pygame.Vector2(25, 25), 15) #Draw texture
    if (player2.item != None):
        pygame.draw.circle(screen, "black", pygame.Vector2(615, 25), 15) #Draw texture

    pygame.display.flip()

    dt = clock.tick(60) / 1000  # limits FPS and gives the delta time (dt)

pygame.quit()