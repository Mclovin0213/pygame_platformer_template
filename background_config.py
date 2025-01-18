"""
Configuration file for level backgrounds.
Each level can have multiple background layers that move at different speeds.
The closer the scroll_speed is to 1.0, the faster it moves with the camera.
"""

LEVEL_BACKGROUNDS = {
    'Level 1': [
        # Example background layers for Level 1
        # Format: (image_path, scroll_speed)
        ('assets/backgrounds/level1_sky.png', 0.1),
        ('assets/backgrounds/level1_mountains.png', 0.3),
        ('assets/backgrounds/level1_trees.png', 0.6),
    ],
    'Level 2': [
        # Example background layers for Level 2
        ('assets/backgrounds/level2_sky.png', 0.1),
        ('assets/backgrounds/level2_clouds.png', 0.2),
        ('assets/backgrounds/level2_city.png', 0.4),
    ]
}
