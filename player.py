import pygame
from settings import *
from animation import Animation
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(message)s',
                   datefmt='%H:%M:%S')

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, platform_sprites=None, ladder_sprites=None, conveyor_sprites=None, portal_sprites=None):
        super().__init__(groups)
        
        # Player stats
        self.max_health = 3
        self.health = self.max_health
        self.lives = 3
        self.coins = 0
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerability_duration = 1000
        self.initial_pos = pos
        
        # Animation setup
        self.animation = Animation('idle')
        self.animation.load_sprite_sheets(PLAYER_SPRITES_PATH)
        self.facing_right = True
        
        # Get the first frame for initial setup
        self.image = self.animation.get_current_frame()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-20, 0)
        
        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED
        self.gravity = GRAVITY
        self.jump_speed = PLAYER_JUMP_SPEED
        self.on_ground = False
        
        # Collision
        self.collision_sprites = collision_sprites
        self.platform_sprites = platform_sprites or pygame.sprite.Group()
        self.ladder_sprites = ladder_sprites or pygame.sprite.Group()
        self.conveyor_sprites = conveyor_sprites or pygame.sprite.Group()
        self.portal_sprites = portal_sprites or pygame.sprite.Group()
        
        # State flags
        self.on_ladder = False
        self.on_platform = False
        self.on_conveyor = False
        self.is_climbing = False  # New state to track if actually climbing
        self.near_portal = False

    def input(self):
        keys = pygame.key.get_pressed()
        
        # Start climbing only when pressing UP while touching a ladder
        if self.on_ladder and keys[pygame.K_UP]:
            self.is_climbing = True
            self.animation.set_state('climb')
        elif not self.on_ladder:
            self.is_climbing = False
        
        # Only restrict horizontal movement if actually climbing
        if not self.is_climbing:
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.facing_right = True
                self.animation.set_state('run')
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.facing_right = False
                self.animation.set_state('run')
            else:
                self.direction.x = 0
                if self.on_ground:
                    self.animation.set_state('idle')
        else:
            self.direction.x = 0
            
        # Ladder climbing
        if self.is_climbing:
            if keys[pygame.K_UP]:
                self.direction.y = -1
            elif keys[pygame.K_DOWN]:
                self.direction.y = +1
            else:
                self.direction.y = 0
        
        # Jump only if not climbing
        if keys[pygame.K_SPACE] and self.on_ground and not self.is_climbing:
            self.direction.y = self.jump_speed
            self.animation.set_state('jump')
        
        # Portal interaction
        if self.near_portal and keys[pygame.K_UP]:
            portal_collisions = pygame.sprite.spritecollide(self, self.portal_sprites, False)
            if portal_collisions:
                portal = portal_collisions[0]
                if hasattr(portal, 'teleport'):
                    portal.teleport(self)
                    logging.info("Player teleported through portal")

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.hitbox.y += self.direction.y

    def horizontal_collisions(self):
        """Handle horizontal collisions with solid tiles and conveyors"""
        self.hitbox.x += self.direction.x * self.speed
        
        # Check conveyor belt effects
        for sprite in self.conveyor_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                logging.info(f"Player on Conveyor tile type {sprite.tile_type.name} at position {sprite.rect.topleft}")
                self.on_conveyor = True
                conveyor_speed = TILE_PROPERTIES[sprite.tile_type].get('speed', 0)
                self.hitbox.x += conveyor_speed
                break
        else:
            self.on_conveyor = False
        
        # Check solid collisions
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                logging.info(f"Player colliding horizontally with Solid tile type {sprite.tile_type.name} at position {sprite.rect.topleft}")
                if self.direction.x < 0:  # Moving left
                    self.hitbox.left = sprite.hitbox.right
                elif self.direction.x > 0:  # Moving right
                    self.hitbox.right = sprite.hitbox.left
                
        # Update rect position
        self.rect.centerx = self.hitbox.centerx
    
    def vertical_collisions(self):
        """Handle vertical collisions with solid tiles, platforms, and ladders"""
        # Check ladder collisions first
        self.on_ladder = False
        for sprite in self.ladder_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                self.on_ladder = True
                logging.info(f"Player colliding with Ladder tile at position {sprite.rect.topleft}")
                break
            
        # Apply gravity only if not climbing
        if not self.is_climbing:
            self.direction.y += self.gravity
            
        self.hitbox.y += self.direction.y
        
        # Check platform and solid collisions
        self.on_ground = False
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                logging.info(f"Player colliding with Solid tile type {sprite.tile_type.name} at position {sprite.rect.topleft}")
                if self.direction.y > 0:  # Moving down
                    self.hitbox.bottom = sprite.hitbox.top
                    self.rect.bottom = self.hitbox.bottom
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0:  # Moving up
                    self.hitbox.top = sprite.hitbox.bottom
                    self.rect.top = self.hitbox.top
                    self.direction.y = 0
        
        # Check one-way platform collisions
        if not self.on_ground:
            for sprite in self.platform_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    logging.info(f"Player colliding with Platform tile at position {sprite.rect.topleft}")
                    if self.direction.y > 0 and self.hitbox.bottom <= sprite.hitbox.centery:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.rect.bottom = self.hitbox.bottom
                        self.direction.y = 0
                        self.on_ground = True
                        break
        
        # Update rect position
        self.rect.centery = self.hitbox.centery
    
    def take_damage(self, amount):
        if not self.invulnerable:
            self.health -= amount
            self.invulnerable = True
            self.invulnerable_timer = pygame.time.get_ticks()
            
            if self.health <= 0:
                self.lives -= 1
                if self.lives > 0:
                    self.respawn()
                return True  # Player died
        return False

    def respawn(self):
        self.health = self.max_health
        self.hitbox.topleft = self.initial_pos
        self.rect.topleft = self.initial_pos
        self.direction = pygame.math.Vector2()
        self.on_ground = False
    
    def update(self, dt):
        # Check portal collision
        self.near_portal = False
        portal_collisions = pygame.sprite.spritecollide(self, self.portal_sprites, False)
        if portal_collisions:
            self.near_portal = True
            logging.info("Player near portal")
        
        self.input()
        self.apply_gravity()
        self.horizontal_collisions()
        self.vertical_collisions()
        
        # Update invulnerability
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.invulnerable_timer >= self.invulnerability_duration:
                self.invulnerable = False
        
        # Update animation
        self.image = self.animation.update(dt)
        if self.facing_right:
            self.image = self.animation.get_current_frame()
        else:
            self.image = self.animation.get_current_frame(flip_x=True)
