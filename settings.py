import math

# Game mode
game_mode_2d = False

# Screen
resolution = screen_width, screen_height = 1200, 650
screen_half_width = screen_width // 2
screen_half_height = screen_height // 2
fps = 60

# Mouse control in 3d
mouse_border_left = 100
mouse_border_right = screen_width - mouse_border_left
mouse_border_top = 100
mouse_border_bottom = screen_height - mouse_border_top
mouse_sensitivity = 0.0003
mouse_max_rotation = 40

# Player
player_vertical_angle_limit = 0.1
player_speed = 0.004
player_starting_health = 100
player_size = 0.2
player_color = 'green'

# Enemies
enemy_density = 0.1
enemies_inactive = False

# Items
item_spawn_prob = 0.5
ammo_quantity_min = 1
ammo_quantity_max = 3

# 2d rendering
camera_fov_width = 15 # measured in nr of map tiles that fit on screen horizontally
camera_fov_height = (screen_height / screen_width) * camera_fov_width
wall_line_width = 2
dead_agent_line_width = 4
use_camera = True

# 3d rendering
field_of_view = math.pi / 3
half_field_of_view = field_of_view / 2
screen_dist = screen_half_width / math.tan(half_field_of_view)

half_field_of_view_vert = math.atan2(screen_half_height, screen_dist)
max_vertical_offset = int(screen_dist * math.tan(player_vertical_angle_limit))

# texturing
texture_size = 256
half_texture_size = texture_size // 2

# text
font_size = screen_height // 10
health_hud_color = "firebrick3"
health_hud_offset = int(1.5 * font_size)
health_hud_position = (health_hud_offset, screen_height - health_hud_offset)
ammo_hud_color = "gray"
ammo_hud_offset = int(1.5 * font_size)
ammo_hud_position = (screen_width - 3 * ammo_hud_offset, screen_height - ammo_hud_offset)

# random map
room_block_rows = 2
room_block_cols = 3
room_block_width = 10
room_block_height = 10
n_wall_textures = 4
decorator_density = 0.04