import pygame
from settings import *
from tile_types import TileType, TILE_PROPERTIES
from level_data import parse_level_data
from player import Player
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
        # Create hitbox for any tile that needs collision detection
        self.hitbox = self.rect.inflate(0, -10) if self.properties.get('has_hitbox', False) else pygame.Rect(0, 0, 0, 0)
        
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

class Portal(Tile):
    def __init__(self, pos, tile_type, groups):
        super().__init__(pos, tile_type, groups)
        self.last_used = 0  # Timestamp of last portal use
        self.linked_portal = None  # Will be set by TileMap
        
    def can_use(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_used >= self.properties['cooldown']
        
    def teleport(self, player):
        if self.can_use() and self.linked_portal:
            current_time = pygame.time.get_ticks()
            # Update cooldown for both portals
            self.last_used = current_time
            self.linked_portal.last_used = current_time
            # Teleport player to linked portal
            player.rect.centerx = self.linked_portal.rect.centerx
            player.rect.bottom = self.linked_portal.rect.bottom
            player.hitbox.centerx = player.rect.centerx
            player.hitbox.bottom = player.rect.bottom
            return True
        return False

class Pickup(Tile):
    def __init__(self, pos, tile_type, groups):
        super().__init__(pos, tile_type, groups)
        self.value = self.properties.get('value', 1)
        self.pickup_type = self.properties.get('pickup_type', 'coin')
        self.collected = False

    def collect(self, player):
        """Handle pickup collection based on type"""
        if not self.collected:
            self.collected = True
            if self.pickup_type == 'coin':
                player.coins += self.value
            elif self.pickup_type == 'oneup':
                player.lives += self.value
            self.kill()  # Remove the pickup from all sprite groups

class TileMap:
    def __init__(self, game):
        self.game = game
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.solid_tiles = pygame.sprite.Group()
        self.platform_tiles = pygame.sprite.Group()
        self.ladder_tiles = pygame.sprite.Group()
        self.checkpoint_tiles = pygame.sprite.Group()
        self.conveyor_tiles = pygame.sprite.Group()
        self.destructible_tiles = pygame.sprite.Group()
        self.hazard_tiles = pygame.sprite.Group()
        self.background_tiles = pygame.sprite.Group()
        self.portal_tiles = pygame.sprite.Group()
        self.pickup_tiles = pygame.sprite.Group()
        self.portals = {'1': [], '2': []}
        
        self.tile_list = {}
        self.entity_list = {}
        self.player_spawn = None  # Store player spawn position
    
    def get_sprite_group(self, tile_type):
        """Get the appropriate sprite group(s) for a tile type"""
        groups = [self.all_sprites]
        
        if tile_type == TileType.SOLID:
            groups.append(self.solid_tiles)
        elif tile_type == TileType.PLATFORM:
            groups.append(self.platform_tiles)
        elif tile_type == TileType.LADDER:
            groups.append(self.ladder_tiles)
        elif tile_type == TileType.CHECKPOINT:
            groups.append(self.checkpoint_tiles)
        elif tile_type in [TileType.CONVEYOR_LEFT, TileType.CONVEYOR_RIGHT]:
            groups.append(self.conveyor_tiles)
        elif tile_type == TileType.DESTRUCTIBLE:
            groups.append(self.destructible_tiles)
        elif tile_type == TileType.SPIKE:
            groups.append(self.hazard_tiles)
        elif tile_type == TileType.BACKGROUND:
            groups.append(self.background_tiles)
        elif tile_type in [TileType.PORTAL_SET_1, TileType.PORTAL_SET_2]:
            groups.append(self.portal_tiles)
        elif tile_type in [TileType.PICKUP_COIN, TileType.PICKUP_ONEUP]:
            groups.append(self.pickup_tiles)
            
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
        groups = self.get_sprite_group(tile_type)
        
        if tile_type in [TileType.PORTAL_SET_1, TileType.PORTAL_SET_2]:
            portal = Portal(pos, tile_type, groups)
            portal_type = str(TILE_PROPERTIES[tile_type]['portal_type'])
            self.portals[portal_type].append(portal)
            # Link portals if we have a pair
            if len(self.portals[portal_type]) == 2:
                self.portals[portal_type][0].linked_portal = self.portals[portal_type][1]
                self.portals[portal_type][1].linked_portal = self.portals[portal_type][0]
            return portal
        elif tile_type in [TileType.PICKUP_COIN, TileType.PICKUP_ONEUP]:
            return Pickup(pos, tile_type, groups)
        else:
            return Tile(pos, tile_type, groups)

    def load_map(self, level_data):
        """Create a level from the level data dictionary"""
        # Clear existing tiles and entities
        self.all_sprites.empty()
        self.solid_tiles.empty()
        self.platform_tiles.empty()
        self.ladder_tiles.empty()
        self.checkpoint_tiles.empty()
        self.conveyor_tiles.empty()
        self.destructible_tiles.empty()
        self.hazard_tiles.empty()
        self.background_tiles.empty()
        self.portal_tiles.empty()
        self.pickup_tiles.empty()
        self.entity_list.clear()  # Clear the dictionary
        
        # Parse level data
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
        
        # Create entities
        self.spawn_entities(entities)
    
    def spawn_entities(self, entities):
        """Spawn entities defined in the level data"""
        for entity_data in entities:
            entity_type = entity_data['type']
            pos = entity_data['position']
            x, y = pos
            x *= TILE_SIZE
            y *= TILE_SIZE
            
            if entity_type == 'player_spawn':
                self.player_spawn = (x, y)  # Just store the position
            elif entity_type == 'enemy':
                # Enemy creation would go here
                pass
            elif entity_type == 'powerup':
                # Powerup creation would go here
                pass
            elif entity_type == 'checkpoint':
                # Checkpoint creation would go here
                pass
    
    def get_player_spawn(self):
        """Find the player spawn position in the level"""
        if self.player_spawn:
            return self.player_spawn
        # Default spawn if none specified
        return (TILE_SIZE * 2, TILE_SIZE * 2)

    def check_portal_interaction(self, player):
        # Check if player is pressing up key
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_UP]:
            return
            
        # Check collision with any portal
        for portal_set in self.portals.values():
            for portal in portal_set:
                if player.hitbox.colliderect(portal.hitbox):
                    portal.teleport(player)
                    return

    def check_pickup_collision(self, player):
        """Check for collision between player and pickups"""
        for pickup in self.pickup_tiles:
            if player.hitbox.colliderect(pickup.hitbox):
                pickup.collect(player)

    def update(self, dt):
        """Update all tiles (for animations, etc.)"""
        for sprite in self.all_sprites:
            if hasattr(sprite, 'update'):
                sprite.update(dt)
