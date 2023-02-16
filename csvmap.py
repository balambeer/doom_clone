import csv
import pygame as pg
import settings
from random_map import *

class Map:
    def __init__(self, game,
                 generate_random_map,
                 path = 'maps/tutorial.csv'):
        self.path = path
        self.game = game
        self.mini_map = []
        self.walls_dict = {}
        self.empty_spaces = []
        
        # for drawing
        self.n_rows = 0
        self.n_cols = 0
        self.tile_size_2d = 0
        self.offset_x = 0
        self.offset_y = 0
        
        if generate_random_map:
            self.generate_random_map()
        else:
            self.read_csv_map()
        self.process_mini_map()
        self.get_walls_and_empty_spaces()

    def read_csv_map(self):
        csv_map = []
        with open(self.path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                csv_map.append(row)
        
        n_rows = len(csv_map)
        n_cols = len(csv_map[0])
        for i in range(n_rows):
            for j in range(n_cols):
                csv_map[i][j] = int(csv_map[i][j])
        
        self.mini_map = csv_map
        
    def generate_random_map(self):
        random_map = RandomMap(settings.room_block_rows,
                               settings.room_block_cols,
                               settings.room_block_width,
                               settings.room_block_height,
                               settings.n_wall_textures,
                               settings.decorator_density)
        
        self.mini_map = random_map.generated_map
        
    def process_mini_map(self):
        self.n_rows = len(self.mini_map)
        self.n_cols = len(self.mini_map[0])
        
        self.tile_size_2d = min(settings.screen_width // self.n_cols, settings.screen_height // self.n_rows)
        self.offset_x = (settings.screen_width % self.tile_size_2d) // 2
        self.offset_y = (settings.screen_height % self.tile_size_2d) // 2
        
        print('Log: Processed mini map:')
        for row in self.mini_map:
            print(row)
        print('  Tile size 2d = %5d' % (self.tile_size_2d))
        print('  Offset x = %5d' % (self.offset_x))
        print('  Offset y = %5d' % (self.offset_y))
        
    def get_walls_and_empty_spaces(self):
        for row_index, row in enumerate(self.mini_map):
            for col_index, value in enumerate(row):
                if value > 0:
                    self.walls_dict[(col_index, row_index)] = value
                else:
                    self.empty_spaces.append((col_index, row_index))
                    
        print('Log: Processed walls dictionary:')
        print(self.walls_dict)

    def drawIn2d(self):
        [
            pg.draw.rect(self.game.screen,
                         'darkgray',
                         (self.offset_x + wall[0] * self.tile_size_2d,
                          self.offset_y + wall[1] * self.tile_size_2d,
                          self.tile_size_2d, self.tile_size_2d),
                         width = 2)
            for wall in self.walls_dict
        ]
