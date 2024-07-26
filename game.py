import pygame

pygame.init()

screen = pygame.display.set_mode((960, 640))

screen.fill((0,0,0))


clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.flip()
    clock.tick(60)