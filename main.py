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
pygame.display.set_caption("Tape jumpers")
clock = pygame.time.Clock()
dt = 0
font = pygame.font.SysFont('Arial', 50)

#Music
pygame.mixer.music.load(os.path.join("gameJamSong1.mp3"))
pygame.mixer.music.play(-1)

newStart = True

while (newStart):
    newStart = False
    running = True

    item.items.clear()
    object.objects.clear()
    player.players.clear()

    #Match result
    resultTxt = None

    #Items
    itemTypes = [item_reverse.Reverse, item_fastForward.FastForward, item_pause.Pause]
    itemSpawnTimer = 0
    itemSpawnRate = 6

    #Parkour sections
    parkourSet = [  [pygame.Rect(-90, 370, 20, 30), pygame.Rect(-130, 330, 20, 70), pygame.Rect(-170, 360, 20, 40)],
                    [pygame.Rect(-110, 370, 40, 30), pygame.Rect(-30, 340, 40, 10), pygame.Rect(-130, 300, 20, 100)],
                    [pygame.Rect(-40, 380, 30, 20), pygame.Rect(-80, 350, 20, 50), pygame.Rect(-90, 380, 10, 20), pygame.Rect(-20, 310, 30, 10), pygame.Rect(-140, 280, 20, 120), pygame.Rect(-230, 300, 20, 100), pygame.Rect(-200, 370, 10, 30), pygame.Rect(-150, 330, 20, 10)]]
    parkourSpawnTimer = 0

    #VHS stats
    vhsSpeed = 20
    modVHSspeed = 0
    vhsModTimer = 0
    vhsTapePos = 0
    vhsWheelRot = 0

    player1 = player.Player(pygame.Vector2(screen.get_width()/2, screen.get_height()/2), pygame.image.load(os.path.join("textures", "neo standing.png")), pygame.image.load(os.path.join("textures", "neo left.png")), pygame.image.load(os.path.join("textures", "neo left up.png")))
    player2 = player.Player(pygame.Vector2(screen.get_width()/2, screen.get_height()/2), pygame.image.load(os.path.join("textures", "lara croft.png")), pygame.image.load(os.path.join("textures", "lara croft left.png")), pygame.image.load(os.path.join("textures", "lara croft left up.png")))

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

        if (keys[pygame.K_r]):
            running = False
            newStart = True
        elif (keys[pygame.K_ESCAPE]):
            running = False

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

        #Check deaths
        if (resultTxt == None):
            if (player1.isDead and player2.isDead):
                resultTxt = "Tie!"
            elif (player1.isDead):
                resultTxt = "Fala Froft won!"
            elif(player2.isDead):
                resultTxt = "Eno won!"

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

        #Spawn parkour
        if (parkourSpawnTimer > 0):
            if (vhsModTimer > 0):
                parkourSpawnTimer -= vhsSpeed * modVHSspeed * dt
            else:
                parkourSpawnTimer -= vhsSpeed * dt
        else:
            parkourBlocks = parkourSet[random.randint(0, parkourSet.__len__()-1)]
            for r in parkourBlocks:
                newBlock = object.Object(pygame.Vector2(r.x, r.y), pygame.Vector2(r.width, r.height), vhsSpeed)
            parkourSpawnTimer = 320

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

        if (resultTxt != None):
            screen.blit(font.render(resultTxt, False, (0,0,0)), (250,150))

        pygame.display.flip()

        dt = clock.tick(60) / 1000  # limits FPS and gives the delta time (dt)

pygame.quit()