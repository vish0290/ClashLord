import pygame


class SpriteSheet(object):
    def __init__(self, fileName):
        self.sheet = pygame.image.load(fileName)

    def image_at(self, rectangle, flip):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if flip:
            image = pygame.transform.flip(image, True, False)
        return image


def player_idle_right() -> tuple:
    sprites = SpriteSheet("graphics/Sprites/01-King Human/Idle (78x58).png")
    frames = []
    for i in range(0, 11):
        frames.append(sprites.image_at((i * 78, 0, 78, 58), False))

    return tuple(frames)


def player_idle_left() -> tuple:
    sprites = SpriteSheet("graphics/Sprites/01-King Human/Idle (78x58).png")
    frames = []
    for i in range(0, 11):
        frames.append(sprites.image_at((i * 78, 0, 78, 58), True))
    return tuple(frames)


def player_walk_right() -> tuple:
    sprites = SpriteSheet("graphics/Sprites/01-King Human/Run (78x58).png")
    frames = []
    for i in range(0, 11):
        frames.append(sprites.image_at((i * 78, 0, 78, 58), False))
    return tuple(frames)


def player_walk_left() -> tuple:
    sprites = SpriteSheet("graphics/Sprites/01-King Human/Run (78x58).png")
    frames = []
    for i in range(0, 11):
        frames.append(sprites.image_at((i * 78, 0, 78, 58), True))

    return tuple(frames)


def player_jump_right() -> tuple:
    sprites_1 = SpriteSheet("graphics/Sprites/01-King Human/Run (78x58).png")
    sprites_2 = SpriteSheet("graphics/Sprites/01-King Human/Jump (78x58).png")
    sprites_3 = SpriteSheet("graphics/Sprites/01-King Human/Fall (78x58).png")
    frames = (
        sprites_1.image_at((0, 0, 78, 58), False),
        sprites_2.image_at((0, 0, 78, 58), False),
        sprites_3.image_at((0, 0, 78, 58), False),
        sprites_1.image_at((0, 0, 78, 58), False),
    )
    return frames


def player_jump_left() -> tuple:
    sprites_1 = SpriteSheet("graphics/Sprites/01-King Human/Run (78x58).png")
    sprites_2 = SpriteSheet("graphics/Sprites/01-King Human/Jump (78x58).png")
    sprites_3 = SpriteSheet("graphics/Sprites/01-King Human/Fall (78x58).png")
    frames = (
        sprites_1.image_at((0, 0, 78, 58), True),
        sprites_2.image_at((0, 0, 78, 58), True),
        sprites_3.image_at((0, 0, 78, 58), True),
        sprites_1.image_at((0, 0, 78, 58), True),
    )
    return frames
