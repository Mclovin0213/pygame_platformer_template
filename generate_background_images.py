import pygame
import os

def create_gradient_surface(width, height, start_color, end_color):
    surface = pygame.Surface((width, height))
    for y in range(height):
        lerp = y / height
        color = [start + (end - start) * lerp for start, end in zip(start_color, end_color)]
        pygame.draw.line(surface, color, (0, y), (width, y))
    return surface

def generate_background_images():
    pygame.init()
    
    # Create backgrounds directory if it doesn't exist
    os.makedirs('assets/backgrounds', exist_ok=True)
    
    # Background dimensions
    width, height = 1920, 1080  # Wide enough for parallax scrolling
    
    # Level 1 backgrounds
    # Sky
    sky = create_gradient_surface(width, height, (135, 206, 235), (65, 105, 225))
    pygame.image.save(sky, 'assets/backgrounds/level1_sky.png')
    
    # Mountains
    mountains = pygame.Surface((width, height), pygame.SRCALPHA)
    for i in range(5):
        x = width * i // 5
        points = [(x, height), (x + width//10, height//2), (x + width//5, height)]
        pygame.draw.polygon(mountains, (100, 100, 100, 255), points)
    pygame.image.save(mountains, 'assets/backgrounds/level1_mountains.png')
    
    # Trees
    trees = pygame.Surface((width, height), pygame.SRCALPHA)
    for i in range(10):
        x = width * i // 10
        pygame.draw.rect(trees, (34, 139, 34, 255), (x, height//2, 40, height//2))
        pygame.draw.circle(trees, (46, 139, 87, 255), (x + 20, height//2), 50)
    pygame.image.save(trees, 'assets/backgrounds/level1_trees.png')
    
    # Level 2 backgrounds
    # Sky
    sky2 = create_gradient_surface(width, height, (25, 25, 112), (70, 130, 180))
    pygame.image.save(sky2, 'assets/backgrounds/level2_sky.png')
    
    # Clouds
    clouds = pygame.Surface((width, height), pygame.SRCALPHA)
    for i in range(8):
        x = width * i // 8
        y = height // 3 + (i % 3) * 50
        pygame.draw.circle(clouds, (255, 255, 255, 128), (x, y), 40)
        pygame.draw.circle(clouds, (255, 255, 255, 128), (x + 30, y), 40)
    pygame.image.save(clouds, 'assets/backgrounds/level2_clouds.png')
    
    # City
    city = pygame.Surface((width, height), pygame.SRCALPHA)
    for i in range(15):
        x = width * i // 15
        h = height//3 + (i % 4) * 50
        pygame.draw.rect(city, (50, 50, 50, 255), (x, height - h, 60, h))
        # Windows
        for wy in range(h//40):
            for wx in range(2):
                pygame.draw.rect(city, (255, 255, 0, 255), 
                               (x + 15 + wx*20, height - h + 10 + wy*40, 10, 20))
    pygame.image.save(city, 'assets/backgrounds/level2_city.png')
    
    pygame.quit()

if __name__ == '__main__':
    generate_background_images()
