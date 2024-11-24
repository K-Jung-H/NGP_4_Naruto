from pico2d import *

import game_framework
import game_world
import mode_choose_mode
import play_mode
import math
import charactor_choose_mode

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
        self.damage = 10
        self.sx, self.sy = 0, 0

    def draw(self):

        self.shuriken.clip_composite_draw(int(self.frame) * 44, 0, 44, 35, 0, '', self.sx, self.sy, 44*1.5, 35*1.5)
        # draw_rectangle(*self.get_bb())

    def update(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
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

        if self.dir == 1:
            self.skill1_effect.clip_composite_draw(int(self.frame) * 97, 0, 97, 80, 0, '',
                                                    self.sx, self.sy + 90, 325, 241)
        elif self.dir == -1:
            self.skill1_effect.clip_composite_draw(int(self.frame) * 97, 0, 97, 80, 0, 'h',
                                                    self.sx, self.sy + 90, 325, 241)
        # draw_rectangle(*self.get_bb())

    def update(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
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
            Skill2.skill2_effect1 = load_image('resource/itachi_skill2_effect1.png')
        if Skill2.skill2_effect2 == None:
            Skill2.skill2_effect2 = load_image('resource/itachi_skill2_effect2.png')
        self.x, self.y = x, y - 60
        self.frame = 0
        self.dot_frame = 0
        self.dot_count = 0
        self.dir = dir
        self.count = 0
        self.damage = 15
        self.sx, self.sy = 0, 0
        self.reach = False
        if mode_choose_mode.mode_choose_result() == '2p':
            if charactor_choose_mode.p1_choose_result() == 3:
                self.p_num = 1
            elif charactor_choose_mode.p2_choose_result() == 3:
                self.p_num = 2
        elif mode_choose_mode.mode_choose_result() == '1p':
            self.p_num = 1
    def get_enenmy(self):
        if self.p_num == 1:
            if self.x < play_mode.p2.x:
                self.dir = 1
            else:
                self.dir = -1
            rad = math.atan2(play_mode.p2.y - self.y, play_mode.p2.x - self.x)
            self.x += 100 * math.cos(rad) * game_framework.frame_time
            self.y += 100 * math.sin(rad) * game_framework.frame_time
            pass
        elif self.p_num == 2:
            if self.x < play_mode.p1.x:
                self.dir = 1
            else:
                self.dir = -1
            rad = math.atan2(play_mode.p1.y - self.y, play_mode.p1.x - self.x)
            self.x += 100 * math.cos(rad) * game_framework.frame_time
            self.y += 100 * math.sin(rad) * game_framework.frame_time
            pass

    def draw(self):


        if not self.reach:
            self.get_enenmy()
            if self.dir == 1:
                self.skill2_effect1.clip_composite_draw(int(self.frame) * 122, 0, 122,56, 0, '',
                                                        self.sx, self.sy + 41, 200, 140)
            elif self.dir == -1:
                self.skill2_effect1.clip_composite_draw(int(self.frame) * 122, 0, 122, 56, 0, 'h',
                                                        self.sx, self.sy + 41, 200, 140)
        else:
            if self.p_num == 1:
                self.skill2_effect2.clip_composite_draw(int(self.frame) * 133, 0, 133, 150, 0, '',
                                                        play_mode.p2.sx, play_mode.p2.sy, 100, 130)
            elif self.p_num == 2:
                self.skill2_effect2.clip_composite_draw(int(self.frame) * 133, 0, 133, 150, 0, '',
                                                        play_mode.p1.sx, play_mode.p1.sy, 100, 130)
        # draw_rectangle(*self.get_bb())

    def update(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
        # self.count += 1
        self.frame = (self.frame + 6 * 1 * game_framework.frame_time) % 6
        if self.reach:
            self.dot_frame = self.dot_frame + 5 * game_framework.frame_time
            if self.dot_frame >= 10:
                print("dot++")
                self.dot_frame = 0
                self.dot_count += 1
                if self.p_num == 1:
                    if not play_mode.p2.invincible:
                        play_mode.p2.hp -= self.damage
                        play_mode.p2.frame = 0
                        play_mode.p2.hit_state = 'easy'
                elif self.p_num == 2:
                    if not play_mode.p1.invincible:
                        play_mode.p1.hp -= self.damage
                        play_mode.p1.frame = 0
                        play_mode.p1.hit_state = 'easy'
            if self.dot_count == 5:
                game_world.remove_object(self)
            if play_mode.p1.win or play_mode.p2.win:
                game_world.remove_object(self)
        pass

    def get_bb(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
        # return self.x - skill_range_x, self.y - skill_range_y, self.x + skill_range_x, self.y + skill_range_y
        return self.sx - 110, self.sy - 30, self.sx + 110, self.sy + 90

    def handle_collision(self, group, other):
        if not self.reach:
            if group == 'p1:p2_skill2' or group == 'p2:p1_skill2':
                print("아마테라스 맞음")
                self.reach = True

class Attack_range:
    def __init__(self, x = 400, y = 300, dir = 1, attack_num = 0):
        self.x, self.y = x, y
        self.frame = 0
        self.dir = dir
        self.range_set(0, 0, 0, 0, 0)
        self.attack_num = attack_num
        if self.attack_num == 1:
            self.range_set(50, 50, 30, 20, 15)
        elif self.attack_num == 2:
            self.range_set(80, 30, 50, 10, 15)
        elif self.attack_num == 3:
            self.range_set(80, 50, 50, 20, 20)
        elif self.attack_num == 4:
            self.range_set(60, 80, 50, 60, 25)
        elif self.attack_num == 'run':
            self.range_set(70, 50, 50, 0, 25)
        elif self.attack_num == 'jump':
            self.range_set(80, 40, 10, 0, 30)
        self.sx, self.sy = 0, 0

    def range_set(self, range_x, range_y, dis_x, dis_y, damage):
        self.attack_range_x = range_x
        self.attack_range_y = range_y
        self.attack_x_dis = dis_x
        self.attack_y_dis = dis_y
        self.damage = damage

    def update(self):
        self.sx, self.sy = self.x - play_mode.map.window_left, self.y - play_mode.map.window_bottom
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
        #
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
                other.dir = -self.dir
                other.hp -= self.damage
                other.frame = 0
                other.hit_state = 'easy'
                game_world.remove_object(self)
