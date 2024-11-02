import pygame
import player
import object
import os
import item
import item_reverse
import item_pause
import item_fastForward
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
running = True
dt = 0

itemTypes = [item_reverse.Reverse, item_fastForward.FastForward, item_pause.Pause]
itemSpawnTimer = 0
itemSpawnRate = 6

#VHS stats
vhsSpeed = 20
modVHSspeed = 0
vhsModTimer = 0
vhsTapePos = 0
vhsWheelRot = 0

player1 = player.Player(pygame.Vector2(screen.get_width()/2, screen.get_height()/2), pygame.image.load(os.path.join("textures", "neo standing.png")), pygame.image.load(os.path.join("textures", "neo left.png")), pygame.image.load(os.path.join("textures", "neo left up.png")))
player2 = player.Player(pygame.Vector2(screen.get_width()/2, screen.get_height()/2), pygame.image.load(os.path.join("textures", "lara croft.png")), pygame.image.load(os.path.join("textures", "lara croft left.png")), pygame.image.load(os.path.join("textures", "lara croft left up.png")))

#Temp
object.Object(pygame.Vector2(90, 370), pygame.Vector2(70, 10), vhsSpeed)
object.Object(pygame.Vector2(40, 350), pygame.Vector2(30, 30), vhsSpeed)
object.Object(pygame.Vector2(0, 330), pygame.Vector2(40, 40), vhsSpeed)
item_fastForward.FastForward(pygame.Vector2(240, 370))
item_pause.Pause(pygame.Vector2(470, 370))

#Textures
tapeTexture = pygame.image.load(os.path.join("textures", "vhs tape.png"))
wheelTexture = pygame.image.load(os.path.join("textures", "vhs wheel.png"))
wheelHighlightTexture = pygame.image.load(os.path.join("textures", "vhs wheel highlight.png"))

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
        result = player1.useItem(vhsSpeed)
        if (result != None):
            modVHSspeed = result.x
            vhsModTimer = result.y

    if keys[pygame.K_LEFT]:
        player2.move(-1)
    if keys[pygame.K_RIGHT]:
        player2.move(1)
    if keys[pygame.K_UP]:
        player2.jump()
    if keys[pygame.K_RSHIFT]:
        result = player2.useItem(vhsSpeed)
        if (result != None):
            modVHSspeed = result.x
            vhsModTimer = result.y

    #Temporary for testing
    if keys[pygame.K_j]:
        changeVHSspeed(-100)
    if keys[pygame.K_k]:
        changeVHSspeed(100)

    #Physics/movement and such
    if (vhsModTimer <= 0):
        movement = vhsSpeed * dt
    else:
        movement = vhsSpeed * modVHSspeed * dt
        vhsModTimer -= dt

    for o in object.objects:
        o.position.x += movement

    for p in player.players:
        p.physicsUpdate(dt)
        if (p.isGrounded):
            p.position.x += movement

    for i in item.items:
        i.position.x += movement * 0.5

    vhsTapePos += movement
    vhsWheelRot -= movement

    changeVHSspeed(vhsSpeed + dt * 2)

    #Spawn items
    if (itemSpawnTimer > 0):
        itemSpawnTimer -= dt
    else:
        itemSpawnTimer = itemSpawnRate

        type = itemTypes[random.randint(0, itemTypes.__len__()-1)]
        if (movement > 0):
            newItem = type(pygame.Vector2(30, 280 + random.randrange(0, 40)))
        else:
            newItem = type(pygame.Vector2(600, 280 + random.randrange(0, 40)))

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

    pygame.draw.rect(screen, "white", pygame.Rect(250, 430, 150, 200)) #White pad

    for o in object.objects:
        pygame.draw.rect(screen, "green", pygame.Rect(o.position, o.size))

    for p in player.players:
        if (p.isFacingLeft):
            screen.blit(p.texture, pygame.Rect(p.position, p.size))
        else:
            screen.blit(pygame.transform.flip(p.texture, True, False), pygame.Rect(p.position, p.size))

    for i in item.items:
        screen.blit(i.image, i.position - pygame.Vector2(5, 5))

    blitRotateCenter(screen, wheelTexture, pygame.Vector2(450, 390), vhsWheelRot)
    blitRotateCenter(screen, wheelTexture, pygame.Vector2(50, 390), vhsWheelRot)

    screen.blit(wheelHighlightTexture, pygame.Vector2(450, 390))
    screen.blit(wheelHighlightTexture, pygame.Vector2(50, 390))

    #UI
    pygame.draw.rect(screen, "gray", pygame.Rect(15, 20, 35, 35))
    pygame.draw.rect(screen, "gray", pygame.Rect(600, 20, 35, 35))

    if (player1.item != None):
        screen.blit(player1.item.image, pygame.Vector2(20, 25))
    if (player2.item != None):
        screen.blit(player2.item.image, pygame.Vector2(605, 25))

    pygame.display.flip()

    dt = clock.tick(60) / 1000  # limits FPS and gives the delta time (dt)

pygame.quit()