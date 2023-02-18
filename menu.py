import pygame as pg
import settings

class Button():
    def __init__(self, game,
                 center_position,
                 text,
                 text_color,
                 idle_color,
                 clicked_color):
        self.game = game
        
        self.text_color = text_color
        self.idle_color = idle_color
        self.clicked_color = clicked_color
        
        self.current_color = self.idle_color
        self.text = self.game.font.render(text, False, self.text_color)
        self.text_rect = self.text.get_rect(center = (int(center_position[0] * settings.resolution[0]),
                                                      int(center_position[1] * settings.resolution[1])))
        
        self.background_rect = self.text_rect.inflate(0.1 * self.text.get_width(),
                                                      0.1 * self.text.get_height())
        
    def draw(self):
        pg.draw.rect(self.game.screen, self.current_color, self.background_rect)
        pg.draw.rect(self.game.screen, self.text_color, self.background_rect, int(0.1 * self.text.get_height()))
        self.game.screen.blit(self.text, self.text_rect)
        
    def is_left_clicked(self):
        if pg.mouse.get_pressed()[0]:
            return self.background_rect.collidepoint(pg.mouse.get_pos())
            
class ButtonNewGame(Button):
    def __init__(self, game,
                 center_position = (0.5, 0.5),
                 text = "New Game",
                 text_color = "khaki2",
                 background_color = "black",
                 clicked_color = "black"):
        super().__init__(game, center_position, text, text_color, background_color, clicked_color)
        
    def listen(self):
        if self.is_left_clicked():
            self.game.new_game()
        
class Menu():
    def __init__(self, game):
        self.game = game
        
        #self.game_title = self.game.font.render("BOOM", False, "red")
        self.game_title = pg.image.load("resources/menu/logo.jpg").convert_alpha()
        self.game_title = pg.transform.scale2x(self.game_title)
        self.game_title_rect = self.game_title.get_rect(center = (0.5 * settings.screen_width, 0.2 * settings.screen_height))
        
        self.game_score = 0
        self.score_text = self.game.font.render("Score: " + f"{self.game_score}", False, "gray")
        self.score_text_rect = self.score_text.get_rect(center = (0.5 * settings.screen_width, 0.8 * settings.screen_height))
        
        self.game_result_text = self.game.font.render(" ", False, "gray")
        self.game_result_text_rect = self.game_result_text.get_rect(center = (0.5 * settings.screen_width, 0.4 * settings.screen_height))
        
        self.new_game_button = ButtonNewGame(self.game)
        
    def draw(self):
        pg.display.flip()
        self.game.screen.fill("black")
        self.game.screen.blit(self.game_title, self.game_title_rect)
        self.game.screen.blit(self.score_text, self.score_text_rect)
        self.game.screen.blit(self.game_result_text, self.game_result_text_rect)
        self.new_game_button.draw()
        
    def update_at_game_over(self):
        pg.mouse.set_visible(True)
        pg.mouse.set_pos((0.5 * settings.screen_width, 0.9 * settings.screen_height))
        
        self.game_score = self.game.player.health
        self.score_text = self.game.font.render("Score: " + f"{self.game_score}", False, "gray")
        self.score_text_rect = self.score_text.get_rect(center = (0.5 * settings.screen_width, 0.8 * settings.screen_height))
        
        if self.game.player.alive:
            self.game_result_text = self.game.font.render("You win!", False, "darkolivegreen3")
            self.game_result_text_rect = self.game_result_text.get_rect(center = (0.5 * settings.screen_width,                                                                       0.4 * settings.screen_height))
        else:
            self.game_result_text = self.game.font.render("You lose!", False, "firebrick3")
            self.game_result_text_rect = self.game_result_text.get_rect(center = (0.5 * settings.screen_width,
                                                                                  0.4 * settings.screen_height))
            
    def listen_to_inputs(self):
        self.new_game_button.listen()
        
