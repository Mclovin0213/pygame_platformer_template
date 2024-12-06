from enum import Enum

class TileType(Enum):
    """Enum for different tile types"""
    EMPTY = 0
    SOLID = 1
    PLATFORM = 2
    LADDER = 3
    CONVEYOR_LEFT = 4
    CONVEYOR_RIGHT = 5
    DESTRUCTIBLE = 6
    SPIKE = 7
    POWERUP_SPAWN = 8
    ENEMY_SPAWN = 9
    CHECKPOINT = 10
    FINISH = 11
    BACKGROUND = 12

# Define properties for each tile type
TILE_PROPERTIES = {
    TileType.EMPTY: {
        'solid': False,
        'damage': 0,
        'image': None,
        'animation_frames': [],
    },
    TileType.SOLID: {
        'solid': True,
        'damage': 0,
        'image': '1.png',
        'animation_frames': [],
    },
    TileType.PLATFORM: {
        'solid': True,
        'damage': 0,
        'image': '2.png',
        'animation_frames': [],
        'platform': True,  # Can jump through from below
    },
    TileType.LADDER: {
        'solid': False,
        'climbable': True,
        'image': '3.png',
        'animation_frames': [],
    },
    TileType.CONVEYOR_LEFT: {
        'solid': True,
        'speed': -2,
        'image': '4.png',
        'animation_frames': ['conveyor_1.png', 'conveyor_2.png', 'conveyor_3.png'],
    },
    TileType.CONVEYOR_RIGHT: {
        'solid': True,
        'speed': 2,
        'image': '5.png',
        'animation_frames': ['conveyor_1.png', 'conveyor_2.png', 'conveyor_3.png'],
    },
    TileType.DESTRUCTIBLE: {
        'solid': True,
        'health': 1,
        'image': '6.png',
        'animation_frames': [],
        'break_effect': 'break_particles',
    },
    TileType.SPIKE: {
        'solid': False,
        'damage': 1,
        'image': '7.png',
        'animation_frames': [],
    },
    TileType.POWERUP_SPAWN: {
        'solid': False,
        'powerup_type': None,  # Set when creating level
        'image': None,  # Invisible spawn point
        'animation_frames': [],
    },
    TileType.ENEMY_SPAWN: {
        'solid': False,
        'enemy_type': None,  # Set when creating level
        'image': None,  # Invisible spawn point
        'animation_frames': [],
    },
    TileType.CHECKPOINT: {
        'solid': False,
        'image': '10.png',
        'animation_frames': ['checkpoint_1.png', 'checkpoint_2.png'],
        'activated': False,
    },
    TileType.FINISH: {
        'solid': False,
        'image': '11.png',
        'animation_frames': ['finish_1.png', 'finish_2.png'],
    },
    TileType.BACKGROUND: {
        'solid': False,
        'damage': 0,
        'image': 'background.png',
        'animation_frames': [],
        'layer': 'background'
    },
}
