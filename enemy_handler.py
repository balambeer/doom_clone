import pygame as pg
import settings
import random
from enemy import *

class EnemyHandler:
    def __init__(self, game):
        self.game = game
        self.enemy_list = []
        self.dead_enemy_list = []
        
        self.get_enemies()
        
    def get_enemies(self):
        possible_locations = self.game.map.empty_spaces
        num_enemies = random.randint(max(1, int(settings.enemy_density * len(possible_locations)) - 1),
                                     int(settings.enemy_density * len(possible_locations)) + 1)
        # print(possible_locations)
        # possible_locations.remove((int(settings.player_starting_position[0]), int(settings.player_starting_position[1])))
        possible_locations.remove(self.game.player_starting_pos)
        
        for i in range(num_enemies):
            enemy_tile = random.choice(possible_locations)
            self.enemy_list.append(Soldier(self.game, enemy_id = i, starting_pos = (enemy_tile[0] + 0.5, enemy_tile[1] + 0.5)))
            possible_locations.remove(enemy_tile)
        
    def update(self):
        for enemy in self.enemy_list:
            enemy.update()
            if not enemy.alive:
                # print("Log: screen_x = %4.3f" % enemy.screen_x_3d)
                self.enemy_list.remove(enemy)
                self.dead_enemy_list.append(enemy)
                self.game.player.multi_kill += 1
                # print("Log: dead enemies:")
                # print(self.dead_enemy_list)
        for enemy in self.dead_enemy_list:
            enemy.enemy_death()
        
    def drawIn2d(self):
        for enemy in self.enemy_list:
            enemy.drawIn2d()
        for enemy in self.dead_enemy_list:
            enemy.drawIn2d()