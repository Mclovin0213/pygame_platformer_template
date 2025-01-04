from enum import Enum
import pygame
import os
from settings import *

class EnemyType(Enum):
    """Enum for different enemy types"""
    WALKER = 'walker'
    JUMPER = 'jumper'
    FLYER = 'flyer'

# Define properties for each enemy type
ENEMY_PROPERTIES = {
    EnemyType.WALKER: {
        'size': (32, 64),
        'color': 'red',  # Fallback color if sprite not found
        'speed': 2,
        'damage': 1,
        'health': 2,
        'patrol_distance': 100,
        'affected_by_gravity': True,
        'can_jump': False,
        'sprite_name': 'walker.png'  # Sprite filename in assets/enemies
    },
    EnemyType.JUMPER: {
        'size': (32, 32),
        'color': 'green',  # Fallback color if sprite not found
        'speed': 3,
        'damage': 1,
        'health': 1,
        'patrol_distance': 150,
        'affected_by_gravity': True,
        'can_jump': True,
        'jump_force': -8,
        'jump_cooldown': 2000,  # milliseconds
        'sprite_name': 'jumper.png'  # Sprite filename in assets/enemies
    },
    EnemyType.FLYER: {
        'size': (48, 48),
        'color': 'purple',  # Fallback color if sprite not found
        'speed': 4,
        'damage': 2,
        'health': 1,
        'patrol_distance': 200,
        'affected_by_gravity': False,
        'can_jump': False,
        'vertical_amplitude': 50,  # Pixels to move up/down
        'vertical_speed': 2,
        'sprite_name': 'bat_temp.png'  # Sprite filename in assets/enemies
    }
}

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, enemy_type, groups, collision_sprites):
        super().__init__(groups)
        
        # Get properties for this enemy type
        self.enemy_type = enemy_type
        self.properties = ENEMY_PROPERTIES[enemy_type]
        
        # Try to load sprite, fall back to colored rectangle if not found
        sprite_path = os.path.join(ENEMY_SPRITES_PATH, self.properties['sprite_name'])
        try:
            if os.path.exists(sprite_path):
                self.image = pygame.image.load(sprite_path).convert_alpha()
            else:
                self.image = pygame.Surface(self.properties['size'])
                self.image.fill(self.properties['color'])
        except (pygame.error, FileNotFoundError):
            self.image = pygame.Surface(self.properties['size'])
            self.image.fill(self.properties['color'])
        
        # Basic setup
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-20, 0)
        
        # Stats
        self.health = self.properties['health']
        self.speed = self.properties['speed']
        self.damage = self.properties['damage']
        
        # Movement
        self.direction = pygame.math.Vector2(1, 0)  # Start moving right
        self.gravity = GRAVITY if self.properties['affected_by_gravity'] else 0
        self.on_ground = False
        self.start_x = pos[0]
        self.start_y = pos[1]
        self.patrol_distance = self.properties['patrol_distance']
        
        # Special movement variables
        if enemy_type == EnemyType.JUMPER:
            self.jump_cooldown = self.properties['jump_cooldown']
            self.can_jump = True
            self.last_jump = 0
        elif enemy_type == EnemyType.FLYER:
            self.vertical_offset = 0
            self.vertical_direction = 1
        
        # Collision
        self.collision_sprites = collision_sprites

    def move(self, dt):
        if self.properties['affected_by_gravity'] and not self.on_ground:
            self.direction.y += self.gravity * dt
        
        # Type-specific movement
        if self.enemy_type == EnemyType.FLYER:
            # Sinusoidal vertical movement
            self.vertical_offset += self.properties['vertical_speed'] * self.vertical_direction
            if abs(self.vertical_offset) > self.properties['vertical_amplitude']:
                self.vertical_direction *= -1
            self.direction.y = self.vertical_direction * self.properties['vertical_speed']
        elif self.enemy_type == EnemyType.JUMPER:
            # Jump when on ground and cooldown is ready
            current_time = pygame.time.get_ticks()
            if self.on_ground and current_time - self.last_jump > self.jump_cooldown:
                self.direction.y = self.properties['jump_force']
                self.last_jump = current_time
                self.on_ground = False
        
        # Update position horizontally
        self.hitbox.x += self.direction.x * self.speed
        self.check_collisions('horizontal')
        
        # Update position vertically
        self.hitbox.y += self.direction.y
        self.check_collisions('vertical')
        
        # Update rect to match hitbox
        self.rect.center = self.hitbox.center
        
        # Check patrol boundaries for horizontal movement
        if abs(self.hitbox.x - self.start_x) > self.patrol_distance:
            self.direction.x *= -1

    def check_collisions(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    else:
                        self.hitbox.left = sprite.rect.right
                    self.direction.x *= -1
                else:  # vertical
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                        self.direction.y = 0
                        self.on_ground = True
                    else:
                        self.hitbox.top = sprite.rect.bottom
                        self.direction.y = 0

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0

    def update(self, dt):
        self.move(dt)
