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
                 center_position = (0.5, 0.6),
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
        
        self.boss_image = pg.image.load("resources/sprites/boss/0.png").convert_alpha()
        self.boss_image = pg.transform.scale2x(pg.transform.scale2x(self.boss_image))
        self.boss_image_rect = self.boss_image.get_rect(center = (0.2 * settings.screen_width, 0.5 * settings.screen_height))
        self.boss_image_caption = self.game.font_small.render("Kill this dude!", False, "gray")
        self.boss_image_caption_rect = self.boss_image_caption.get_rect(center = (0.2 * settings.screen_width, 0.7 * settings.screen_height))
        
        self.rules_title = self.game.font_small.render("Controls:", False, "gray")
        self.rules_title_rect = self.rules_title.get_rect(center = (0.8 * settings.screen_width, 0.3 * settings.screen_height))
        self.rules_text = [ self.game.font_small.render("Movement: WASD + mouse", False, "gray"),
                            self.game.font_small.render("Attack: left mouse", False, "gray"),
                            self.game.font_small.render("Sword: 1", False, "gray"),
                            self.game.font_small.render("Shotgun: 2", False, "gray") ]
        self.rules_text_size = self.rules_text[0].get_height()
        self.rules_text_top_left = (0.7 * settings.screen_width, 0.4 * settings.screen_height)
        
        self.new_game_button = ButtonNewGame(self.game)
        
    def draw(self):
        pg.display.flip()
        self.game.screen.fill("black")
        self.game.screen.blit(self.game_title, self.game_title_rect)
        self.game.screen.blit(self.score_text, self.score_text_rect)
        self.game.screen.blit(self.game_result_text, self.game_result_text_rect)
        self.game.screen.blit(self.boss_image, self.boss_image_rect)
        self.game.screen.blit(self.boss_image_caption, self.boss_image_caption_rect)
        self.game.screen.blit(self.rules_title, self.rules_title_rect)
        for index, text in enumerate(self.rules_text):
            self.game.screen.blit(text, (self.rules_text_top_left[0],
                                         int(self.rules_text_top_left[1] + self.rules_text_size * index * 1.2)))
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
        
