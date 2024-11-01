import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Logic here

    screen.fill("purple")

    # RENDER GAME HERE

    pygame.display.flip()

    clock.tick(20)  # limits FPS to 60

pygame.quit()