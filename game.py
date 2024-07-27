import pygame
from code.game_attr import Game
from code.settings import *


def main():
    pygame.init()
    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption(screen_title)
    clock = pygame.time.Clock()
    done = False
    game = Game()

    while not done:
        done = game.processEvents()
        game.runLogic()
        game.draw(screen)
        clock.tick(60)

    pygame.quit()


main()
