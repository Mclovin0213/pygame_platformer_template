import pygame
import sys
from settings import *
from player import Player
from tilemap import TileMap
from camera import Camera
from tile_types import TILE_PROPERTIES
from level_data import LEVEL_1, parse_level_data
from enemy import Enemy, EnemyType
import os

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        color = BUTTON_HOVER if self.is_hovered else BUTTON_NORMAL
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Platformer Template")
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.Font(None, 36)
        self.game_over = False
        self.game_state = "title"  # Can be "title" or "game"
        
        # Title screen setup
        title_bg_path = os.path.join('assets', 'menu', 'title_bg.png')
        self.title_bg = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.title_bg.fill(BLACK)  # Default background if image not found
        
        try:
            if os.path.exists(title_bg_path):
                self.title_bg = pygame.image.load(title_bg_path)
                self.title_bg = pygame.transform.scale(self.title_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except:
            print("Title background image not found, using default background")
        
        # Create buttons
        center_x = WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2
        start_y = WINDOW_HEIGHT // 2
        self.start_button = Button(center_x, start_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Start Game")
        self.quit_button = Button(center_x, start_y + BUTTON_HEIGHT + BUTTON_PADDING, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit")
        
        # Game setup
        self.setup_game()
    
    def setup_game(self):
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()  # New group for enemies
        
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
        
        # Create enemies from level data
        for entity in LEVEL_1['entities']:
            if entity['type'] == 'enemy':
                pos = (entity['position'][0] * TILE_SIZE, entity['position'][1] * TILE_SIZE)
                enemy_type = EnemyType(entity.get('enemy_type', 'walker'))  # Default to walker if not specified
                Enemy(
                    pos=pos,
                    enemy_type=enemy_type,
                    groups=[self.all_sprites, self.enemy_sprites],
                    collision_sprites=self.tilemap.solid_tiles
                )
        
        # Create player instance
        player_spawn = self.tilemap.get_player_spawn()
        self.player = Player(
            pos=player_spawn,
            groups=[self.all_sprites],
            collision_sprites=self.tilemap.solid_tiles,
            platform_sprites=self.tilemap.platform_tiles,
            ladder_sprites=self.tilemap.ladder_tiles,
            conveyor_sprites=self.tilemap.conveyor_tiles,
            portal_sprites=self.tilemap.portal_tiles,
            checkpoint_tiles=self.tilemap.checkpoint_tiles,
            pickup_sprites=self.tilemap.pickup_tiles  # Add pickup sprites
        )

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.game_state == "title":
                    if self.start_button.handle_event(event):
                        self.game_state = "game"
                    if self.quit_button.handle_event(event):
                        pygame.quit()
                        sys.exit()
                
                elif self.game_state == "game":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.game_state = "title"
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN and self.game_over:
                            if event.key == pygame.K_r:
                                self.reset_game()
            
            self.screen.fill(BLACK)
            
            if self.game_state == "title":
                self.screen.blit(self.title_bg, (0, 0))
                self.start_button.draw(self.screen)
                self.quit_button.draw(self.screen)
            
            elif self.game_state == "game":
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
                    
                    # Check for enemy collisions
                    enemy_hits = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False)
                    for enemy in enemy_hits:
                        if self.player.take_damage(enemy.damage):  # Player died
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
        self.enemy_sprites.empty()
        
        # Reload the level
        self.setup_level()

if __name__ == '__main__':
    game = Game()
    game.run()
