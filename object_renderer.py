import pygame as pg
import settings
from raycasting import *

class ObjectRenderer():
    def __init__(self, game):
        self.game = game
        self.wall_textures = self.load_wall_textures()
        
        self.n_rays = settings.screen_width // 2
        self.half_n_rays = self.n_rays // 2
        self.delta_angle = settings.field_of_view / self.n_rays
        self.scale = settings.screen_width // self.n_rays
        
        # walls
        self.wall_pieces = []
        # sky
        self.sky_image = self.get_texture('resources/textures/sky.png', (settings.screen_width, settings.screen_half_height + settings.max_vertical_offset))
        self.sky_offset = 0
        
        self.objects_to_render = []
        
    # Walls
    def get_wall_pieces_to_render(self):
        self.wall_pieces = []
        player_position = (self.game.player.x, self.game.player.y)
        
        ray_angle = self.game.player.angle - settings.half_field_of_view + 0.00001 # to avoid div by 0 errors?
        for ray in range(self.n_rays):
            self.wall_pieces.append(RayCaster(self.game, player_position, ray_angle, True))
            ray_angle += self.delta_angle
            
    def render_walls_3d_simple(self):
        self.get_wall_pieces_to_render()
        for index, wall_piece in enumerate(self.wall_pieces):
            color = [255 / (1 + 0.0002 * wall_piece.depth ** 5)] * 3
            pg.draw.rect(self.game.screen, color,
                         (index * self.scale,
                          settings.screen_half_height - wall_piece.projection_height // 2,
                          self.scale,
                          wall_piece.projection_height))
            
    def render_walls_3d_textured(self, vertical_offset):
        self.get_wall_pieces_to_render()
        for index, wall_piece in enumerate(self.wall_pieces):
            
            if wall_piece.projection_height < settings.screen_height:
                wall_column = self.wall_textures[wall_piece.texture].subsurface(
                        wall_piece.image_offset * (settings.texture_size - self.scale),
                        0,
                        self.scale,
                        settings.texture_size 
                    )
                wall_column = pg.transform.scale(wall_column, (self.scale, wall_piece.projection_height))
                wall_position = (index * self.scale,
                                 settings.screen_half_height - wall_piece.projection_height // 2 + vertical_offset)
            else:
                texture_height_visible_max = int(settings.texture_size * settings.screen_height / wall_piece.projection_height)
                vertical_offset_in_texture = int(wall_piece.depth / settings.screen_dist * vertical_offset * settings.texture_size)
                texture_top = max(0, settings.half_texture_size - texture_height_visible_max // 2 - vertical_offset_in_texture)
                texture_height = min(settings.texture_size - texture_top, settings.half_texture_size + texture_height_visible_max // 2 - vertical_offset_in_texture)
                
                wall_column = self.wall_textures[wall_piece.texture].subsurface(
                        wall_piece.image_offset * (settings.texture_size - self.scale),
                        texture_top,
                        self.scale,
                        texture_height
                    )
                wall_column = pg.transform.scale(wall_column, (self.scale, settings.screen_height * texture_height / texture_height_visible_max))
                if vertical_offset > 0 and texture_top == 0:
                    close_offset = int(settings.screen_height * (1 - texture_height / texture_height_visible_max))
                else:
                    close_offset = 0
                wall_position = (index * self.scale, close_offset)
                
            self.objects_to_render.append((wall_piece.depth, wall_column, wall_position))
          
    # Background
    def draw_background(self, vertical_offset):
        # sky
        self.sky_offset = (self.sky_offset + 4.0 * self.game.player.rotation) % settings.screen_width
        self.game.screen.blit(self.sky_image, (-self.sky_offset,
                                               vertical_offset - settings.max_vertical_offset))
        self.game.screen.blit(self.sky_image, (-self.sky_offset + settings.screen_width,
                                               vertical_offset - settings.max_vertical_offset))
        # floor
        floor_color = (30, 30, 30)
        pg.draw.rect(self.game.screen, floor_color, (0, settings.screen_half_height + vertical_offset,
                                                     settings.screen_width, settings.screen_height))
            
    # Sprites
    def render_enemies(self):
        for enemy in self.game.enemy_handler.enemy_list:
            sprite_rendering_info = enemy.put_sprite_on_screen(self.game.player)
            # print("Log: added enemy at depth %4.3f," % sprite_rendering_info[0])
            # print("     and position (%4.3f, %4.3f)." % sprite_rendering_info[2])
            if not (sprite_rendering_info is None):
                self.objects_to_render.append(sprite_rendering_info)
        for enemy in self.game.enemy_handler.dead_enemy_list:
            sprite_rendering_info = enemy.put_sprite_on_screen(self.game.player)
            # print("Log: added enemy at depth %4.3f," % sprite_rendering_info[0])
            # print("     and position (%4.3f, %4.3f)." % sprite_rendering_info[2])
            if not (sprite_rendering_info is None):
                self.objects_to_render.append(sprite_rendering_info)
    
    def render_3d(self):
        print("Log: vertical offset = %i" % self.game.player.vertical_offset)
        
        self.draw_background(self.game.player.vertical_offset)
        
        self.objects_to_render = []
        self.render_walls_3d_textured(self.game.player.vertical_offset)
        # print("Log: %3d objects to render" % len(self.objects_to_render))
        self.render_enemies()
        
        # Sort objects to render by distance starting from last
        ordered_list = sorted(self.objects_to_render, key = lambda t: t[0], reverse = True)
        # ordered_list.append((0, self.game.shotgun.images[0], self.game.shotgun.position_on_screen))
        ordered_list.append((0, self.game.player.weapon.images[0], self.game.player.weapon.position_on_screen))
        for depth, image, position in ordered_list:
            self.game.screen.blit(image, position)
            
        # if self.game.game_over:
#         if self.game.player.alive:
#             game_over_text = self.game.font.render("You won!", False, "green")
#         else:
#             game_over_text = self.game.font.render("You lose!", False, "red")
#         # print("I'm here")
#         self.game.screen.blit(game_over_text,
#                               (settings.screen_half_width - game_over_text.get_width() // 2,
#                                settings.screen_half_height - game_over_text.get_height() // 2))
        # print("I'm here 2")
            
    def draw_field_of_view_2d(self):
        self.get_wall_pieces_to_render()
        for wall_piece in self.wall_pieces:
            end_coord_x = self.game.player.x + (wall_piece.depth * math.cos(wall_piece.angle))
            end_coord_y = self.game.player.y + (wall_piece.depth * math.sin(wall_piece.angle))
            
            end_coord_screen_x = self.game.map.offset_x + end_coord_x * self.game.map.tile_size_2d
            end_coord_screen_y = self.game.map.offset_y + end_coord_y * self.game.map.tile_size_2d
            pg.draw.line(self.game.screen, 'yellow',
                         (self.game.player.screen_x_2d, self.game.player.screen_y_2d),
                         (end_coord_screen_x, end_coord_screen_y),
                         2)

    @staticmethod
    def get_texture(path, res = (settings.texture_size, settings.texture_size)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/wall/1.png'),
            2: self.get_texture('resources/textures/wall/2.png'),
            3: self.get_texture('resources/textures/wall/3.png'),
            4: self.get_texture('resources/textures/wall/4.png'),
            5: self.get_texture('resources/textures/wall/5.png'),
        }