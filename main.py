import pygame
import player

# pygame setup
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
running = True
dt = 0

#VHS stats
vhsSpeed = 100

player1 = player.Player(pygame.Vector2(screen.get_width()/2, screen.get_height()/2))

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

    for p in player.players:
        p.physicsUpdate(dt)
        if (p.isGrounded):
            p.position.x += vhsSpeed * dt
        

    # Render game here
    screen.fill("purple")

    pygame.draw.circle(screen, "red", player1.position, 10)

    pygame.display.flip()

    dt = clock.tick(60) / 1000  # limits FPS and gives the delta time (dt)

pygame.quit()