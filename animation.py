import pygame
import os
from settings import *

class Animation:
    def __init__(self, default_state='idle'):
        self.sprites = {}
        self.current_frame = 0
        self.animation_time = 0
        self.current_state = default_state
        self.previous_state = default_state
        self.state_changed = False

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

    def set_state(self, new_state):
        """
        Change the current animation state
        Returns True if the state was changed
        """
        if new_state not in self.sprites:
            return False
            
        if new_state != self.current_state:
            self.previous_state = self.current_state
            self.current_state = new_state
            self.current_frame = 0
            self.animation_time = 0
            self.state_changed = True
            return True
        return False

    def get_current_frame(self, flip_x=False):
        """
        Returns the current frame of animation
        """
        if self.current_state not in self.sprites:
            return None
            
        current_frame = self.sprites[self.current_state][self.current_frame]
        if flip_x:
            return pygame.transform.flip(current_frame, True, False)
        return current_frame

    def update(self, dt):
        """
        Update animation state
        Returns the current frame
        """
        if self.current_state not in self.sprites:
            return None

        self.animation_time += dt
        if self.animation_time >= ANIMATION_SPEED:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites[self.current_state])
            self.state_changed = False

        return self.sprites[self.current_state][self.current_frame]
