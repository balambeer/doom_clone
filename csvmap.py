import csv
import pygame as pg
import settings

class Map:
    def __init__(self, game,
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
        
        self.readLevelMap()
        self.get_walls_and_empty_spaces()

    def readLevelMap(self):
        mini_map = []
        with open(self.path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                mini_map.append(row)
        n_rows, n_cols = len(mini_map), len(mini_map[0])
        for i in range(n_rows):
            for j in range(n_cols):
                mini_map[i][j] = int(mini_map[i][j])
        
        self.mini_map = mini_map
        self.n_rows = n_rows
        self.n_cols = n_cols
        
        self.tile_size_2d = min(settings.screen_width // n_cols, settings.screen_height // n_rows)
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
