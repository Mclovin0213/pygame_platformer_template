import pygame
import os

class ParallaxLayer:
    def __init__(self, image_path, scroll_speed):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.scroll_speed = scroll_speed
        self.x1 = 0
        self.x2 = self.image.get_width()
        
    def update(self, camera_x):
        # Calculate relative position based on camera
        rel_x = (camera_x * self.scroll_speed) % self.image.get_width()
            
    def draw(self, screen, camera_x):
        # Calculate relative position based on camera
        rel_x = (camera_x * self.scroll_speed) % self.image.get_width()
        
        # Draw the background images side by side
        if rel_x < 0:
            screen.blit(self.image, (rel_x + self.image.get_width(), 0))
            screen.blit(self.image, (rel_x, 0))
        else:
            screen.blit(self.image, (rel_x - self.image.get_width(), 0))
            screen.blit(self.image, (rel_x, 0))

class ParallaxBackground:
    def __init__(self):
        self.layers = []
        
    def add_layer(self, image_path, scroll_speed):
        """
        Add a new parallax layer
        :param image_path: Path to the background image
        :param scroll_speed: Speed at which this layer scrolls (0.0 to 1.0)
        """
        if os.path.exists(image_path):
            layer = ParallaxLayer(image_path, scroll_speed)
            self.layers.append(layer)
        else:
            print(f"Warning: Background image not found at {image_path}")
            
    def update(self, camera_x):
        """Update all parallax layers"""
        for layer in self.layers:
            layer.update(camera_x)
            
    def draw(self, screen, camera_x):
        """Draw all parallax layers"""
        for layer in self.layers:
            layer.draw(screen, camera_x)
