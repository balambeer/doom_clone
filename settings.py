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
mouse_sensitivity = 0.0003
mouse_max_rotation = 40

# Player
player_starting_position = 1.5, 5
player_starting_angle = 0.3
player_speed = 0.004
player_starting_health = 100
player_size = 0.2
player_color = 'green'

# Enemies
enemy_count_min = 6
enemy_count_max = 8
enemies_inactive = False

# 3d rendering
field_of_view = math.pi / 3
half_field_of_view = field_of_view / 2
screen_dist = screen_half_width / math.tan(half_field_of_view)

# texturing
texture_size = 256
half_texture_size = texture_size // 2

# text
font_size = screen_height // 10
health_hud_color = "gray"
health_hud_offset = int(1.5 * font_size)
health_hud_position = (health_hud_offset, screen_height - health_hud_offset)