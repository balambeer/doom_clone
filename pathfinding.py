from collections import deque

class PathFinding:
    def __init__(self, game):
        self.game = game
        self.map = game.map.mini_map
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
        self.graph = {}
        
        self.get_graph()
        
    def build_bfs_graph(self, start, goal):
        bfs_graph = { start: None }
        nodes_to_check = deque([start])
        
        enemy_map_positions = [ enemy.map_position for enemy in self.game.enemy_handler.enemy_list ]
        if goal in enemy_map_positions:
            enemy_map_positions.remove(goal)
        
        while nodes_to_check:
            current_node = nodes_to_check.popleft()
            
            if current_node == goal:
                break
            
            negihbor_list = self.graph[current_node]
            for neighbor in negihbor_list:
                if neighbor not in bfs_graph and neighbor not in enemy_map_positions:
                    nodes_to_check.append(neighbor)
                    bfs_graph[ neighbor ] = current_node
                    
#         print("Log: built bfs graph:")
#         print(start, goal)
#         print(bfs_graph)
        return bfs_graph
                
    def find_next_step(self, start, goal):
        bfs_graph = self.build_bfs_graph(start, goal)
        if goal in bfs_graph:
            path = [ goal ]
            step = bfs_graph[goal]
            
            while step and step != start:
                path.append(step)
                step = bfs_graph[step]
                
    #         print("Log: path found:")
    #         print(path)
            return path[-1]
        else:
            return start
        
    def get_neighbors(self, x, y):
        return [ (x + dx, y + dy) for dx, dy in self.directions if (x + dx, y + dy) not in self.game.map.walls_dict ]
        
    def get_graph(self):
        for row_index, row in enumerate(self.map):
            for col_index, element in enumerate(row):
                if (col_index, row_index) not in self.game.map.walls_dict:
                    # The indexes are switched, because on the screen the x-coordinate is the column of the map
                    self.graph[(col_index, row_index)] = self.get_neighbors(col_index, row_index)
                    
        # print("Log: processed graph:")
        # print(self.graph)
                    