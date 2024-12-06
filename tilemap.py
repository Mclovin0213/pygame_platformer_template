import pygame
from settings import *
from tile_types import TileType, TILE_PROPERTIES
from level_data import parse_level_data
import random

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, tile_type, groups):
        super().__init__(groups)
        self.tile_type = tile_type
        self.properties = TILE_PROPERTIES[tile_type].copy()
        
        # Load the image
        if self.properties['image']:
            self.image = pygame.image.load(f"{TILE_SET_PATH}/{self.properties['image']}").convert_alpha()
        else:
            # Create an empty surface for invisible tiles
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10) if self.properties.get('solid', False) else pygame.Rect(0, 0, 0, 0)
        
        # Animation setup
        self.animation_frames = []
        self.current_frame = 0
        self.animation_time = 0
        if self.properties.get('animation_frames'):
            self.load_animation_frames()
    
    def load_animation_frames(self):
        """Load animation frames if specified in properties"""
        for frame_file in self.properties['animation_frames']:
            frame = pygame.image.load(f"{TILE_SET_PATH}/{frame_file}").convert_alpha()
            self.animation_frames.append(frame)
    
    def update(self, dt):
        """Update tile animation if it has one"""
        if self.animation_frames:
            self.animation_time += dt
            if self.animation_time >= ANIMATION_SPEED:
                self.animation_time = 0
                self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
                self.image = self.animation_frames[self.current_frame]

class TileMap:
    def __init__(self, game):
        self.game = game
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.solid_tiles = pygame.sprite.Group()
        self.platform_tiles = pygame.sprite.Group()
        self.ladder_tiles = pygame.sprite.Group()
        self.conveyor_tiles = pygame.sprite.Group()
        self.destructible_tiles = pygame.sprite.Group()
        self.hazard_tiles = pygame.sprite.Group()
        self.background_tiles = pygame.sprite.Group()
        
        self.tile_list = {}
        self.entity_list = {}
    
    def get_sprite_group(self, tile_type):
        """Returns appropriate sprite groups for the given tile type"""
        groups = [self.all_sprites]
        
        # Check if it's a background tile
        if TILE_PROPERTIES[tile_type].get('layer') == 'background':
            groups.append(self.background_tiles)
            return groups
            
        # Add to appropriate groups based on properties
        if TILE_PROPERTIES[tile_type].get('solid', False):
            groups.append(self.solid_tiles)
        if TILE_PROPERTIES[tile_type].get('platform', False):
            groups.append(self.platform_tiles)
        if TILE_PROPERTIES[tile_type].get('climbable', False):
            groups.append(self.ladder_tiles)
        if TILE_PROPERTIES[tile_type].get('speed', 0) != 0:
            groups.append(self.conveyor_tiles)
        if TILE_PROPERTIES[tile_type].get('destructible', False):
            groups.append(self.destructible_tiles)
        if TILE_PROPERTIES[tile_type].get('damage', 0) > 0:
            groups.append(self.hazard_tiles)
            
        return groups

    def load_tileset(self, path):
        """Load tileset images from a directory"""
        import os
        for tile_type in TileType:
            properties = TILE_PROPERTIES[tile_type]
            if properties.get('image'):
                image_path = os.path.join(path, properties['image'])
                if os.path.exists(image_path):
                    self.tile_list[tile_type] = pygame.image.load(image_path).convert_alpha()

    def create_tile(self, tile_type, pos):
        """Create a tile of the specified type at the given position"""
        if tile_type == TileType.EMPTY:
            return None
            
        sprite_groups = self.get_sprite_group(tile_type)
        return Tile(pos, tile_type, sprite_groups)

    def load_map(self, level_data):
        """Create a level from the level data dictionary"""
        main_layer, entities, background = parse_level_data(level_data)
        
        # Create background tiles
        for row_index, row in enumerate(background):
            for col_index, tile_type in enumerate(row):
                if tile_type != TileType.EMPTY:
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    self.create_tile(tile_type, (x, y))
        
        # Create main layer tiles
        for row_index, row in enumerate(main_layer):
            for col_index, tile_type in enumerate(row):
                if tile_type != TileType.EMPTY:
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    self.create_tile(tile_type, (x, y))
        
        # Create entities (to be implemented)
        self.entity_list = entities
        self.spawn_entities(entities)
    
    def spawn_entities(self, entities):
        """Spawn entities defined in the level data"""
        for entity_data in entities:
            x, y = entity_data['position']
            x *= TILE_SIZE
            y *= TILE_SIZE
            
            if entity_data['type'] == 'enemy':
                # Enemy creation would go here
                pass
            elif entity_data['type'] == 'powerup':
                # Powerup creation would go here
                pass
            elif entity_data['type'] == 'checkpoint':
                # Checkpoint creation would go here
                pass
    
    def get_player_spawn(self):
        """Find the player spawn position in the level"""
        # Default spawn position
        default_spawn = (TILE_SIZE * 2, TILE_SIZE * 2)
        
        # Look for a specific spawn point in entities
        for entity in self.entity_list:
            if entity.get('type') == 'player_spawn':
                x, y = entity['position']
                return (x * TILE_SIZE, y * TILE_SIZE)
        
        # If no spawn point found, return default
        return default_spawn

    def update(self, dt):
        """Update all tiles (for animations, etc.)"""
        for sprite in self.all_sprites:
            if hasattr(sprite, 'update'):
                sprite.update(dt)
