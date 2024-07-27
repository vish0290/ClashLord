import pygame
import pytmx


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, layers):
        super().__init__()
        self.image = pygame.Surface((32, 48))  # Replace with your player image
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.layers = layers  # The ground layer from your tiled map

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_SPACE] and self.on_ground():
            self.velocity_y = self.jump_strength
        print(
            f"keys: {keys[pygame.K_LEFT]}, {keys[pygame.K_RIGHT]}, {keys[pygame.K_SPACE]}, on_ground: {self.on_ground()}, velocity_y: {self.velocity_y}"
        )

    def apply_gravity(self):
        if not self.on_ground():
            self.velocity_y += self.gravity
        else:
            self.velocity_y = 0

    def on_ground(self):
        self.rect.y += 1  # Move the rect down a bit to check for collision
        on_ground = pygame.sprite.spritecollideany(self, self.layers["ground"])
        self.rect.y -= 1  # Move the rect back to its original position
        return on_ground

    def update(self):
        self.handle_input()
        self.rect.y += self.velocity_y
        self.apply_gravity()

        # Check for collisions with the ground
        if self.on_ground():
            self.velocity_y = 0
            # Move player up to align with the ground tile
            collided_tile = pygame.sprite.spritecollideany(self, self.layers["ground"])
            if collided_tile:
                self.rect.bottom = collided_tile.rect.top

        # Prevent player from moving off the screen
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())


class GroundTile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))


def load_map(filename, ground_layer_name="ground"):
    tmx_data = pytmx.load_pygame(filename, pixelalpha=True)
    ground_layer = pygame.sprite.Group()

    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer) and layer.name == ground_layer_name:
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    tile_x = x * tmx_data.tilewidth
                    tile_y = y * tmx_data.tileheight
                    ground_tile = GroundTile(tile, tile_x, tile_y)
                    ground_layer.add(ground_tile)

    return ground_layer


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((960, 640))

# Load the map and extract the ground layer
ground_layer = load_map(
    "../graphics/maps/level1.tmx", "ground"
)  # Specify the ground layer name

# Create the player and add to the sprite group
player = Player(100, 100, ground_layer)  # Ensure this position is within the map bounds
all_sprites = pygame.sprite.Group(player)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    screen.fill((0, 0, 0))
    ground_layer.draw(screen)
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
