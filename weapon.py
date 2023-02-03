import pygame as pg
import os
import settings
from collections import deque

class Weapon:
    def __init__(self, game,
                 cooldown_time,
                 reload_time,
                 damage,
                 max_ammo,
                 max_range,
                 angle_tolerance,
                 ammo,
                 sprites_path,
                 sprite_scale,
                 sound):
        self.game = game
        self.cooldown_time = cooldown_time
        self.damage = damage
        self.max_ammo = max_ammo
        self.max_range = max_range
        self.angle_tolerance = angle_tolerance
        
        self.ammo = ammo
        self.last_time_used = pg.time.get_ticks()
        self.reload_start = pg.time.get_ticks()
        self.ready_to_use = True
        self.attacked = False
        
        self.images = self.get_images(sprites_path)
        self.width, self.height = self.images[0].get_width(), self.images[0].get_height()
        # print("Log: weapon width, height = %3d, %3d" % (self.width, self.height))
        self.images = deque(
                [ pg.transform.smoothscale(img, (self.width * sprite_scale, self.height * sprite_scale))
                  for img in self.images
                ]
            ) # Can I use map for this?
        # print("Log: weapon transformed width, height = %3d, %3d" % (self.images[0].get_width(), self.images[0].get_height()))
        self.n_images = len(self.images)
        
        self.position_on_screen = (settings.screen_half_width - self.width * sprite_scale // 2,
                                   settings.screen_height - self.height * sprite_scale)
        self.prev_frame_time = pg.time.get_ticks()
        self.animation_time = self.cooldown_time / self.n_images
        self.frame_counter = 0
        
        self.sound = sound
        
    def update(self):
        if self.attacked:
            self.attack()
            self.attacked = False
        if not self.ready_to_use:
            self.reload()
            
    def attack(self):
        if self.ready_to_use:
            # print("Log: Weapon used!")
            self.sound.play()
            self.ready_to_use = False
            self.last_time_used = pg.time.get_ticks()
            self.ammo -= 1
            for enemy in self.game.enemy_handler.enemy_list:
                enemy.did_attack_hit(self, self.game.player)
            
    # For animation... this code is copied from the animated sprite, so we should find a better solution
    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images
    
    def reload(self):
        time_now = pg.time.get_ticks()
        if time_now - self.prev_frame_time > self.animation_time:
            # print("Log: playing frame %1d of reload animation" % self.frame_counter)
            self.images.rotate(-1)
            self.prev_frame_time = time_now
            self.frame_counter = (self.frame_counter + 1) % self.n_images
        if self.frame_counter == 0 and pg.time.get_ticks() - self.last_time_used > self.cooldown_time:
            self.ready_to_use = True

class Shotgun(Weapon):
    def __init__(self, game, sound,
                 reload_time = 1000,
                 cooldown_time = 1000,
                 damage = 25,
                 max_ammo = float('inf'),
                 max_range = float('inf'),
                 angle_tolerance = 0,
                 ammo = float('inf'),
                 sprites_path = "resources/sprites/weapons/shotgun",
                 sprite_scale = 0.2):
        super().__init__(game,
                         cooldown_time,
                         reload_time,
                         damage,
                         max_ammo,
                         max_range,
                         angle_tolerance,
                         ammo,
                         sprites_path,
                         sprite_scale,
                         sound)
        
class Sword(Weapon):
    def __init__(self, game, sound,
                 reload_time = 500,
                 cooldown_time = 500,
                 damage = 50,
                 max_ammo = float('inf'),
                 max_range = 1.2,
                 angle_tolerance = 1,
                 ammo = float('inf'),
                 sprites_path = "resources/sprites/weapons/sword",
                 sprite_scale = 1.6):
        super().__init__(game,
                         cooldown_time,
                         reload_time,
                         damage,
                         max_ammo,
                         max_range,
                         angle_tolerance,
                         ammo,
                         sprites_path,
                         sprite_scale,
                         sound)