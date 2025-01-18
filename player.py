import pygame
from settings import *
from animation import Animation
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(message)s',
                   datefmt='%H:%M:%S')

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, platform_sprites=None, ladder_sprites=None, conveyor_sprites=None, portal_sprites=None, checkpoint_tiles=None, pickup_sprites=None, next_level_tiles=None, finish_tiles=None):
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
        self.checkpoint_pos = pos  # Store last checkpoint position
        
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
        self.checkpoint_tiles = checkpoint_tiles or pygame.sprite.Group()
        self.platform_sprites = platform_sprites or pygame.sprite.Group()
        self.ladder_sprites = ladder_sprites or pygame.sprite.Group()
        self.conveyor_sprites = conveyor_sprites or pygame.sprite.Group()
        self.portal_sprites = portal_sprites or pygame.sprite.Group()
        self.pickup_sprites = pickup_sprites or pygame.sprite.Group()
        self.next_level_tiles = next_level_tiles or pygame.sprite.Group()
        self.finish_tiles = finish_tiles or pygame.sprite.Group()
        
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
        # Apply horizontal movement
        movement = self.direction.x * self.speed
        self.hitbox.x += movement
        
        # Create a combined list of relevant collision objects
        collision_objects = []
        # Add solid tiles first as they take priority
        collision_objects.extend((sprite, 'solid') for sprite in self.collision_sprites)
        # Add conveyor tiles with their properties
        collision_objects.extend((sprite, 'conveyor') for sprite in self.conveyor_sprites)
        
        self.on_conveyor = False
        
        # Check all collisions in one pass
        for sprite, obj_type in collision_objects:
            if sprite.hitbox.colliderect(self.hitbox):
                if obj_type == 'solid':
                    # Handle solid collision
                    if self.direction.x < 0:  # Moving left
                        self.hitbox.left = sprite.hitbox.right
                    elif self.direction.x > 0:  # Moving right
                        self.hitbox.right = sprite.hitbox.left
                    break  # Exit after first solid collision
                elif obj_type == 'conveyor' and not self.on_conveyor:
                    # Only apply conveyor if no solid collision occurred
                    self.on_conveyor = True
                    conveyor_speed = TILE_PROPERTIES[sprite.tile_type].get('speed', 0)
                    # Check if applying conveyor speed would cause a collision
                    self.hitbox.x += conveyor_speed
                    # Check if this would cause a collision with a solid
                    for solid in self.collision_sprites:
                        if solid.hitbox.colliderect(self.hitbox):
                            # Revert conveyor movement if it would cause collision
                            self.hitbox.x -= conveyor_speed
                            break
        
        # Update rect position
        self.rect.centerx = self.hitbox.centerx

    def vertical_collisions(self):
        """Handle vertical collisions with solid tiles, platforms, and ladders"""
        # First check ladder collisions as they don't need complex resolution
        self.on_ladder = False
        for sprite in self.ladder_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                self.on_ladder = True
                logging.info("Player touching ladder")
                break
            
        # Apply gravity only if not climbing
        if not self.is_climbing:
            self.direction.y += self.gravity
            
        # Store original position for platform checks
        original_y = self.hitbox.y
        next_y = original_y + self.direction.y
        
        logging.debug(f"Player Y movement: original_y={original_y:.2f}, next_y={next_y:.2f}, direction.y={self.direction.y:.2f}")
        
        # First check platforms when moving downward
        self.on_ground = False
        if self.direction.y > 0:  # Only check platforms when falling
            logging.info(f"Number of platform sprites: {len(self.platform_sprites)}")
            
            # Calculate player center for more precise platform detection
            player_center_x = self.hitbox.centerx
            
            # Sort platforms by distance to player center for more accurate collision detection
            sorted_platforms = sorted(
                self.platform_sprites,
                key=lambda sprite: abs(sprite.hitbox.centerx - player_center_x)
            )
            
            for sprite in sorted_platforms:
                logging.debug(f"Checking platform at position {sprite.rect.topleft}")
                logging.debug(f"Platform hitbox: top={sprite.hitbox.top}, bottom={sprite.hitbox.bottom}")
                logging.debug(f"Player hitbox: x={self.hitbox.x}, width={self.hitbox.width}")
                logging.debug(f"Platform hitbox: x={sprite.hitbox.x}, width={sprite.hitbox.width}")
                
                # Add horizontal tolerance for platform edges (half of tile size)
                edge_tolerance = TILE_SIZE // 2
                
                # Check if we're horizontally within the platform's bounds (with tolerance)
                horizontally_aligned = (
                    self.hitbox.right > sprite.hitbox.left - edge_tolerance and 
                    self.hitbox.left < sprite.hitbox.right + edge_tolerance
                )
                
                # We're falling and were above the platform in the previous frame
                was_above = original_y + self.hitbox.height <= sprite.hitbox.top + 5
                will_intersect = next_y + self.hitbox.height > sprite.hitbox.top
                
                logging.debug(f"Horizontally aligned with platform: {horizontally_aligned}")
                logging.debug(f"Was above platform: {was_above}")
                logging.debug(f"Will intersect platform: {will_intersect}")
                
                if horizontally_aligned and was_above and will_intersect:
                    logging.info(f"Landing on platform at y={sprite.hitbox.top}")
                    self.hitbox.y = sprite.hitbox.top - self.hitbox.height
                    self.direction.y = 0
                    self.on_ground = True
                    break
        
        # If we haven't landed on a platform, apply movement and check solid collisions
        if not self.on_ground:
            self.hitbox.y = next_y
            logging.debug("Checking solid collisions")
            for sprite in self.collision_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # Moving down
                        logging.info(f"Landing on solid tile at y={sprite.hitbox.top}")
                        self.hitbox.bottom = sprite.hitbox.top
                        self.direction.y = 0
                        self.on_ground = True
                    elif self.direction.y < 0:  # Moving up
                        logging.info(f"Hitting ceiling at y={sprite.hitbox.bottom}")
                        self.hitbox.top = sprite.hitbox.bottom
                        self.direction.y = 0
                    break
        
        # Log final position
        logging.debug(f"Final position: y={self.hitbox.y:.2f}, on_ground={self.on_ground}, direction.y={self.direction.y:.2f}")
        
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
        self.hitbox.topleft = self.checkpoint_pos
        self.rect.topleft = self.checkpoint_pos
        self.direction = pygame.math.Vector2()
        self.on_ground = False
    
    def check_next_level_collision(self):
        next_level_hits = pygame.sprite.spritecollide(self, self.next_level_tiles, False)
        for tile in next_level_hits:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                # Trigger level progression logic
                return True
        return False

    def check_finish_collision(self):
        """
        Check if player has collided with the finish tile
        """
        finish_hits = pygame.sprite.spritecollide(self, self.finish_tiles, False)
        return len(finish_hits) > 0

    def update(self, dt):
        """Update player state"""
        # Check portal interaction
        self.near_portal = False
        portal_collisions = pygame.sprite.spritecollide(self, self.portal_sprites, False)
        if portal_collisions:
            self.near_portal = True
            logging.info("Player near portal")
        
        # Check checkpoint collision
        checkpoint_hits = pygame.sprite.spritecollide(self, self.checkpoint_tiles, False)
        if checkpoint_hits:
            checkpoint = checkpoint_hits[0]
            self.checkpoint_pos = checkpoint.rect.topleft
            logging.info(f"Checkpoint reached at position: {self.checkpoint_pos}")
        
        # Check next level collision
        if self.check_next_level_collision():
            logging.info("Player reached next level")
        
        # Check finish collision
        if self.check_finish_collision():
            logging.info("Player reached finish")
        
        # Get input
        self.input()
        
        # Apply movement
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
        
        # Check pickup collection
        if self.pickup_sprites:
            for pickup in self.pickup_sprites:
                if self.hitbox.colliderect(pickup.hitbox):
                    pickup.collect(self)
