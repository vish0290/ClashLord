import pygame
import pytmx
from code.settings import *
from code.frames import *


class Game(object):
    def __init__(self):
        self.currentLevelNumber = 0
        self.levels = []
        self.levels.append(Level(fileName="graphics/maps/level1.tmx"))
        self.currentLevel = self.levels[self.currentLevelNumber]
        self.player = Player(x=200, y=100)
        self.player.currentLevel = self.currentLevel

    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.goLeft()
                elif event.key == pygame.K_RIGHT:
                    self.player.goRight()
                elif event.key == pygame.K_UP:
                    self.player.jump()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.changeX < 0:
                    self.player.stop()
                elif event.key == pygame.K_RIGHT and self.player.changeX > 0:
                    self.player.stop()

        return False

    def runLogic(self):
        self.player.update()

    def draw(self, screen):
        screen.fill(background)
        self.currentLevel.draw(screen)
        self.player.draw(screen)
        pygame.display.flip()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Load the spritesheet of frames for this player
        self.idleRight = player_idle_right()
        self.idleLeft = player_idle_left()
        self.runRight = player_walk_right()
        self.runLeft = player_walk_left()
        self.jumpingRight = player_jump_right()
        self.jumpingLeft = player_jump_left()
        self.image = self.idleRight[0]

        # Set player position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Set speed and direction
        self.changeX = 0
        self.changeY = 0
        self.direction = "right"

        # Boolean to check if player is running, current running frame, and time since last frame change
        self.running = False
        self.runningFrame = 0
        self.runningTime = pygame.time.get_ticks()

        # Player's current level, set after object initialized in game constructor
        self.currentLevel = None

    def on_ground(self):
        self.rect.y += 2
        tileHitList = pygame.sprite.spritecollide(
            self, self.currentLevel.layers[map_ground_layer].tiles, False
        )
        self.rect.y -= 2
        return tileHitList

    def applyGravity(self):
        self.changeY += 0.5  # Gravity is always applied
        tileHitList = self.on_ground()  # Define tileHitList variable
        if tileHitList:
            print(f"Player y: {self.rect.y}, tile y: {tileHitList}")

            # self.rect.bottom = tileHitList[0].rect.top  # Correct player position on the ground
            self.changeY = 0

    def jump(self):
        if self.on_ground():
            self.changeY = -10
            if self.direction == "right":
                self.image = self.jumpingRight[1]
            else:
                self.image = self.jumpingLeft[1]

    def goRight(self):
        self.direction = "right"
        self.running = True
        self.changeX = 3

    def goLeft(self):
        self.direction = "left"
        self.running = True
        self.changeX = -3

    def stop(self):
        self.running = False
        self.changeX = 0

    def update(self):
        self.rect.x += self.changeX
        self.rect.y += self.changeY
        self.applyGravity()

        if self.rect.right >= screen_width - 200:
            difference = self.rect.right - (screen_width - 200)
            self.rect.right = screen_width - 200
            self.currentLevel.shiftLevel(-difference)
        elif self.rect.left <= 200:
            difference = 200 - self.rect.left
            self.rect.left = 200
            self.currentLevel.shiftLevel(difference)

        if self.running:
            if self.direction == "right":
                self.image = self.runRight[self.runningFrame]
            else:
                self.image = self.runLeft[self.runningFrame]
        else:
            if self.direction == "right":
                self.image = self.idleRight[self.runningFrame]
            else:
                self.image = self.idleLeft[self.runningFrame]

        if pygame.time.get_ticks() - self.runningTime > 50:
            self.runningTime = pygame.time.get_ticks()
            if self.runningFrame == 4:
                self.runningFrame = 0
            else:
                self.runningFrame += 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Level(object):
    def __init__(self, fileName):
        self.mapObject = pytmx.load_pygame(fileName)
        self.layers = []
        self.levelShift = 0
        for layer in range(len(self.mapObject.layers)):
            self.layers.append(Layer(index=layer, mapObject=self.mapObject))

    def shiftLevel(self, shiftX):
        self.levelShift += shiftX
        for layer in self.layers:
            for tile in layer.tiles:
                tile.rect.x += shiftX

    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)


class Layer(object):
    def __init__(self, index, mapObject):
        self.index = index
        self.tiles = pygame.sprite.Group()
        self.mapObject = mapObject
        for x in range(self.mapObject.width):
            for y in range(self.mapObject.height):
                img = self.mapObject.get_tile_image(x, y, self.index)
                if img:
                    self.tiles.add(
                        Tile(
                            image=img,
                            x=(x * self.mapObject.tilewidth),
                            y=(y * self.mapObject.tileheight),
                        )
                    )

    def draw(self, screen):
        self.tiles.draw(screen)


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
