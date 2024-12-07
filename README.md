# Pygame Platformer Template

Welcome to the **Pygame Platformer Template**! This project provides a modular and flexible foundation for building a 2D platformer game using the Pygame library. It includes essential components for player movement, tile-based environments, animations, and camera management.

---

## **Features**
- **Tile-Based World**: A flexible tile system for creating solid platforms, ladders, conveyors, destructible tiles, hazards, and more.
- **Animation System**: A robust framework for loading and managing sprite animations.
- **Camera System**: Smooth camera movement that follows the player and stays within level boundaries.
- **Entity Management**: Supports enemies, power-ups, checkpoints, and other interactive objects.
- **Level Data Parser**: Easily define levels using dictionaries for layout, background, and entity placement.

---

## **Setup Instructions**

### **1. Prerequisites**
Make sure you have the following installed:
- **Python 3.9+**
- **Pygame** (Install using `pip install pygame`)

---

### **2. Cloning the Repository**
```bash
git clone https://github.com/yourusername/pygame_platformer_template.git
cd pygame_platformer_template
```

---

### **3. Installing Dependencies**
The primary dependency for this project is Pygame. Install it by running:
```bash
pip install pygame
```

---

### **4. Running the Project**
To run the game, execute the following command:
```bash
python main.py
```
This will launch the game window, where you can test and explore the platformer template.

---

## **Project Structure**
```plaintext
pygame_platformer_template/
├── assets/                 # Game assets (sprites, tiles, sounds, etc.)
│   ├── player/             # Player sprite sheets
│   ├── tiles/              # Tileset images
│   └── background/         # Background images
├── settings.py             # Global constants for configuration
├── animation.py            # Animation handling system
├── camera.py               # Camera and viewport management
├── tilemap.py              # Tile and level management
├── level_data.py           # Level structure and data parser
├── player.py               # Player character class
├── main.py                 # Entry point for the game
└── README.md               # Project documentation
```

---

## **How to Use Each Module**

### **1. Animation System**
The `animation.py` module provides the `Animation` class for managing sprite animations.

#### Example:
```python
from animation import Animation

# Initialize and load animations
animation = Animation()
animation.load_sprite_sheets("assets/player", scale=2)

# Animate player state
current_frame = animation.animate("run", dt)
if current_frame:
    screen.blit(current_frame, (player_x, player_y))
```

### **2. Tilemap System**
The `tilemap.py` module handles tiles and level layout. You can load levels using predefined `level_data` structures.

#### Example:
```python
from tilemap import TileMap
from level_data import LEVEL_1

# Initialize the tilemap
tilemap = TileMap()
tilemap.load_map(LEVEL_1)

# Update and draw tiles
tilemap.update(dt)
tilemap.draw(screen)
```

### **3. Camera System**
The `camera.py` module provides the `Camera` class for managing the game’s viewport.

#### Example:
```python
from camera import Camera

# Initialize the camera
camera = Camera(world_width, world_height)

# Update the camera to follow the player
camera.update(player)

# Render objects relative to the camera
screen.blit(entity.image, camera.apply(entity))
```

---

## **Level Design**

Levels are defined in `level_data.py` using a dictionary-based format. A sample level looks like this:
```python
LEVEL_1 = {
    'name': 'Level 1',
    'background_color': (50, 50, 100),
    'main_layer': [
        "111111111111111111111111111111",
        "100000000000000000000000000001",
        "100000P00000000000000000F0001",
        "100000000L0000000000000000001",
        "111111111111111111111111111111"
    ],
    'entities': [
        {
            'type': 'enemy',
            'enemy_type': 'walker',
            'position': (5, 5),
            'properties': {'patrol_distance': 3}
        }
    ],
    'tile_mapping': {
        '1': TileType.SOLID,
        'P': TileType.POWERUP_SPAWN,
        'L': TileType.LADDER,
        'F': TileType.FINISH
    }
}
```

---

## **Configuration**
The `settings.py` file contains global constants that control various game parameters:
- **Window Settings**:
  ```python
  WINDOW_WIDTH = 1280
  WINDOW_HEIGHT = 720
  FPS = 60
  ```
- **Player Physics**:
  ```python
  PLAYER_SPEED = 5
  PLAYER_JUMP_SPEED = -8
  GRAVITY = 0.3
  ```
- **Animation**:
  ```python
  ANIMATION_SPEED = 0.15
  ```

---

## **Customization**

### Adding New Animations:
1. Add a new folder in the `assets/player/` directory (e.g., `slide`).
2. Place the animation frames in the folder (e.g., `frame1.png`, `frame2.png`).
3. Call `animation.load_sprite_sheets()` with the updated directory.

### Adding New Tile Types:
1. Add a new tile type to the `TileType` enum in `tile_types.py`.
2. Define its properties in `TILE_PROPERTIES`.

---

## **Contributing**
We welcome contributions! Feel free to fork the repository and submit pull requests with new features, bug fixes, or improvements.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## **Acknowledgments**
This template was built with love using the Pygame library. Special thanks to the open-source community for their contributions!
