import pygame
from settings import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        
    def apply(self, entity):
        """Returns a rect with camera offset applied"""
        return entity.rect.move(self.camera.topleft)
    
    def apply_rect(self, rect):
        """Returns a rect with camera offset applied"""
        return rect.move(self.camera.topleft)
        
    def update(self, target):
        """Updates camera position to follow target"""
        x = -target.rect.centerx + WINDOW_WIDTH // 2
        y = -target.rect.centery + WINDOW_HEIGHT // 2
        
        # Limit scrolling to map size
        x = min(0, x)  # left side
        x = max(-(self.width - WINDOW_WIDTH), x)  # right side
        y = min(0, y)  # top side
        y = max(-(self.height - WINDOW_HEIGHT), y)  # bottom side
        
        self.camera = pygame.Rect(x, y, self.width, self.height)
        
    @property
    def x(self):
        """Get the camera's x position"""
        return self.camera.x
        
    @property
    def y(self):
        """Get the camera's y position"""
        return self.camera.y
