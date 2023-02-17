import pygame as pg
import math
import os
import settings
from collections import deque

class Agent:
    def __init__(self, game,
             starting_pos,
             agent_speed,
             starting_health,
             size,
             color):
        self.game = game
        self.x, self.y = starting_pos
        self.speed = agent_speed
        self.dx, self.dy = 0, 0
        self.size = size
        self.health = starting_health
        
        # for 2d display
        self.screen_x_2d = 0
        self.screen_y_2d = 0
        self.color = color
        self.convert_to_screen_position_2d()
        
        # print('Log: created Agent at position (%3d, %3d).' % (self.x, self.y))
        
    @property
    def alive(self):
        return self.health > 0
        
    def update(self, agent_list):
        self.truncate_movement(agent_list)
        self.x += self.dx
        self.y += self.dy
        if self.game.game_mode_2d:
            self.convert_to_screen_position_2d()
        
    def convert_to_screen_position_2d(self):
        self.screen_x_2d = self.game.map.offset_x + self.x * self.game.map.tile_size_2d
        self.screen_y_2d = self.game.map.offset_y + self.y * self.game.map.tile_size_2d
        
    # Not taking size into account
    def wall_collision(self, x, y):
        return (int(x), int(y)) in self.game.map.walls_dict
        
    # Taking size into account
    def wall_collision_with_size(self, x, y):
        wall_collision_left = self.wall_collision(x - self.size, y)
        wall_collision_right = self.wall_collision(x + self.size, y)
        wall_collision_up = self.wall_collision(x, y - self.size)
        wall_collision_down = self.wall_collision(x, y + self.size)
        return (wall_collision_left or wall_collision_right or wall_collision_up or wall_collision_down)
    
    def agent_collision(self, agent):
        projected_distance_to_agent = math.sqrt((self.x + self.dx - agent.x) ** 2 + (self.y + self.dy - agent.y) ** 2)
        return projected_distance_to_agent < self.size + agent.size
    
    def truncate_movement(self, agent_list):
        if self.wall_collision_with_size(self.x + self.dx, self.y):
            self.dx = 0
        if self.wall_collision_with_size(self.x, self.y + self.dy):
            self.dy = 0
        for agent in agent_list:
            if self.agent_collision(agent):
                self.dx = 0
                self.dy = 0
        
    @property
    def position(self):
        return self.x, self.y
     
    @property
    def map_position(self):
        return int(self.x), int(self.y)
        
class SpriteAgent(Agent):
    def __init__(self, game,
                 starting_pos,
                 agent_speed,
                 starting_health,
                 size,
                 color,
                 main_folder_path,
                 animation_time,
                 height,
                 eyeline_ratio):
        super().__init__(game, starting_pos, agent_speed, starting_health, size, color)
        self.main_folder = main_folder_path
        # self.current_animation_images = self.get_images(self.main_folder) # pg.image.load(default_image_path).convert_alpha()
        
        self.image = self.get_images(self.main_folder)[0]
        self.image_width = self.image.get_width()
        self.image_half_width = self.image_width // 2
        self.image_height = self.image.get_height()
        self.image_ratio = self.image_width / self.image_height
        # self.main_folder = default_image_path.rsplit('/', 1)[0]
        
        self.height = height
        self.eyeline_ratio = eyeline_ratio
        
        self.screen_x_3d = 0
        self.screen_y_3d = 0
        self.sprite_half_width = 0

        self.animation_time = animation_time
        self.prev_animation_time = pg.time.get_ticks()
        self.animation_trigger = False

    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images
    
    def put_sprite_on_screen(self, player):
        angle_from_player = math.atan2(self.y - player.y, self.x - player.x)
        angle_from_player_pov = (player.angle - angle_from_player) % math.tau
        if angle_from_player_pov > math.pi:
            angle_from_player_pov -= math.tau
        
        # print("Log: angle_from_player_pov = %4.3f" % angle_from_player_pov)

        if math.cos(angle_from_player_pov) >= 0:
            delta_rays = - angle_from_player_pov / self.game.object_renderer.delta_angle
            self.screen_x_3d = (self.game.object_renderer.half_n_rays + delta_rays) * self.game.object_renderer.scale
            
            # print("Log: delta_rays = %4.3f" % delta_rays)
            # print("Log: screen_x_3d = %4.3f" % self.screen_x_3d)
            
            distance = math.hypot(self.y - player.y, self.x - player.x)
            distance = distance * math.cos(angle_from_player_pov)
            # print("Log: distance = %4.3f" % distance)
            
            if -self.image_half_width < self.screen_x_3d < (settings.screen_width + self.image_half_width):
            
                projection_height = settings.screen_dist / distance * self.height
                projection_width = projection_height * self.image_ratio
                
                # print("Log: projection_width = %4.3f" % projection_width)
                # print("Log: projection_height = %4.3f" % projection_height)
                
                image = pg.transform.scale(self.image, (projection_width, projection_height))
                
                self.sprite_half_width = projection_width // 2
                height_shift = self.eyeline_ratio * projection_height
                position = (self.screen_x_3d - self.sprite_half_width,
                            settings.screen_half_height - projection_height + height_shift + player.vertical_offset)
            
                # print("Log: position = (%4.3f, %4.3f)" % position)
            
                return (distance, image, position)
        
    def change_sprite(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]
            self.prev_animation_time = pg.time.get_ticks()
            self.animation_trigger = False
        
    def check_animation_time(self, animation_speed_factor):
        if pg.time.get_ticks() - self.prev_animation_time > self.animation_time * animation_speed_factor:
            self.animation_trigger = True

    def update(self, agent_list, animation_speed_factor = 1):
        super().update(agent_list)
        if not self.animation_trigger:
            self.check_animation_time(animation_speed_factor)
        # self.put_sprite_on_screen(self.game.player)
