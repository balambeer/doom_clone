import pygame as pg

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = "resources/sounds/"
        
        self.shotgun = pg.mixer.Sound(self.path + "shotgun.wav")
        self.shotgun.set_volume(0.5)
        self.sword = pg.mixer.Sound(self.path + "sword.ogg")
        self.player_pain = pg.mixer.Sound(self.path + "player_pain.wav")
        
        self.enemy_attack = pg.mixer.Sound(self.path + "enemy_attack.wav")
        self.enemy_attack.set_volume(0.5)
        self.enemy_pain = pg.mixer.Sound(self.path + "enemy_pain.wav")
        self.enemy_death = pg.mixer.Sound(self.path + "enemy_death.wav")