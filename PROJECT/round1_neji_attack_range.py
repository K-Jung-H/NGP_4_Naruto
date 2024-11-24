from pico2d import *

import game_framework
import game_world
import play_mode

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 50.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Shuriken:
    shuriken = None
    def __init__(self, x = 400, y = 300, dir = 1):
        if Shuriken.shuriken == None:
            Shuriken.shuriken = load_image('resource/shuriken4.png')
        self.x, self.y = x, y,
        self.frame = 0
        self.dir = dir
        self.count = 0
        self.damage = 10
        self.sx, self.sy = 0, 0

    def draw(self):
        if self.dir == 1:
            self.shuriken.clip_composite_draw(int(self.frame) * 46, 0, 46, 35, 0, '', self.sx, self.sy, 46*2, 35*2)
        elif self.dir == -1:
            self.shuriken.clip_composite_draw(int(self.frame) * 46, 0, 46, 35, 0, 'h', self.sx, self.sy, 46*2, 35*2)
        # draw_rectangle(*self.get_bb())

    def update(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
        self.frame = (self.frame + 4 * 4 * game_framework.frame_time) % 4
        self.x += self.dir * RUN_SPEED_PPS * 1.5 * game_framework.frame_time
        if self.x < 0 or self.x > play_mode.map.w:
            game_world.remove_object(self)
        if play_mode.p1.win or play_mode.p2.win:
            game_world.remove_object(self)

    def get_bb(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
        return self.sx - 22, self.sy - 18, self.sx + 22, self.sy + 18

    def handle_collision(self, group, other):
        if group == 'p1:p2_shuriken' or group == 'p2:p1_shuriken':
            # print("충돌")
            if not other.invincible:
                other.dir = -self.dir
                print(self.damage)
                other.hp -= self.damage
                other.frame = 0
                other.hit_state = 'easy'
                game_world.remove_object(self)

class Skill1:
    skill1_effect = None
    def __init__(self, x = 400, y = 300, dir = 1):
        if Skill1.skill1_effect == None:
            Skill1.skill1_effect = load_image('resource/naruto_skill1_effect.png')
        self.x, self.y = x, y
        self.frame = 0
        self.dir = dir
        self.count = 0
       # self.damage = 40
        self.damage = 10
        self.sx, self.sy = 0, 0
        self.range_set(-100, -100, 0, 0, 0)


    def range_set(self, range_x, range_y, dis_x, dis_y, damage):
        self.attack_range_x = range_x
        self.attack_range_y = range_y
        self.attack_x_dis = dis_x
        self.attack_y_dis = dis_y
        self.damage = damage

    def draw(self):

        # if self.dir == 1:
        #     self.skill1_effect.clip_composite_draw(int(self.frame) * 193, 0, 193, 136, 0, '',
        #                                            self.sx, self.sy+20, 543, 382)
        # elif self.dir == -1:
        #     self.skill1_effect.clip_composite_draw(int(self.frame) * 193, 0, 193, 136, 0, 'h',
        #                                            self.sx, self.sy+20, 543, 382)
        # draw_rectangle(*self.get_bb())
        pass

    def update(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
        if int(self.frame) == 3:
            self.range_set(70, 60, 40, -40, 40)

        if self.frame < 3:
            self.frame = (self.frame + 59 * 0.03 * game_framework.frame_time) % 59
        else:
            self.frame = (self.frame + 59 * 0.2 * game_framework.frame_time) % 59
            self.x += self.dir * RUN_SPEED_PPS * 0.4 * game_framework.frame_time
        if play_mode.p1.x < self.x:
            self.dir = -1
        elif play_mode.p1.x >= self.x:
            self.dir = 1
        if self.frame >= 58:
            game_world.remove_object(self)
        if play_mode.p1.win or play_mode.p2.win:
            game_world.remove_object(self)

    def get_bb(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
        return (self.sx - self.attack_range_x + self.dir * self.attack_x_dis,
                self.sy - self.attack_range_y + self.attack_y_dis,
                self.sx + self.attack_range_x + self.dir * self.attack_x_dis,
                self.sy + self.attack_range_y + self.attack_y_dis)
        # if self.dir == 1:
        #     return self.sx - 30, self.sy-100, self.sx + 110, self.sy + 25
        # elif self.dir == -1:
        #     return self.sx - 110, self.sy-100, self.sx + 30, self.sy + 25


    def handle_collision(self, group, other):
        if not other.invincible:
            if group == 'p1:p2_skill1' or group == 'p2:p1_skill1':
                print("64장 맞음")
                other.hp -= self.damage
                other.dir = -self.dir
                other.frame = 0
                print(other.hp)
                other.hit_state = 'hard'
               # other.hit_state = 'easy'
                other.invincible = True
            # game_world.remove_object(self)

class Skill2:
    skill2_effect = None
    def __init__(self, x = 400, y = 300, dir = 1):
        if Skill2.skill2_effect == None:
            Skill2.skill2_effect = load_image('resource/naruto_skill2_effect.png')
        self.x, self.y = x, y
        self.frame = 0
        self.dir = dir
        self.count = 0
        self.damage = 60
        self.sx, self.sy = 0, 0

    def draw(self):

        if self.frame >= 7:
            if self.dir == 1:
                self.skill2_effect.clip_composite_draw((int(self.frame)-7) * 159, 0, 159, 88, 0, '',
                                                       self.sx, self.sy , 447, 247)
            elif self.dir == -1:
                self.skill2_effect.clip_composite_draw((int(self.frame)-7) * 159, 0, 159, 88, 0, 'h',
                                                       self.sx, self.sy, 447, 247)
        # draw_rectangle(*self.get_bb())

    def update(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
        self.frame = (self.frame + 16 * 1 * game_framework.frame_time) % 16
        if self.frame >= 7:
            self.x += self.dir * RUN_SPEED_PPS * 1 * game_framework.frame_time
            if self.frame >= 15:
                self.frame = 12
        if self.x < 0 or self.x > play_mode.map.w:
            game_world.remove_object(self)
        pass

    def get_bb(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
        if self.dir == 1:
            return self.sx - 80, self.sy - 130, self.sx + 220, self.sy + 110
        elif self.dir == -1:
            return self.sx - 220, self.sy - 130, self.sx + 80, self.sy + 110

    def handle_collision(self, group, other):
        if not other.invincible:
            if group == 'p1:p2_skill2' or group == 'p2:p1_skill2':
                print("나선환 맞음")
                other.hp -= self.damage
                other.dir = -self.dir
                other.frame = 0
                print(other.hp)
                other.hit_state = 'hard'
                other.invincible = True
            # game_world.remove_object(self)


class Attack_range:
    def __init__(self, x = 400, y = 300, dir = 1, attack_num = 0):
        self.x, self.y = x, y
        self.frame = 0
        self.dir = dir
        self.range_set(0, 0, 0, 0, 0)
        self.attack_num = attack_num
        if self.attack_num == 1:
            self.range_set(50, 20, 40, 10, 10)
        elif self.attack_num == 2:
            self.range_set(50, 30, 30, 15, 10)
        elif self.attack_num == 3:
            self.range_set(70, 30, 40, 0, 15)
        elif self.attack_num == 4:
            self.range_set(70, 50, 40, 0, 20)
        elif self.attack_num == 'run':
            self.range_set(40, 50, 30, -20, 30)
        elif self.attack_num == 'jump':
            self.range_set(50, 60, 30, 20, 30)
        self.sx, self.sy = 0, 0

    def range_set(self, range_x, range_y, dis_x, dis_y, damage):
        self.attack_range_x = range_x
        self.attack_range_y = range_y
        self.attack_x_dis = dis_x
        self.attack_y_dis = dis_y
        self.damage = damage

    def update(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
        self.frame = self.frame + 5 * 3 * game_framework.frame_time
        if self.attack_num == 1:
            if self.frame >= 4:
                self.frame = 0
                game_world.remove_object(self)
        if self.attack_num == 2:
            if self.frame >= 6:
                self.frame = 0
                game_world.remove_object(self)
        if self.attack_num == 3:
            if self.frame >= 9:
                self.frame = 0
                game_world.remove_object(self)
        if self.attack_num == 4:
            if self.frame >= 7:
                self.frame = 0
                game_world.remove_object(self)
        if self.attack_num == 'run':
            self.x += self.dir * RUN_SPEED_PPS * 1 * game_framework.frame_time
            if self.frame >= 6.5:
                self.frame = 0
                game_world.remove_object(self)
        if self.attack_num == 'jump':
            if self.frame >= 3:
                self.frame = 0
                game_world.remove_object(self)

    def draw(self):

        # draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
        return (self.sx - self.attack_range_x + self.dir * self.attack_x_dis,
                self.sy - self.attack_range_y + self.attack_y_dis,
                self.sx + self.attack_range_x + self.dir * self.attack_x_dis,
                self.sy + self.attack_range_y + self.attack_y_dis)

    def handle_collision(self, group, other):
        if not other.invincible:
            if group == 'p1:p2_attack' or group == 'p2:p1_attack':
                # print("충돌")
                other.hp -= self.damage
                other.dir = -self.dir
                other.frame = 0
                print(other.hp)
                other.hit_state = 'easy'
                game_world.remove_object(self)