import pygame as pg
import math
import settings

class RayCaster:
    def __init__(self, game,
                 starting_pos,
                 angle,
                 remove_fishbowl):
        self.game = game
        self.x, self.y = starting_pos
        self.angle = angle
        self.remove_fishbowl = remove_fishbowl
        
        self.depth = 0
        self.projection_height = 0
        self.texture = 0
        self.image_offset = 0
        self.cast_ray()
        
    def cast_ray(self):
        x_map, y_map = int(self.x), int(self.y)
        
        texture_vert, texture_hor = 0, 0
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        
        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
        depth_hor = (y_hor - self.y) / sin_a
        x_hor = self.x + depth_hor * cos_a
        
        delta_depth = dy / sin_a
        dx = delta_depth * cos_a
        
        for i in range(max(self.game.map.n_rows, self.game.map.n_cols)):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor in self.game.map.walls_dict:
                texture_hor = self.game.map.walls_dict[tile_hor]
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth
            
        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
        depth_vert = (x_vert - self.x) / cos_a
        y_vert = self.y + depth_vert * sin_a
        
        delta_depth = dx / cos_a
        dy = delta_depth * sin_a
        
        for i in range(max(self.game.map.n_rows, self.game.map.n_cols)):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert in self.game.map.walls_dict:
                texture_vert = self.game.map.walls_dict[tile_vert]
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth
            
        # depth, texture, offset for texturing
        if depth_vert < depth_hor:
            self.depth = depth_vert
            self.texture = texture_vert
            y_vert %= 1
            self.image_offset = y_vert if cos_a > 0 else (1 - y_vert)
        else:
            self.depth = depth_hor
            self.texture = texture_hor
            x_hor %= 1
            self.image_offset = (1 - x_hor) if sin_a > 0 else x_hor
            
        if self.remove_fishbowl:
            self.depth *= math.cos(self.game.player.angle - self.angle)
        
        # we need to calculate the projection height for 3d rendering
        self.projection_height = settings.screen_dist / (self.depth + 0.0001)            
        