import pygame
import os
from settings import *
from tile_types import TileType, TILE_PROPERTIES

def create_dummy_sprite(width, height, color, filename):
    """Create a simple rectangular sprite with the given dimensions and color"""
    surface = pygame.Surface((width, height))
    surface.fill(color)
    # Add a border to make it more visible
    pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), 2)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    pygame.image.save(surface, filename)

def main():
    pygame.init()
    
    # Create player animation sprites
    player_states = ['idle', 'run', 'jump']
    player_colors = {
        'idle': (0, 255, 0),    # Green
        'run': (255, 165, 0),   # Orange
        'jump': (255, 0, 0)     # Red
    }
    
    # Create player sprites for each state
    for state in player_states:
        state_dir = os.path.join('assets', 'player', state)
        os.makedirs(state_dir, exist_ok=True)
        
        # Create 4 frames for each state
        for i in range(4):
            filename = os.path.join(state_dir, f'{i+1}.png')
            create_dummy_sprite(TILE_SIZE, TILE_SIZE, player_colors[state], filename)
    
    # Create tile sprites based on TileType enum
    tiles_dir = os.path.join('assets', 'tiles')
    os.makedirs(tiles_dir, exist_ok=True)
    
    # Colors for different tile types
    tile_colors = {
        TileType.SOLID: (100, 100, 100),          # Gray
        TileType.PLATFORM: (139, 69, 19),         # Brown
        TileType.LADDER: (218, 165, 32),          # Goldenrod
        TileType.CONVEYOR_LEFT: (70, 130, 180),   # Steel Blue
        TileType.CONVEYOR_RIGHT: (70, 130, 180),  # Steel Blue
        TileType.DESTRUCTIBLE: (205, 92, 92),     # Indian Red
        TileType.SPIKE: (220, 20, 60),            # Crimson
        TileType.CHECKPOINT: (60, 179, 113),      # Medium Sea Green
        TileType.FINISH: (147, 112, 219),         # Medium Purple
        TileType.BACKGROUND: (40, 40, 80),        # Dark Blue-Gray
    }
    
    # Create sprites for each tile type that needs an image
    for tile_type in TileType:
        if tile_type == TileType.EMPTY:
            continue
            
        properties = TILE_PROPERTIES[tile_type]
        if properties.get('image'):
            color = tile_colors.get(tile_type, (200, 200, 200))
            filename = os.path.join(tiles_dir, properties['image'])
            create_dummy_sprite(TILE_SIZE, TILE_SIZE, color, filename)
            
            # Create animation frames if specified
            if properties.get('animation_frames'):
                for frame_file in properties['animation_frames']:
                    filename = os.path.join(tiles_dir, frame_file)
                    create_dummy_sprite(TILE_SIZE, TILE_SIZE, color, filename)

if __name__ == '__main__':
    main()
    print("Dummy sprites generated successfully!")
