import random
from pipe import *

class RandomMap:
    def __init__(self,
                 room_block_rows,
                 room_block_cols,
                 room_block_width,
                 room_block_height,
                 n_wall_textures,
                 decorator_density):
        self.room_block_rows = room_block_rows
        self.room_block_cols = room_block_cols
        self.n_room_blocks = room_block_rows * room_block_cols
#         print("Log: n_room_blocks = %i" % self.n_room_blocks)
        
        self.room_block_width = room_block_width
        self.room_block_height = room_block_height
        
        self.n_rows = room_block_rows * room_block_height
        self.n_cols = room_block_cols * room_block_width
        
        self.decorator_density = decorator_density
        
        self.room_block_midpoints = self.get_midpoints()
#         print("Log: room_block_midpoints:")
        print(self.room_block_midpoints)
        
        self.n_anchor_points = random.randint(self.n_room_blocks - 1, self.n_room_blocks + 1)
        self.row_half_range = self.room_block_height // 4
        self.col_half_range = self.room_block_width // 4
#         print("Log: n_anchor_points = %i" % self.n_anchor_points)
        self.anchor_point_list = self.create_anchor_points(self.row_half_range,
                                                           self.col_half_range)
        
        self.n_wall_textures = n_wall_textures
        self.texture_list = [ random.randint(1, self.n_wall_textures) for i in range(self.n_anchor_points) ]
#         print("Log: anchor_point_list:")
#         print(self.anchor_point_list)
#         print("Log: texture_list:")
#         print(self.texture_list)

        self.rooms = []
        self.corridors = []
        self.decorators_no_go = []
 
        self.generated_map = []
        self.generate_map()
        
        print("Log: room layout:")
        print(self.rooms)
        print(self.corridors)
        
        print('Log: Generated random map:')
        for row in self.generated_map:
            print(row)
        
    # Empty map
    def generate_empty_map(self):
        self.generated_map = [ [ 0 for i in range(self.n_cols) ] for j in range(self.n_rows) ]
        
    # Wall textures
    def get_midpoints(self):
        midpoints = []
        
        for i in range(1, self.room_block_rows + 1):
            for j in range(1, self.room_block_cols + 1):
                midpoints.append((int(self.room_block_height / 2 + (i - 1) * self.room_block_height),
                                  int(self.room_block_width / 2 + (j - 1) * self.room_block_width) ))
        
        return midpoints
    
    def lp_distance(self, point_1, point_2, p = 2):
        return ((point_1[0] - point_2[0]) ** p + (point_1[1] - point_2[1]) ** p) ** (1/p)
    
    def find_closest_anchor_point(self, point):
        shortest_distance = self.lp_distance(point, self.anchor_point_list[0])
        texture_value = self.texture_list[0]
        
        for i in range(1, len(self.anchor_point_list)):
            current_distance = self.lp_distance(point, self.anchor_point_list[i])
            if current_distance < shortest_distance:
                shortest_distance = current_distance
                texture_value = self.texture_list[i]
                               
        return texture_value
    
    def create_anchor_points(self, row_half_range, col_half_range):
        anchor_point_list = []
        
        for i in range(self.n_anchor_points):
            room_block = self.room_block_midpoints[random.randint(0, self.n_room_blocks - 1)]
            anchor_point_list.append((random.randint(int(room_block[0] - row_half_range), int(room_block[0] + row_half_range)),
                                      random.randint(int(room_block[1] - col_half_range), int(room_block[1] + col_half_range))))
            
        return anchor_point_list
    
    def fill_with_wall_textures(self):
        for i in range(len(self.generated_map)):
            for j in range(len(self.generated_map[0])):
                self.generated_map[i][j] = self.find_closest_anchor_point((i, j))
    
    # Layout
    def sample_room_layout(self):
        
        midpoints_remaining = [ i for i in range(self.n_room_blocks) ]
        keep_sampling = True
        for i in range(self.n_room_blocks):
            if keep_sampling and (i < (self.n_room_blocks - 2) or random.random() < 0.5):
                chosen_index = midpoints_remaining[ random.randint(0, len(midpoints_remaining) - 1) ]
                self.rooms.append(self.room_block_midpoints[chosen_index])
                midpoints_remaining.remove(chosen_index)
                
                room_connected = False
                if i > 0:
                    for j in range(1, i):
                        if random.random() < 0.5:
                            self.corridors.append((self.rooms[j], self.rooms[i]))
                            room_connected = True
                    if not room_connected:
                        self.corridors.append((self.rooms[random.randint(0, i - 1)], self.rooms[i]))
            else:
                keep_sampling = False
          
    # Carve rooms
    def carve_single_room(self, room_block_midpoint):
        room_height = random.randint(self.room_block_height // 2, self.room_block_height - 2)
        room_width = random.randint(self.room_block_width // 2, self.room_block_width - 2)
        
        midpoint_ratio = (random.random(), random.random())
        
        room_topleft = (room_block_midpoint[0] - int(midpoint_ratio[0] * room_height),
                        room_block_midpoint[1] - int(midpoint_ratio[1] * room_width))
        
        for i in range(max(1, room_topleft[0]), min(self.n_rows - 2, room_topleft[0] + room_height + 1)):
            for j in range(max(1, room_topleft[1]), min(self.n_cols - 2, room_topleft[1] + room_width + 1)):
                self.generated_map[i][j] = 0
    
    def carve_rooms(self):
        for room in self.rooms:
            self.carve_single_room(room)
            
    # Decorators
    def is_decorator_allowed(self, position):
        allowed = True
        for pos in self.decorators_no_go:
            if position == pos:
                allowed = False
                break
        
        return allowed
    
    def append_no_go_points(self, position):
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbor_position = (position[0] + i, position[1] + j)
                if self.is_decorator_allowed(neighbor_position):
                    self.decorators_no_go.append(neighbor_position)
                    
    def add_decorators(self):
        n_decorators = int(self.decorator_density * self.n_rows * self.n_cols)
        
        for i in range(n_decorators):
            decorator_orientation = random.randint(0, 1)
            decorator_size = random.randint(1, 3)
            decorator_texture = random.randint(1, self.n_wall_textures)
            
            decorator_position = (random.randint(0, self.n_rows - 1), random.randint(0, self.n_cols - 1))
            
            if decorator_orientation == 0:
                for i in range(max(0, decorator_position[0] - decorator_size), decorator_position[0]):
                    if self.is_decorator_allowed((i, decorator_position[1])):
                        self.generated_map[i][decorator_position[1]] = decorator_texture
                for i in range(max(0, decorator_position[0] - decorator_size), decorator_position[0]):
                    self.append_no_go_points((i, decorator_position[1]))
            else:
                for j in range(max(0, decorator_position[1] - decorator_size), decorator_position[1]):
                    if self.is_decorator_allowed((decorator_position[0], j)):
                        self.generated_map[decorator_position[0]][j] = decorator_texture
                for j in range(max(0, decorator_position[1] - decorator_size), decorator_position[1]):
                    self.append_no_go_points((decorator_position[0], j))
    
    # Corridors
    def carve_single_corridor(self, corridor):
        start_point = corridor[0]
        end_point = corridor[1]
        
        if random.random() < 0.5:
            for i in range(start_point[0], end_point[0] + 1):
                self.generated_map[i][start_point[1]] = 0
            for j in range(start_point[1], end_point[1] + 1):
                self.generated_map[end_point[0]][j] = 0
        else:
            for j in range(start_point[1], end_point[1] + 1):
                self.generated_map[start_point[0]][j] = 0
            for i in range(start_point[0], end_point[0] + 1):
                self.generated_map[i][end_point[1]] = 0
                
    def carve_corridors(self):
        for corridor in self.corridors:
            self.carve_single_corridor(corridor)
    
    # Generator
    def generate_map(self):
        self.generate_empty_map()
        self.fill_with_wall_textures()
        self.sample_room_layout()
        self.carve_rooms()
        self.add_decorators()
        self.carve_corridors()