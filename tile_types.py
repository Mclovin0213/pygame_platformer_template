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
    PORTAL_SET_1 = 13
    PORTAL_SET_2 = 14
    PICKUP_COIN = 15
    PICKUP_ONEUP = 16

# Define properties for each tile type
TILE_PROPERTIES = {
    TileType.EMPTY: {
        'solid': False,
        'has_hitbox': False,
        'damage': 0,
        'image': None,
        'animation_frames': [],
    },
    TileType.SOLID: {
        'solid': True,
        'has_hitbox': True,
        'damage': 0,
        'image': '1.png',
        'animation_frames': [],
    },
    TileType.PLATFORM: {
        'solid': True,
        'has_hitbox': True,
        'damage': 0,
        'image': '2.png',
        'animation_frames': [],
        'platform': True,  # Can jump through from below
    },
    TileType.LADDER: {
        'solid': False,
        'has_hitbox': True,
        'climbable': True,
        'image': '3.png',
        'animation_frames': [],
    },
    TileType.CONVEYOR_LEFT: {
        'solid': True,
        'has_hitbox': True,
        'speed': -2,
        'image': '4.png',
        'animation_frames': ['conveyor_1.png', 'conveyor_2.png', 'conveyor_3.png'],
    },
    TileType.CONVEYOR_RIGHT: {
        'solid': True,
        'has_hitbox': True,
        'speed': 2,
        'image': '5.png',
        'animation_frames': ['conveyor_1.png', 'conveyor_2.png', 'conveyor_3.png'],
    },
    TileType.DESTRUCTIBLE: {
        'solid': True,
        'has_hitbox': True,
        'health': 1,
        'image': '6.png',
        'animation_frames': [],
        'destructible': True,
        'break_effect': 'break_particles',
    },
    TileType.SPIKE: {
        'solid': False,
        'has_hitbox': True,
        'damage': 1,
        'image': '7.png',
        'animation_frames': [],
    },
    TileType.POWERUP_SPAWN: {
        'solid': False,
        'has_hitbox': False,
        'powerup_type': None,  # Set when creating level
        'image': None,  # Invisible spawn point
        'animation_frames': [],
    },
    TileType.ENEMY_SPAWN: {
        'solid': False,
        'has_hitbox': False,
        'enemy_type': None,  # Set when creating level
        'image': None,  # Invisible spawn point
        'animation_frames': [],
    },
    TileType.CHECKPOINT: {
        'solid': False,
        'has_hitbox': True,
        'image': '10.png',
        'animation_frames': ['checkpoint_1.png', 'checkpoint_2.png'],
        'activated': False,
    },
    TileType.FINISH: {
        'solid': False,
        'has_hitbox': True,
        'image': '11.png',
        'animation_frames': ['finish_1.png', 'finish_2.png'],
    },
    TileType.BACKGROUND: {
        'solid': False,
        'has_hitbox': False,
        'damage': 0,
        'image': 'background.png',
        'animation_frames': [],
        'layer': 'background'
    },
    TileType.PORTAL_SET_1: {
        'solid': False,
        'has_hitbox': True,
        'damage': 0,
        'image': 'portal_1.png',
        'animation_frames': [],
        'portal_type': 1,
        'cooldown': 1000,  # Cooldown in milliseconds
    },
    TileType.PORTAL_SET_2: {
        'solid': False,
        'has_hitbox': True,
        'damage': 0,
        'image': 'portal_2.png',
        'animation_frames': [],
        'portal_type': 2,
        'cooldown': 1000,  # Cooldown in milliseconds
    },
    TileType.PICKUP_COIN: {
        'solid': False,
        'has_hitbox': True,
        'damage': 0,
        'image': 'coin.png',
        'value': 1,
        'pickup_type': 'coin'
    },
    TileType.PICKUP_ONEUP: {
        'solid': False,
        'has_hitbox': True,
        'damage': 0,
        'image': 'apple.png',
        'animation_frames': ['oneup_1.png', 'oneup_2.png'],
        'value': 1,
        'pickup_type': 'oneup'
    },
}
