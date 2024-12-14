import pygame
import sys
from settings import *
from player import Player
from tilemap import TileMap
from camera import Camera
from level_data import LEVEL_1, parse_level_data

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Platformer Template")
        self.clock = pygame.time.Clock()
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
        # Setup
        self.tilemap = TileMap(self)
        self.setup_level()
        
        # Calculate level dimensions
        level_width = len(LEVEL_1['main_layer'][0]) * TILE_SIZE
        level_height = len(LEVEL_1['main_layer']) * TILE_SIZE
        
        # Create camera with level dimensions
        self.camera = Camera(level_width, level_height)

    def setup_level(self):
        """
        Example level setup - modify this to load your own levels
        """
        # Load tileset
        self.tilemap.load_tileset(TILE_SET_PATH)
        
        # Create the level using the new level data format
        self.tilemap.load_map(LEVEL_1)
        
        # Create player instance
        player_spawn = self.tilemap.get_player_spawn()
        self.player = Player(
            pos=player_spawn,
            groups=[self.all_sprites, self.collision_sprites],
            collision_sprites=self.tilemap.solid_tiles,
            platform_sprites=self.tilemap.platform_tiles,
            ladder_sprites=self.tilemap.ladder_tiles,
            conveyor_sprites=self.tilemap.conveyor_tiles,
            portal_sprites=self.tilemap.portal_tiles
        )

    def run(self):
        while True:
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Delta time
            dt = self.clock.tick(FPS) / 1000
            
            # Update
            self.all_sprites.update(dt)
            self.camera.update(self.player)
            
            # Draw
            self.screen.fill(BLACK)
            
            # Draw all sprites with camera offset
            for sprite in self.tilemap.all_sprites:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
            
            # Display
            pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()
