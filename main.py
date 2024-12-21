import pygame
import sys
from settings import *
from player import Player
from tilemap import TileMap
from camera import Camera
from tile_types import TILE_PROPERTIES
from level_data import LEVEL_1, parse_level_data

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Platformer Template")
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.Font(None, 36)
        self.game_over = False
        
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
                if event.type == pygame.KEYDOWN and self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
            
            # Delta time
            dt = self.clock.tick(FPS) / 1000
            
            if not self.game_over:
            
                # Update
                self.all_sprites.update(dt)
                self.camera.update(self.player)
            
                # Draw
                self.screen.fill(BLACK)
                
                # Check for hazard collisions
                hazard_hits = pygame.sprite.spritecollide(self.player, self.tilemap.hazard_tiles, False)
                for hazard in hazard_hits:
                    tile_type = hazard.tile_type
                    damage = TILE_PROPERTIES[tile_type]['damage']
                    if self.player.take_damage(damage):  # Player died
                        if self.player.lives <= 0:
                            self.game_over = True
            
                # Draw all sprites with camera offset
                for sprite in self.tilemap.all_sprites:
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
                for sprite in self.all_sprites:
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
                    
                self.draw_hud()
            else:
                self.draw_game_over()        
            
            # Display
            pygame.display.flip()
            
    def draw_hud(self):
        # Draw lives
        lives_text = self.font.render(f'Lives: {self.player.lives}', True, (255, 255, 255))
        self.screen.blit(lives_text, (10, 10))
        
        # Draw health
        health_text = self.font.render(f'Health: {self.player.health}', True, (255, 255, 255))
        self.screen.blit(health_text, (10, 50))
        
        # Draw coins
        coins_text = self.font.render(f'Coins: {self.player.coins}', True, (255, 255, 255))
        self.screen.blit(coins_text, (10, 90))
    
    def draw_game_over(self):
        game_over_text = self.font.render('Game Over! Press R to restart', True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.screen.blit(game_over_text, text_rect)
    
    def reset_game(self):
        # Reset game state
        self.game_over = False
        
        # Clear all sprites
        self.all_sprites.empty()
        self.collision_sprites.empty()
        
        # Reload the level
        self.setup_level()

if __name__ == '__main__':
    game = Game()
    game.run()
