import pygame as pg
import math
import random
from agent import *
from raycasting import *

class Enemy(SpriteAgent):
    def __init__(self, game,
                 enemy_id,
                 starting_pos,
                 enemy_speed,
                 starting_health,
                 damage,
                 min_range, max_range,
                 accuracy,
                 range_boost,
                 attack_speed,
                 max_seach_distance,
                 size, # TODO: Make this automatically synced with the sprite!
                 color,
                 default_image_path,
                 animation_time,
                 height,
                 eyeline_ratio):
            super().__init__(game,
                             starting_pos,
                             enemy_speed,
                             starting_health,
                             size,
                             color,
                             default_image_path,
                             animation_time,
                             height,
                             eyeline_ratio)
            self.damage = damage
            self.range = random.uniform(min_range, max_range)
            self.accuracy = accuracy
            self.range_boost = range_boost
            self.attack_speed = attack_speed
            self.last_attack = pg.time.get_ticks()
            self.enemy_id = enemy_id
            
            self.search_mode = False
            self.max_search_distance = max_seach_distance
            
            self.player_in_los = False
            self.hit_by_player = False
            self.distance_to_player = 0
            self.angle_to_player = 0
            
            self.attack_images = self.get_images(self.main_folder + '/attack')
            self.death_images = self.get_images(self.main_folder + '/death')
            # self.idle_images = self.get_images(self.main_folder + '/idle')
            self.pain_images = self.get_images(self.main_folder + '/pain')
            self.walk_images = self.get_images(self.main_folder + '/walk')

            self.death_animation_counter = 0
            self.n_death_images = len(self.death_images)
            
            self.in_pain = False
            self.pain_animation_counter = 0
            self.n_pain_images = len(self.pain_images)
            # print('Log: Spawned Enemy at (%2.1f, %2.1f)' % (self.x, self.y))
    
    # update
    def update_relation_to_player(self, player):
        self.angle_to_player = math.atan2(player.y - self.y, player.x - self.x) % math.tau
        self.distance_to_player = math.sqrt((player.y - self.y) ** 2 + (player.x - self.x) ** 2)
        
        # LoS
        raycast_result = RayCaster(self.game, self.position, self.angle_to_player, False)
        if raycast_result.depth < self.distance_to_player:
            self.player_in_los = False
            # print('Log: Lost LoS to player!')
        else:
            self.player_in_los = True
            # print('Log: Spotted player!')
            
    def did_attack_hit(self, weapon, player):
        # print("Log: Checking if attack hit enemy %1d." % self.enemy_id)
        max_angle_delta = math.atan2(self.size, self.distance_to_player) + weapon.angle_tolerance
        angle_to_player_rev = (math.pi + self.angle_to_player) % math.tau
        
#         print("  Log: Distance to player = %4.3f" % self.distance_to_player)
#         print("  Log: Weapon max range = %4.3f" % weapon.max_range)
#         print("  Log: Angle to player = %4.3f" % self.angle_to_player)
#         print("  Log: Angle to player reversed = %4.3f" % angle_to_player_rev)
#         print("  Log: Player angle = %4.3f" % self.game.player.angle)
#         print("  Log: max_angle_delta = %4.3f" % max_angle_delta)
        
        if abs(player.angle - angle_to_player_rev) < max_angle_delta and self.player_in_los and self.distance_to_player < weapon.max_range:
            # print("  Log: Attack hit enemy %1d." % self.enemy_id)
            self.hit_by_player = True
            self.in_pain = True
            
    def take_damage(self, weapon):      
        self.health -= weapon.damage
        self.hit_by_player = False
        if self.alive:
            self.game.sound.enemy_pain.play()
        else:
            self.game.sound.enemy_death.play()
        # print("Log: enemy %1d took %2d damage, current health is %2d." % (self.enemy_id, weapon.damage, self.health))
        
    def attack(self, player):
        if pg.time.get_ticks() - self.last_attack > self.attack_speed:
            self.last_attack = pg.time.get_ticks()
            self.game.sound.enemy_attack.play()
            range_boost = self.range_boost * (1 - self.distance_to_player / self.range)
            if random.random() < self.accuracy + range_boost:
                player.damage_list.append(self.damage)
                # print("Log: enemy %1d did %2d damage to player." % (self.enemy_id, self.damage))
            
    def move_toward_player(self):
#         print("    Log: move toward player:")
#         print("    Log: angle to player = %4.3f" % self.angle_to_player)
#         print("    Log: speed = %4.3f" % self.speed)
#         print("    Log: delta time = %4.3f" % self.game.delta_time)
        self.dy = math.sin(self.angle_to_player) * self.speed * self.game.delta_time
        self.dx = math.cos(self.angle_to_player) * self.speed * self.game.delta_time
            
    def halt(self):
        self.dx = 0
        self.dy = 0
        
    def search_for_player(self):
        if self.distance_to_player < self.max_search_distance:
#             print("Log: Enemy %1d searching for player" % self.enemy_id)
#             print("  Enemy position = (%3.2f, %3.2f)" % (self.x, self.y))
#             print("  Start tile = (%2d, %2d)" % self.map_position)
#             print("  Goal = (%2d, %2d)" % self.game.player.map_position)
            target_tile = self.game.pathfinding.find_next_step(self.map_position, self.game.player.map_position)
#             print("  Target tile = (%2d, %2d)" % target_tile)
            direction = math.atan2((target_tile[1] + 0.5) - self.y, (target_tile[0] + 0.5) - self.x)
            self.dx = math.cos(direction) * self.speed * self.game.delta_time
            self.dy = math.sin(direction) * self.speed * self.game.delta_time
        else:
            self.halt()
            self.search_mode = False
            
    def enemy_death(self):
#         if self.death_animation_counter == 0:
#             self.game.player.multi_kill += 1
        self.halt()
        super().update([], 0.5)
        
        if self.animation_trigger and self.death_animation_counter < self.n_death_images:
            # print("Log: enemy %2d died, frame %2d playing" % (self.enemy_id, self.death_animation_counter))
            # print("Log: screen_x = %4.3f" % self.screen_x_3d)
            self.change_sprite(self.death_images)
            self.death_animation_counter += 1
            
    def animate_pain(self):
        if self.in_pain:
            super().update([])
            if self.animation_trigger and self.pain_animation_counter < self.n_pain_images:
                self.change_sprite(self.pain_images)
                self.pain_animation_counter += 1
                if self.pain_animation_counter == self.n_pain_images:
                    self.pain_animation_counter = 0
                    self.in_pain = False
            
    def update(self):
        if self.alive and not settings.enemies_inactive:
#             print("Log: updating enemy %1d" % self.enemy_id)
#             print("  enemy position = (%2d, %2d)" % (self.x, self.y))
            self.update_relation_to_player(self.game.player)
            
            if self.in_pain:
                self.halt()
                if self.hit_by_player:
                    self.take_damage(self.game.player.weapon)
                self.animate_pain()
            
            elif self.player_in_los:
#                 print("  Player in LoS: enemy position = (%2d, %2d)" % (self.x, self.y))
                self.search_mode = True
                if self.distance_to_player < self.range:
                    # print("  Player in range: enemy position = (%2d, %2d)" % (self.x, self.y))
                    self.halt()
                    self.change_sprite(self.attack_images)
                    self.attack(self.game.player)
                else:
                    # print("  Player not in range: enemy position = (%2d, %2d)" % (self.x, self.y))
                    self.change_sprite(self.walk_images)
                    self.move_toward_player()
                # print("  Enemy speed = (%3.2f, %3.2f)" % (self.dx, self.dy))
            else:
                # print("  Player not in LoS: enemy position = (%2d, %2d)" % (self.x, self.y))
                if self.search_mode:
                    self.search_for_player()
            # print("  enemy position before super.update = (%2d, %2d)" % (self.x, self.y))
            
            agent_list = [ enemy for enemy in self.game.enemy_handler.enemy_list if enemy.enemy_id != self.enemy_id ]
            agent_list.append(self.game.player)
            super().update(agent_list)
            # print("  enemy position after super.update = (%2d, %2d)" % (self.x, self.y))
        
    # drawing    
    def drawIn2d(self):    
        if self.alive:
            pg.draw.circle(self.game.screen, self.color,
                           (self.screen_x_2d,
                            self.screen_y_2d),
                           int(self.size * self.game.map.tile_size_2d))
        else:
            dead_enemy_line_width = 4 # TODO: Should fix this
            pg.draw.line(self.game.screen, self.color,
                         (self.screen_x_2d - self.size * self.game.map.tile_size_2d,
                          self.screen_y_2d - self.size * self.game.map.tile_size_2d),
                         (self.screen_x_2d + self.size * self.game.map.tile_size_2d,
                          self.screen_y_2d + self.size * self.game.map.tile_size_2d),
                         dead_enemy_line_width)
            pg.draw.line(self.game.screen, self.color,
                         (self.screen_x_2d - self.size * self.game.map.tile_size_2d,
                          self.screen_y_2d + self.size * self.game.map.tile_size_2d),
                         (self.screen_x_2d + self.size * self.game.map.tile_size_2d,
                          self.screen_y_2d - self.size * self.game.map.tile_size_2d),
                         dead_enemy_line_width)
                         
    
class Soldier(Enemy):
    def __init__(self, game,
                 enemy_id,
                 starting_pos,
                 soldier_speed = 0.003,
                 starting_health = 50,
                 damage = 10,
                 min_range = 3,
                 max_range = 5,
                 accuracy = 0.2,
                 range_boost = 0.2,
                 attack_speed = 500,
                 max_seach_distance = 10,
                 size = 0.2,
                 color = 'red',
                 default_image_path = "resources/sprites/soldier",
                 animation_time = 120,
                 height = 0.6,
                 eyeline_ratio = 0.9):
        super().__init__(game,
                         enemy_id,
                         starting_pos,
                         soldier_speed,
                         starting_health,
                         damage,
                         min_range,
                         max_range,
                         accuracy,
                         range_boost,
                         attack_speed,
                         max_seach_distance,
                         size,
                         color,
                         default_image_path,
                         animation_time,
                         height,
                         eyeline_ratio)
        # print('Log: Spawned Soldier %1d at (%2d, %2d)' % (self.enemy_id, self.x, self.y))

class Boss(Enemy):
    def __init__(self, game,
                 enemy_id,
                 starting_pos,
                 soldier_speed = 0.003,
                 starting_health = 200,
                 damage = 20,
                 min_range = 3,
                 max_range = 5,
                 accuracy = 0.3,
                 range_boost = 0.3,
                 attack_speed = 500,
                 max_seach_distance = 10,
                 size = 0.2,
                 color = 'orange',
                 default_image_path = "resources/sprites/boss",
                 animation_time = 120,
                 height = 0.6,
                 eyeline_ratio = 0.9):
        super().__init__(game,
                         enemy_id,
                         starting_pos,
                         soldier_speed,
                         starting_health,
                         damage,
                         min_range,
                         max_range,
                         accuracy,
                         range_boost,
                         attack_speed,
                         max_seach_distance,
                         size,
                         color,
                         default_image_path,
                         animation_time,
                         height,
                         eyeline_ratio)
        # print('Log: Spawned Boss %1d at (%2d, %2d)' % (self.enemy_id, self.x, self.y))

    def take_damage(self, weapon):
        if weapon.weapon_type == "blade":
            self.health -= weapon.damage // 4
        else:
            self.health -= weapon.damage
        self.hit_by_player = False
        if self.alive:
            self.game.sound.enemy_pain.play()
        else:
            self.game.sound.enemy_death.play()