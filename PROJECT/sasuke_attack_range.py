from pico2d import *

import game_framework
import game_world
import mode_choose_mode
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
            Shuriken.shuriken = load_image('resource/shuriken1.png')
        self.x, self.y = x, y,
        self.frame = 0
        self.dir = dir
        self.count = 0
        self.damage = 10
        self.sx, self.sy = 0, 0

    def draw(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
        self.shuriken.clip_composite_draw(int(self.frame) * 44, 0, 44, 35, 0, '', self.sx, self.sy, 44*1.5, 35*1.5)
        # draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + 4 * 4 * game_framework.frame_time) % 4
        self.x += self.dir * RUN_SPEED_PPS * 1.5 * game_framework.frame_time
        if self.x < 0 or self.x > play_mode.map.w:
            print("표창 사라짐")
            game_world.remove_object(self)
        if play_mode.p1.win or play_mode.p2.win:
            game_world.remove_object(self)

    def get_bb(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
        return self.sx - 22, self.sy - 18, self.sx + 22, self.sy + 18

    def handle_collision(self, group, other):
        if group == 'p1:p2_shuriken' or group == 'p2:p1_shuriken':
            print("충돌")
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
            Skill1.skill1_effect = load_image('resource/sasuke_skill1_effect.png')
        self.x, self.y = x + dir * 150, y
        self.frame = 0
        self.dir = dir
        self.count = 0
        self.damage = 60
        self.sx, self.sy = 0, 0

    def draw(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
        if self.dir == 1:
            self.skill1_effect.clip_composite_draw(int(self.frame) * 97, 0, 97, 80, 0, '',
                                                    self.sx, self.sy + 90, 325, 241)
        elif self.dir == -1:
            self.skill1_effect.clip_composite_draw(int(self.frame) * 97, 0, 97, 80, 0, 'h',
                                                    self.sx, self.sy + 90, 325, 241)
        # draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + 10 * 2 * game_framework.frame_time) % 10
        if self.frame >= 8:
            self.frame = 5
        # if self.frame >= 9:
        self.x += self.dir * RUN_SPEED_PPS * 1.2 * game_framework.frame_time
        if self.x < 0 - 200 or self.x > play_mode.map.w + 200:
            print("화둔 없어짐")
            game_world.remove_object(self)
        if play_mode.p1.win or play_mode.p2.win:
            game_world.remove_object(self)

    def get_bb(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
        # return self.x - skill_range_x, self.y - skill_range_y, self.x + skill_range_x, self.y + skill_range_y
        return self.sx - 140, self.sy - 40, self.sx + 140, self.sy + 150

    def handle_collision(self, group, other):
        if not other.invincible:
            if group == 'p1:p2_skill1' or group == 'p2:p1_skill1':
                print("화둔 맞음")
                other.hp -= self.damage
                other.dir = -self.dir
                other.frame = 0
                print(other.hp)
                other.hit_state = 'hard'
                other.invincible = True
class Skill2:
    skill2_effect1 = None
    skill2_effect2 = None
    def __init__(self, x = 400, y = 300, dir = 1):
        if Skill2.skill2_effect1 == None:
            Skill2.skill2_effect1 = load_image('resource/sasuke_skill2_effect1.png')
        if Skill2.skill2_effect2 == None:
            Skill2.skill2_effect2 = load_image('resource/sasuke_skill2_effect2.png')
        self.x, self.y = x, y
        self.frame = 0
        self.dir = dir
        self.count = 0
        self.damage = 80
        self.sx, self.sy = 0, 0

    def draw(self):

        if self.frame <= 7:
            self.skill2_effect2.clip_composite_draw(int(self.frame) * 104, 0, 104, 77, 0, '',
                                                    self.sx, self.sy + 41, 325, 241)
            # p1.skill1_stand.clip_composite_draw(int(p1.frame) * 40, 0, 40, 64, 0, 'h', p1.x, p1.y, 125, 200)
        if self.frame >= 1:
            if self.dir == -1:
                if self.frame > 7:
                    self.skill2_effect1.clip_composite_draw((int(self.frame) - 1) * 104, 0, 104, 77, 0, 'h',
                                                            self.sx + 30, self.sy - 10, 325, 241)
                else:
                    self.skill2_effect1.clip_composite_draw((int(self.frame) - 1) * 104, 0, 104, 77, 0, 'h',
                                                            self.sx + 30, self.sy + 41 - 10, 325, 241)
            elif self.dir == 1:
                if self.frame > 7:
                    self.skill2_effect1.clip_composite_draw((int(self.frame) - 1) * 104, 0, 104, 77, 0, '',
                                                            self.sx - 30, self.sy - 10, 325, 241)
                else:
                    self.skill2_effect1.clip_composite_draw((int(self.frame) - 1) * 104, 0, 104, 77, 0, '',
                                                            self.sx - 30, self.sy + 41 - 10, 325, 241)
        # draw_rectangle(*self.get_bb())

    def update(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
        self.count += 1
        self.frame = (self.frame + 18 * 1 * game_framework.frame_time) % 18
        if self.frame >= 7:
            self.x += self.dir * RUN_SPEED_PPS * 2 * game_framework.frame_time
        if self.frame >= 17:
            game_world.remove_object(self)
        if play_mode.p1.win or play_mode.p2.win:
            game_world.remove_object(self)
        pass

    def get_bb(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
        # return self.x - skill_range_x, self.y - skill_range_y, self.x + skill_range_x, self.y + skill_range_y
        return self.sx - 130, self.sy - 70, self.sx + 130, self.sy + 70

    def handle_collision(self, group, other):
        if not other.invincible:
            if group == 'p1:p2_skill2' or group == 'p2:p1_skill2':
                print("치도리 맞음")
                other.hp -= self.damage
                other.dir = -self.dir
                other.frame = 0
                print(other.hp)
                other.hit_state = 'hard'
                other.invincible = True

class Attack_range:
    def __init__(self, x = 400, y = 300, dir = 1, attack_num = 0):
        self.x, self.y = x, y
        self.frame = 0
        self.dir = dir
        self.range_set(0, 0, 0, 0, 0)
        self.attack_num = attack_num
        if self.attack_num == 1:
            self.range_set(80, 30, 60, 0, 10)
        elif self.attack_num == 2:
            self.range_set(90, 30, 60, 10, 10)
        elif self.attack_num == 3:
            self.range_set(105, 70, 90, 0, 15)
        elif self.attack_num == 4:
            self.range_set(105, 80, 90, 20, 20)
        elif self.attack_num == 'run':
            self.range_set(100, 30, 60, -20, 20)
        elif self.attack_num == 'jump':
            self.range_set(90, 50, 10, -10, 25)
        self.sx, self.sy = 0, 0

    def range_set(self, range_x, range_y, dis_x, dis_y, damage):
        self.attack_range_x = range_x
        self.attack_range_y = range_y
        self.attack_x_dis = dis_x
        self.attack_y_dis = dis_y
        self.damage = damage

    def update(self):
        self.frame = self.frame + 7 * 3 * game_framework.frame_time
        if self.attack_num == 1:
            if self.frame >= 4:
                self.frame = 0
                game_world.remove_object(self)
        if self.attack_num == 2:
            if self.frame >= 5:
                self.frame = 0
                game_world.remove_object(self)
        if self.attack_num == 3:
            if self.frame >= 7:
                self.frame = 0
                game_world.remove_object(self)
        if self.attack_num == 4:
            if self.frame >= 6.5:
                self.frame = 0
                game_world.remove_object(self)
        if self.attack_num == 'run':
            self.x += self.dir * RUN_SPEED_PPS * 1 * game_framework.frame_time
            if self.frame >= 6.5:
                self.frame = 0
                game_world.remove_object(self)
        if self.attack_num == 'jump':
            if self.frame >= 4:
                self.frame = 0
                game_world.remove_object(self)
        pass

    def draw(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
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
                #if mode_choose_mode.mode_choose_result() == '1p':
                play_mode.p1.chakra += int(self.damage//2)
                print("차크라충전")
                other.hp -= self.damage
                other.dir = -self.dir
                other.frame = 0
                print(other.hp)
                other.hit_state = 'easy'
                game_world.remove_object(self)