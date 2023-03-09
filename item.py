import pygame as pg
import math
import settings

class Item():
    def __init__(self, game,
                 position,
                 quantity,
                 item_type,
                 size,
                 color,
                 image_path,
                 height,
                 eyeline_ratio):
        self.game = game
        self.item_type = item_type
        self.quantity = quantity
        
        self.x = position[0]
        self.y = position[1]
        self.size = size
        self.color = color
        
        self.image = pg.image.load(image_path).convert_alpha()
        self.image_width = self.image.get_width()
        self.image_half_width = self.image_width // 2
        self.image_height = self.image.get_height()
        self.image_ratio = self.image_width / self.image_height
        
        self.height = height
        self.eyeline_ratio = eyeline_ratio
        
        self.screen_x_2d = 0
        self.screen_y_2d = 0
        
        self.screen_x_3d = 0
        self.screen_y_3d = 0
        self.sprite_half_width = 0
        
    def picked_up(self, player):
        return math.hypot(self.y - player.y, self.x - player.x) < self.size + player.size
        
    # Code duplication from SpriteAgent
    # Would have done this differently if I knew that I also wanted static objects, but I won't refactor the code now...
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
    
    def convert_to_screen_position_2d(self):
        self.screen_x_2d = self.game.map.offset_x + self.x * self.game.map.tile_size_2d
        self.screen_y_2d = self.game.map.offset_y + self.y * self.game.map.tile_size_2d
    
    def drawIn2d(self):
        self.convert_to_screen_position_2d()
        size = int(self.game.map.tile_size_2d * self.size)
        pg.draw.rect(self.game.screen, self.color, pg.Rect(self.screen_x_2d - size //2, self.screen_y_2d - size //2,
                                                           size, size))
            
class Ammo(Item):
    def __init__(self, game,
                 position,
                 quantity,
                 item_type = "ammo",
                 size = 0.4,
                 color = "blue",
                 image_path = "resources/sprites/items/ammo.png",
                 height = 0.1,
                 eyeline_ratio = 4.5):
        super().__init__(game,
                         position,
                         quantity,
                         item_type,
                         size,
                         color,
                         image_path,
                         height,
                         eyeline_ratio)
        
class Shotgun(Item):
    def __init__(self, game,
                 position,
                 quantity = 1,
                 item_type = "shotgun",
                 size = 0.4,
                 color = "purple",
                 image_path = "resources/sprites/items/ammo.jpg",
                 height = 0.1,
                 eyeline_ratio = 0.5):
        super().__init__(game,
                         position,
                         quantity,
                         item_type,
                         size,
                         color,
                         image_path,
                         height,
                         eyeline_ratio)