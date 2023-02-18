import sys
import pygame as pg
import random
import settings
from csvmap import *
from player import *
from enemy_handler import *
from weapon import *
from sound import *
from pathfinding import *
from object_renderer import *
from menu import *

class Game:
    # Constructor
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(settings.resolution)
        self.font = pg.font.Font(None, settings.font_size)
        self.game_mode_2d = settings.game_mode_2d
        self.game_over = True
        self.game_over_frames = 0
        self.menu = Menu(self)
        
        # print("health hud position = (%3d, %3d)" % settings.health_hud_position)
        
        # self.new_game()
        
    def new_game(self):
        if not self.game_mode_2d:
            pg.mouse.set_visible(False)
        self.game_over = False
        self.game_over_frames = 0
        self.clock = pg.time.Clock()
        self.delta_time = 0
        
        self.map = Map(self, True)

        self.pathfinding = PathFinding(self)
        self.sound = Sound(self)
        
        self.shotgun = Shotgun(self, self.sound.shotgun)
        self.sword = Sword(self, self.sound.sword)
        
        self.player_starting_pos = random.choice(self.map.empty_spaces)
        player_starting_anlge = math.tau * random.random()
        self.player = Player(self,
                             (self.player_starting_pos[0] + 0.51, self.player_starting_pos[1] + 0.51),
                             player_starting_anlge,
                             settings.player_speed,
                             settings.player_starting_health,
                             settings.player_size,
                             settings.player_color,
                             self.shotgun)
        self.enemy_handler = EnemyHandler(self)
        self.object_renderer = ObjectRenderer(self)
    
    # Check events
    def check_for_quit(self, event):
        return event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)
    
    def check_events(self):
        for event in pg.event.get():
            if self.check_for_quit(event):
                pg.quit()
                sys.exit()
    
    # Update game state
    def update(self):
        # print("Log: delta_time = %4.3f" % self.delta_time)
        self.delta_time = self.clock.tick(settings.fps)
        if not self.player.alive or len(self.enemy_handler.enemy_list) == 0:
            self.menu.update_at_game_over()
            self.game_over = True
            for enemy in self.enemy_handler.dead_enemy_list:
                self.game_over = self.game_over and (enemy.n_death_images == enemy.death_animation_counter)
        self.player.update()
        self.enemy_handler.update()
        
        # pg.display.set_caption(f'{self.clock.get_fps(): .1f}')

    # Update screen
    def draw2d(self):
        self.screen.fill('black')
        self.map.drawIn2d()
        self.object_renderer.draw_field_of_view_2d()
        self.player.drawIn2d()
        self.enemy_handler.drawIn2d()
        
    def draw3d(self):
        # self.screen.fill('black')
        # self.object_renderer.render_walls_3d_simple()
        self.object_renderer.render_3d()
        self.screen.blit(self.player.health_hud, settings.health_hud_position)
        
    def draw(self):
        pg.display.flip()
        if self.game_mode_2d:
            self.draw2d()
        else:
            self.draw3d()        
        
    # main funciton
    def run(self):
        while True:
            self.check_events()
            if not self.game_over:
                self.update()
                self.draw()
            else:
#                 if self.player.alive:
#                     game_over_text = self.font.render("You win!", False, "green")
#                 else:
#                     game_over_text = self.font.render("You lose!", False, "red")
#                 pg.display.flip()
#                 self.screen.blit(game_over_text,
#                                  (settings.screen_half_width - game_over_text.get_width() // 2,
#                                   settings.screen_half_height - game_over_text.get_height() // 2))
                
                if self.game_over_frames > 0:
                    self.menu.listen_to_inputs()
                    self.menu.draw()
#                     pg.time.wait(4000)
#                     self.new_game()
                else:
                    self.game_over_frames += 1
            
if __name__ == '__main__':
    game = Game()
    game.run()

