import pygame as pg
import math
import settings
from agent import *

class Player(Agent):
    def __init__(self, game,
                 starting_pos,
                 starting_angle,
                 player_speed,
                 starting_health,
                 size,
                 color,
                 starting_weapon):
        super().__init__(game, starting_pos, player_speed, starting_health, size, color)
        self.angle = starting_angle
        self.vertical_angle = 0
        self.vertical_offsett = 0
        self.weapon = starting_weapon
        self.damage_list = []
        
        self.rotation = 0 # for mouse-control in 3d-mode
        
        self.multi_kill = 0
        
        self.health_hud = self.game.font.render('%3d' % self.health, False, settings.health_hud_color)

        # print('Log: Spawned Player at position (%2.1f, %2.1f).' % (self.x, self.y))
        
    # movement controls
    def movement2d(self):
        self.dx, self.dy = 0, 0
        
        displacement = self.speed * self.game.delta_time
        # print('Log: speed = %4.3f' % speed)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.dy -= displacement
        if keys[pg.K_s]:
            self.dy += displacement
        if keys[pg.K_a]:
            self.dx -= displacement
        if keys[pg.K_d]:
            self.dx += displacement
           
        mx, my = pg.mouse.get_pos()
        # print('Log: mouse position = %4.3f, %4.3f' % (mx, my))
        self.angle = math.atan2(my - self.screen_y_2d,  mx - self.screen_x_2d) % math.tau
            
        # print('Log: player dx, dy = %4.3f, %4.3f' % (self.dx, self.dy))
        
    def movement3d(self):
        self.dx, self.dy = 0, 0
        
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)        
        displacement = self.speed * self.game.delta_time
        
        # print('Log: speed = %4.3f' % speed)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.dx += displacement * cos_a
            self.dy += displacement * sin_a
        if keys[pg.K_s]:
            self.dx -= displacement * cos_a
            self.dy -= displacement * sin_a
        if keys[pg.K_a]:
            self.dx += displacement * sin_a
            self.dy -= displacement * cos_a
        if keys[pg.K_d]:
            self.dx -= displacement * sin_a
            self.dy += displacement * cos_a
           
        mx, my = pg.mouse.get_pos()
        # print('Log: mouse position = %4.3f, %4.3f' % (mx, my))
        if mx < settings.mouse_border_left or mx > settings.mouse_border_right:
            pg.mouse.set_pos([settings.screen_half_width, settings.screen_half_height])
        if my > settings.mouse_border_bottom or my < settings.mouse_border_top:
            pg.mouse.set_pos([settings.screen_half_width, settings.screen_half_height])
        mouse_movement = pg.mouse.get_rel()
        self.rotation = max(-settings.mouse_max_rotation, min(settings.mouse_max_rotation, mouse_movement[0]))
        self.angle += self.rotation * settings.mouse_sensitivity * self.game.delta_time
        self.vertical_angle += -mouse_movement[1] * settings.mouse_sensitivity

        self.angle = self.angle % math.tau
        self.vertical_angle = max(-settings.player_vertical_angle_limit,
                                  min(settings.player_vertical_angle_limit,
                                      self.vertical_angle))
        print("Log: player angle vert = %.3f" % self.vertical_angle)
        
        self.vertical_offset = int(settings.screen_dist * math.tan(self.vertical_angle))
        
    def listen_to_weapon(self):
        left_button_pressed = pg.mouse.get_pressed()[0]
        if left_button_pressed and self.weapon.ready_to_use:
            # print("Log: weapon attacked")
            self.weapon.attacked = True
        # Change weapon
        keys = pg.key.get_pressed()
        if keys[pg.K_1]:
            self.weapon = self.game.sword
        if keys[pg.K_2]:
            self.weapon = self.game.shotgun
        
    def take_damage(self):
        for damage in self.damage_list:
            self.game.sound.player_pain.play()
            self.health -= damage
            self.damage_list.remove(damage)
            # print("Log: player took %2d damage, health = %.3d" % (damage, self.health))
        
    def health_boost(self):
        if self.multi_kill > 0:
            self.health += 10 * (2 ** (self.multi_kill - 1))
            self.multi_kill = 0
        
    # update
    def update(self):
        if self.alive:
            if self.game.game_mode_2d:
                self.movement2d()
            else:
                self.movement3d()
            self.take_damage()
            self.listen_to_weapon()
            self.weapon.update()
            self.health_boost()
            self.health_hud = self.game.font.render('%3d' % self.health, False, settings.health_hud_color)
            super().update(self.game.enemy_handler.enemy_list)
        
    # drawing    
    def drawIn2d(self):
        if self.alive:
            pg.draw.line(self.game.screen, self.color,
                         (self.screen_x_2d,
                          self.screen_y_2d),
                         (self.screen_x_2d + settings.screen_width * math.cos(self.angle),
                          self.screen_y_2d + settings.screen_width * math.sin(self.angle)),
                         2)
            pg.draw.circle(self.game.screen, self.color,
                           (self.screen_x_2d,
                            self.screen_y_2d),
                           int(self.size * self.game.map.tile_size_2d))
        else:
            dead_player_line_width = 4 # TODO: Should fix this
            pg.draw.line(self.game.screen, self.color,
                         (self.screen_x_2d - self.size * self.game.map.tile_size_2d,
                          self.screen_y_2d - self.size * self.game.map.tile_size_2d),
                         (self.screen_x_2d + self.size * self.game.map.tile_size_2d,
                          self.screen_y_2d + self.size * self.game.map.tile_size_2d),
                         dead_player_line_width)
            pg.draw.line(self.game.screen, self.color,
                         (self.screen_x_2d - self.size * self.game.map.tile_size_2d,
                          self.screen_y_2d + self.size * self.game.map.tile_size_2d),
                         (self.screen_x_2d + self.size * self.game.map.tile_size_2d,
                          self.screen_y_2d - self.size * self.game.map.tile_size_2d),
                         dead_player_line_width)
