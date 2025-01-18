import pygame
import os

class MusicManager:
    def __init__(self):
        self.current_music = None
        self.menu_music_path = None
        self.game_music_path = None
        self.death_music_path = None
        self.victory_music_path = None
        
    def set_menu_music(self, path):
        """Set the path for menu music"""
        self.menu_music_path = path
        
    def set_game_music(self, path):
        """Set the path for game music"""
        self.game_music_path = path
        
    def set_death_music(self, path):
        """Set the path for death music"""
        self.death_music_path = path
        
    def set_victory_music(self, path):
        """Set the path for victory/completion music"""
        self.victory_music_path = path
        
    def play_menu_music(self):
        """Play menu music if set"""
        if self.menu_music_path and os.path.exists(self.menu_music_path):
            if self.current_music != self.menu_music_path:
                pygame.mixer.music.load(self.menu_music_path)
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
                self.current_music = self.menu_music_path
                
    def play_game_music(self):
        """Play game music if set"""
        if self.game_music_path and os.path.exists(self.game_music_path):
            if self.current_music != self.game_music_path:
                pygame.mixer.music.load(self.game_music_path)
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
                self.current_music = self.game_music_path
                
    def play_death_music(self):
        """Play death music if set"""
        if self.death_music_path and os.path.exists(self.death_music_path):
            if self.current_music != self.death_music_path:
                pygame.mixer.music.load(self.death_music_path)
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
                self.current_music = self.death_music_path
                
    def play_victory_music(self):
        """Play victory music if set"""
        if self.victory_music_path and os.path.exists(self.victory_music_path):
            if self.current_music != self.victory_music_path:
                pygame.mixer.music.load(self.victory_music_path)
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
                self.current_music = self.victory_music_path
                
    def stop_music(self):
        """Stop current music"""
        pygame.mixer.music.stop()
        self.current_music = None
