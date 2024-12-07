import pygame
from settings import *
from animation import Animation

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, platform_sprites=None, ladder_sprites=None, conveyor_sprites=None):
        super().__init__(groups)
        
        # Animation setup
        self.animation = Animation()
        self.animation.load_sprite_sheets(PLAYER_SPRITES_PATH)
        self.state = 'idle'
        self.facing_right = True
        
        # Get the first frame for initial setup
        self.image = self.animation.sprites['idle'][0]
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
        
        # State flags
        self.on_ladder = False
        self.on_platform = False
        self.on_conveyor = False

    def input(self):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
            self.state = 'run'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
            self.state = 'run'
        else:
            self.direction.x = 0
            if self.on_ground:
                self.state = 'idle'
        
        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.direction.y = self.jump_speed
            self.state = 'jump'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.hitbox.y += self.direction.y

    def horizontal_collisions(self):
        """Handle horizontal collisions with solid tiles and conveyors"""
        self.hitbox.x += self.direction.x * self.speed
        
        # Check conveyor belt effects
        for sprite in self.conveyor_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                self.on_conveyor = True
                conveyor_speed = TILE_PROPERTIES[sprite.tile_type].get('speed', 0)
                self.hitbox.x += conveyor_speed
                break
        else:
            self.on_conveyor = False
        
        # Check solid collisions
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.x < 0:  # Moving left
                    self.hitbox.left = sprite.hitbox.right
                elif self.direction.x > 0:  # Moving right
                    self.hitbox.right = sprite.hitbox.left
                
        # Update rect position
        self.rect.centerx = self.hitbox.centerx
    
    def vertical_collisions(self):
        """Handle vertical collisions with solid tiles, platforms, and ladders"""
        # Apply gravity
        if not self.on_ladder:
            self.direction.y += self.gravity
            
        self.hitbox.y += self.direction.y
        
        # Check ladder collisions
        self.on_ladder = False
        for sprite in self.ladder_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                self.on_ladder = True
                if pygame.key.get_pressed()[pygame.K_UP]:
                    self.direction.y = -self.speed
                elif pygame.key.get_pressed()[pygame.K_DOWN]:
                    self.direction.y = self.speed
                else:
                    self.direction.y = 0
                break
        
        # Check platform and solid collisions
        self.on_ground = False
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.y > 0:  # Moving down
                    self.hitbox.bottom = sprite.hitbox.top
                    self.rect.bottom = self.hitbox.bottom  # Update rect to match hitbox
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0:  # Moving up
                    self.hitbox.top = sprite.hitbox.bottom
                    self.rect.top = self.hitbox.top  # Update rect to match hitbox
                    self.direction.y = 0
        
        # Check one-way platform collisions
        if not self.on_ground:
            for sprite in self.platform_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0 and self.hitbox.bottom <= sprite.hitbox.centery:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.rect.bottom = self.hitbox.bottom  # Update rect to match hitbox
                        self.direction.y = 0
                        self.on_ground = True
                        break
        
        # Update rect position
        self.rect.centery = self.hitbox.centery
        
    def animate(self, dt):
        current_frame = self.animation.animate(self.state, dt)
        if current_frame:
            self.image = current_frame
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

    def update(self, dt):
        self.input()
        self.horizontal_collisions()
        self.vertical_collisions()
        self.animate(dt)
