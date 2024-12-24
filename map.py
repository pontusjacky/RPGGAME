import numpy as np
import random
from PIL import Image

class genrate_map:
    def __init__(self, size=50):
        self.size = size
        self.map = np.random.choice(['water', 'forest', 'mountain', 'plain'], (size, size), p=[0.2, 0.3, 0.3, 0.2])
        self.terrain_types = ['water', 'forest', 'mountain', 'plain']
    
    def dfs(self, x, y, terrain_type, visited):
        stack = [(x, y)]
        region = []

        while stack:
            cx, cy = stack.pop()
            
            if visited[cx, cy]:
                continue
            
            visited[cx, cy] = True
            region.append((cx, cy))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and not visited[nx, ny]:
                    if self.map[nx, ny] == terrain_type:
                        stack.append((nx, ny))
        return region
    def fitness(self):
        
        rate = 1
        plain_ratio = np.sum(self.map == 'plain') / (self.size * self.size)
        forest_ratio = np.sum(self.map == 'forest') / (self.size * self.size)
        if plain_ratio < forest_ratio:
            rate = 0.8
        diversity_score = len(np.unique(self.map)) / 4.0
        continuity_score = self.continuity_score()
        penalty_score = self.penalty_score()
        return (0.5 * diversity_score + 0.5 * continuity_score - 2 * penalty_score)*rate

    def continuity_score(self):
        continuity = 0

        for x in range(self.size):
            for y in range(self.size):
                terrain = self.map[x, y]
                
                neighbors = [
                    self.map[i, j]
                    for i in range(max(0, x - 1), min(self.size, x + 2))
                    for j in range(max(0, y - 1), min(self.size, y + 2))
                    if (i, j) != (x, y) 
                ]
                continuity += neighbors.count(terrain)

        max_possible_neighbors = sum(
            min(3, x + 1) * min(3, y + 1) - 1
            for x in range(self.size) for y in range(self.size)
        )

        return continuity / max_possible_neighbors
    def penalty_score(self):
        visited = np.zeros_like(self.map, dtype=bool)
        penalty = 0

        for x in range(self.size):
            for y in range(self.size):
                if not visited[x, y]:
                    terrain_type = self.map[x, y]
                    region = self.dfs(x, y, terrain_type, visited)
                    region_size = len(region)
                    if region_size < 10:
                        penalty += (100 - region_size) /5000
                    elif region_size < 50:
                        penalty += (100 - region_size) /125000
                    elif region_size < 100:
                        penalty += (100 - region_size) /250000
        return penalty  

            
    def mutate(self):
        if np.random.rand() < 0.8:
            self.local_mutation()
        else:
            self.global_mutation()
    
    def local_mutation(self):
        mutation_rate = 0.1  
        num_mutations = int(self.map.size * mutation_rate)
        size = self.map.shape[0]

        for _ in range(num_mutations):
            x, y = np.random.randint(0, size, size=2)
            self.map[x, y] = np.random.choice(['water', 'forest', 'mountain', 'plain'])
            
    def global_mutation(self):
        size = self.map.shape[0]
        region_size = np.random.randint(size // 4, size // 2)
        x_start = np.random.randint(0, size - region_size)
        y_start = np.random.randint(0, size - region_size)
        
        new_terrain = np.random.choice(self.terrain_types)
        
        a = np.random.randint(region_size // 3, region_size)
        b = np.random.randint(region_size // 3, region_size)
        
        for x in range(x_start, x_start + region_size):
            for y in range(y_start, y_start + region_size):
                dx = x - (x_start + region_size // 2)
                dy = y - (y_start + region_size // 2)
                # 橢圓方程：((dx^2)/(a^2)) + ((dy^2)/(b^2)) <= 1
                if (dx**2) / (a**2) + (dy**2) / (b**2) <= 1:
                    if 0 <= x < self.size and 0 <= y < self.size:
                        self.map[x, y] = new_terrain
        
    
        
    def to_image(self, filepath):
        color_map = {
            'water': (0, 0, 255),         
            'forest': (0, 100, 0),       
            'mountain': (139, 137, 137),
            'plain': (144, 238, 144)
        }
        img = Image.new('RGB', (self.size, self.size))
        pixels = img.load()
        for i in range(self.size):
            for j in range(self.size):
                pixels[j, i] = color_map[self.map[i, j]]
        img = img.resize((500, 500), Image.NEAREST)
        img.save(filepath)
