"""
Level data format using a more flexible dictionary structure that allows for:
- Multiple layers (background, main, foreground)
- Entity placement with properties
- Tile properties and variations
"""

from tile_types import TileType

# Example of a level with multiple layers and entity placement
LEVEL_1 = {
    'name': 'Level 1',
    'background_color': (50, 50, 100),
    'background_tiles': [
        "                                                  ",
        "     BBB        BBB          BBB        BBB      ",
        "   BBBBBBB    BBBBBBB    BBBBBBB     BBBBBBB    ",
        # ... more background tiles
    ],
    
    'main_layer': [
        "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "10000000000000000000000L000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000P0000000000000000L000000000000000000F00000000000000000000000000000000000000000000000000001",
        "10000000022200000000000L000022200000000000000000000000000000000000000000000000000000000000000001",
        "10000000000000000000000L000000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000022222220000000000000000000000000000000000000000000000000000000000000000000001",
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "100D00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001",
        "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
    ],
    
    'entities': [
        {
            'type': 'enemy',
            'enemy_type': 'walker',
            'position': (10, 5),
            'properties': {
                'patrol_distance': 4,
                'speed': 2
            }
        },
        {
            'type': 'powerup',
            'powerup_type': 'jump_boost',
            'position': (15, 3),
            'properties': {
                'duration': 10,
                'strength': 1.5
            }
        },
        {
            'type': 'checkpoint',
            'position': (25, 5)
        }
    ],
    
    # Define what each character in the level string means
    'tile_mapping': {
        ' ': TileType.EMPTY,
        '1': TileType.SOLID,
        '2': TileType.PLATFORM,
        'L': TileType.LADDER,
        'C': TileType.CONVEYOR_RIGHT,
        'D': TileType.DESTRUCTIBLE,
        'S': TileType.SPIKE,
        'P': TileType.POWERUP_SPAWN,
        'E': TileType.ENEMY_SPAWN,
        'K': TileType.CHECKPOINT,
        'F': TileType.FINISH,
        'B': 'background_block'  # Special case for background tiles
    },
    
    # Optional tile variations for visual diversity
    'tile_variations': {
        TileType.SOLID: {
            'variations': ['1.png', '1_var1.png', '1_var2.png'],
            'rules': {
                'top_edge': '1_top.png',
                'bottom_edge': '1_bottom.png',
                'left_edge': '1_left.png',
                'right_edge': '1_right.png'
            }
        }
    }
}

def parse_level_data(level_data):
    """
    Converts the level dictionary into a format the game can use
    Returns: tuple of (main_layer_tiles, entities, background_tiles)
    """
    # Character to TileType mapping
    char_to_tile = {
        '0': TileType.EMPTY,
        '1': TileType.SOLID,
        '2': TileType.PLATFORM,
        'L': TileType.LADDER,
        'C': TileType.CONVEYOR_RIGHT,
        'c': TileType.CONVEYOR_LEFT,
        'D': TileType.DESTRUCTIBLE,
        'S': TileType.SPIKE,
        'P': TileType.POWERUP_SPAWN,
        'E': TileType.ENEMY_SPAWN,
        'K': TileType.CHECKPOINT,
        'F': TileType.FINISH,
        'B': TileType.BACKGROUND,
        ' ': TileType.EMPTY
    }
    
    # Parse main layer
    main_layer = []
    for row in level_data['main_layer']:
        tile_row = []
        for char in row:
            tile_type = char_to_tile.get(char, TileType.EMPTY)
            tile_row.append(tile_type)
        main_layer.append(tile_row)
    
    # Parse background layer if it exists
    background = []
    if 'background_tiles' in level_data:
        for row in level_data['background_tiles']:
            tile_row = []
            for char in row:
                tile_type = char_to_tile.get(char, TileType.EMPTY)
                tile_row.append(tile_type)
            background.append(tile_row)
    
    # Parse entities
    entities = level_data.get('entities', [])
    
    return main_layer, entities, background
