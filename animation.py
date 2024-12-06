import pygame
import os
from settings import *

class Animation:
    def __init__(self):
        self.sprites = {}
        self.current_frame = 0
        self.animation_time = 0

    def load_sprite_sheets(self, path, scale=1):
        """
        Load all sprite sheets from a directory.
        Directory structure should be:
        path/
            state_name/
                frame1.png
                frame2.png
                ...
        """
        for state in os.listdir(path):
            state_path = os.path.join(path, state)
            if os.path.isdir(state_path):
                self.sprites[state] = []
                for frame in sorted(os.listdir(state_path)):
                    if frame.endswith('.png'):
                        image_path = os.path.join(state_path, frame)
                        image = pygame.image.load(image_path).convert_alpha()
                        if scale != 1:
                            new_width = image.get_width() * scale
                            new_height = image.get_height() * scale
                            image = pygame.transform.scale(image, (new_width, new_height))
                        self.sprites[state].append(image)

    def animate(self, state, dt):
        """
        Returns the current frame of the animation for the given state
        """
        if state not in self.sprites:
            return None

        self.animation_time += dt
        if self.animation_time >= ANIMATION_SPEED:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites[state])

        return self.sprites[state][self.current_frame]
