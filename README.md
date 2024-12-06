# Pygame Platformer Template

A flexible and easy-to-use template for creating 2D platformer games with Pygame.

## Features
- Tile-based level creation
- Sprite animation system
- Player physics (movement, jumping, collision detection)
- Easy-to-modify settings

## Project Structure
```
pygame_platformer_template/
├── assets/
│   ├── player/
│   │   ├── idle/
│   │   ├── run/
│   │   └── jump/
│   └── tiles/
├── main.py
├── player.py
├── animation.py
├── tilemap.py
├── settings.py
└── requirements.txt
```

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create the asset structure:
```
assets/
    player/
        idle/
            1.png
            2.png
            ...
        run/
            1.png
            2.png
            ...
        jump/
            1.png
            ...
    tiles/
        1.png
        2.png
        ...
```

## Creating Levels
1. Place your tile images in the `assets/tiles` directory
2. Name each tile image with a number (e.g., `1.png`, `2.png`)
3. Modify the level layout in `main.py`:
```python
level = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]
```
Where:
- 0 represents empty space
- Numbers correspond to tile image names (1.png, 2.png, etc.)

## Adding Player Animations
1. Create directories for each animation state in `assets/player/`
2. Place numbered frames (e.g., `1.png`, `2.png`) in each state directory
3. The animation system will automatically load and cycle through these frames

## Customizing the Game
- Modify `settings.py` to change:
  - Window dimensions
  - Player movement speed
  - Gravity strength
  - Animation speed
  - Tile size
  - And more!

## Controls
- Left/Right Arrow Keys: Move
- Space: Jump

## License
This template is free to use for any purpose.
