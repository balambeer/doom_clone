import pygame as pg
import settings
import math

class Camera2d():
    def __init__(self, game,
                 starting_pos):
        self.game = game
        
        self.position = starting_pos
        self.x = self.position[0]
        self.y = self.position[1]
        
        self.fov_width = settings.camera_fov_width
        self.fov_height = settings.camera_fov_height
        self.fov_half_width = self.fov_width // 2
        self.fov_half_height = self.fov_height // 2
        self.left_edge = self.x - self.fov_half_width
        self.top_edge = self.y - self.fov_half_height
        
        self.tile_size_2d = settings.screen_width // self.fov_width
        self.margin = 2 * self.tile_size_2d
        
    def convert_to_screen_position(self, position):
        return (int(self.tile_size_2d * (position[0] - self.left_edge)), int(self.tile_size_2d * (position[1] - self.top_edge)))
        
    def is_in_camera_fov(self, screen_position):
        is_visible_left = screen_position[0] > - self.margin
        is_visible_right = screen_position[0] < settings.screen_width + self.margin
        is_visible_top = screen_position[1] > - self.margin
        is_visible_bottom = screen_position[1] < settings.screen_height + self.margin
        return is_visible_left and is_visible_right and is_visible_bottom and is_visible_top
        
    def update(self):
        self.position = self.game.player.position
        self.x = self.position[0]
        self.y = self.position[1]
        self.left_edge = self.x - self.fov_half_width
        self.top_edge = self.y - self.fov_half_height
        
    def render_walls(self):
        for wall in self.game.map.walls_dict:
            screen_position = self.convert_to_screen_position((wall[0], wall[1]))
            if self.is_in_camera_fov(screen_position):
                pg.draw.rect(self.game.screen,
                             "darkgray",
                             (screen_position[0], screen_position[1],
                              self.tile_size_2d, self.tile_size_2d),
                             width = settings.wall_line_width)
    
    def render_dead_agent(self, screen_position, color, size):
        pg.draw.line(self.game.screen, color,
                     (screen_position[0] - size * self.tile_size_2d,
                      screen_position[1] - size * self.tile_size_2d),
                     (screen_position[0] + size * self.tile_size_2d,
                      screen_position[1] + size * self.tile_size_2d),
                     settings.dead_agent_line_width)
        pg.draw.line(self.game.screen, color,
                     (screen_position[0] - size * self.tile_size_2d,
                      screen_position[1] + size * self.tile_size_2d),
                     (screen_position[0] + size * self.tile_size_2d,
                      screen_position[1] - size * self.tile_size_2d),
                     settings.dead_agent_line_width)
            
    def render_player(self, player):
        screen_position = self.convert_to_screen_position((player.x, player.y))
        if player.alive:
            pg.draw.line(self.game.screen, player.color,
                         screen_position,
                         (screen_position[0] + settings.screen_width * math.cos(player.angle),
                          screen_position[1] + settings.screen_width * math.sin(player.angle)),
                         2)
            pg.draw.circle(self.game.screen, player.color,
                           screen_position,
                           int(player.size * self.tile_size_2d))
        else:
            self.render_dead_agent(screen_position, player.color, player.size)
        
    def render_enemy(self, enemy):
        screen_position = self.convert_to_screen_position((enemy.x, enemy.y))
        if enemy.alive:
            pg.draw.circle(self.game.screen, enemy.color,
                           screen_position,
                           int(enemy.size * self.tile_size_2d))
        else:
            self.render_dead_agent(screen_position, enemy.color, enemy.size)
                
    def render_item(self, item):
        screen_position = self.convert_to_screen_position((item.x, item.y))
        size = int(self.tile_size_2d * item.size)
        pg.draw.rect(self.game.screen, item.color, pg.Rect(screen_position[0] - size //2, screen_position[1] - size //2,
                                                           size, size))
                
    def render_scene(self):
        self.game.screen.fill('black')
        self.render_walls()
        self.render_player(self.game.player)
        for enemy in self.game.enemy_handler.enemy_list:
            self.render_enemy(enemy)
        for enemy in self.game.enemy_handler.dead_enemy_list:
            self.render_enemy(enemy)
        for item in self.game.enemy_handler.item_list:
            self.render_item(item)
        