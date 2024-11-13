from pico2d import *

class Idle:

    @staticmethod
    def enter(p1, e):
        pass

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        pass

    @staticmethod
    def draw(p1):
        if p1.char_name == 'naruto':
            if p1.dir == -1:
                p1.idle.clip_composite_draw(int(p1.frame) * 32, 0, 32, 48, 0, 'h', p1.sx, p1.sy - 15, 90, 135)
            elif p1.dir == 1:
                p1.idle.clip_composite_draw(int(p1.frame) * 32, 0, 32, 48, 0, '', p1.sx, p1.sy - 15, 90, 135)
        elif p1.char_name == 'sasuke':
            if p1.dir == -1:
                p1.idle.clip_composite_draw(int(p1.frame) * 32, 0, 32, 64, 0, 'h', p1.sx+10, p1.sy, 100, 200)
            elif p1.dir == 1:
                p1.idle.clip_composite_draw(int(p1.frame) * 32, 0, 32, 64, 0, '', p1.sx-10, p1.sy, 100, 200)

class Run:

    @staticmethod
    def enter(p2, e):
        pass
    @staticmethod
    def exit(p2, e):
        pass

    @staticmethod
    def do(p2):
        pass
    @staticmethod
    def draw(p2):
        if p2.char_name == 'naruto':
            if p2.dir == -1:
                p2.run.clip_composite_draw(int(p2.frame) * 48, 0, 48, 48, 0, 'h', p2.sx, p2.sy-15, 135, 135)
            elif p2.dir == 1:
                p2.run.clip_composite_draw(int(p2.frame) * 48, 0, 48, 48, 0, '', p2.sx, p2.sy-15, 135, 135)
        elif p2.char_name == 'sasuke':
            if p2.dir == -1:
                p2.run.clip_composite_draw(int(p2.frame) * 64, 0, 64, 32, 0, 'h', p2.sx, p2.sy - 15, 200, 100)
            elif p2.dir == 1:
                p2.run.clip_composite_draw(int(p2.frame) * 64, 0, 64, 32, 0, '', p2.sx, p2.sy - 15, 200, 100)


class Jump:
    @staticmethod
    def enter(p2, e):
        pass

    @staticmethod
    def exit(p2, e):
        pass

    @staticmethod
    def do(p2):
        pass

    @staticmethod
    def draw(p2):
        if p2.char_name == 'naruto':
            if p2.dir == -1:
                if int(p2.frame) < 2:
                    p2.jump.clip_composite_draw(int(p2.frame) * 32, 0, 32, 48, 0, 'h', p2.sx, p2.sy, 90, 135)
                else:
                    p2.jump.clip_composite_draw(64 + (int(p2.frame) - 2) * 40, 0, 40, 48, 0, 'h', p2.sx, p2.sy, 112, 135)
            elif p2.dir == 1:
                if int(p2.frame) < 2:
                    p2.jump.clip_composite_draw(int(p2.frame) * 32, 0, 32, 48, 0, '', p2.sx, p2.sy, 90, 135)
                else:
                    p2.jump.clip_composite_draw(64 + (int(p2.frame) - 2) * 40, 0, 40, 48, 0, '', p2.sx, p2.sy, 112, 135)
        elif p2.char_name == 'sasuke':
            if p2.dir == -1:
                p2.jump.clip_composite_draw(int(p2.frame) * 32, 0, 32, 64, 0, 'h', p2.sx, p2.sy, 100, 200)
            elif p2.dir == 1:
                p2.jump.clip_composite_draw(int(p2.frame) * 32, 0, 32, 64, 0, '', p2.sx, p2.sy, 100, 200)

class SASUKE_MULTI:
    global skill_num
    def __init__(self, p_num):
        self.x, self.y = 400, 0
        self.frame = 0
        self.dir = 1
        self.idle = load_image('resource/sasuke_idle.png')
        self.run = load_image('resource/sasuke_run.png')
        self.jump = load_image('resource/sasuke_jump.png')
        self.teleport = load_image('resource/sasuke_teleport.png')
        self.teleport_motion = load_image('resource/teleport.png')
        self.attack1 = load_image('resource/sasuke_attack1.png')
        self.attack2 = load_image('resource/sasuke_attack2.png')
        self.attack3 = load_image('resource/sasuke_attack3.png')
        self.attack4 = load_image('resource/sasuke_attack4.png')
        self.shuriken_stand = load_image('resource/sasuke_shuriken_stand.png')
        self.shuriken_jump = load_image('resource/sasuke_shuriken_jump.png')
        self.skill1 = load_image('resource/sasuke_skill1.png')
        self.skill2 = load_image('resource/sasuke_skill2.png')
        self.run_attack = load_image('resource/sasuke_run_attack.png')
        self.jump_attack = load_image('resource/sasuke_jump_attack.png')
        self.easy_hit = load_image('resource/sasuke_easy_hit.png')
        self.hard_hit = load_image('resource/sasuke_hard_hit.png')
        self.win_image = load_image('resource/sasuke_win.png')
        self.attack_s_1 = load_wav('sound/sasuke_attack1.wav')
        self.attack_s_1.set_volume(10)
        self.attack_s_2 = load_wav('sound/sasuke_attack2.wav')
        self.attack_s_2.set_volume(10)
        self.easy_hit_s = load_wav('sound/sasuke_easy_hit.wav')
        self.easy_hit_s.set_volume(5)
        self.hard_hit_s = load_wav('sound/sasuke_hard_hit.wav')
        self.hard_hit_s.set_volume(20)
        self.skill1_s = load_wav('sound/sasuke_skill1.wav')
        self.skill1_s.set_volume(10)
        self.skill2_s = load_wav('sound/sasuke_skill2.wav')
        self.skill2_s.set_volume(5)
        self.skill1_s_e = load_wav('sound/itachi_skill1_effect.wav')
        self.skill1_s_e.set_volume(10)
        self.skill2_s_e = load_wav('sound/sasuke_skill2_effect.wav')
        self.skill2_s_e.set_volume(10)
        self.win_s = load_wav('sound/sasuke_win.wav')
        self.win_s.set_volume(20)
        self.right = False
        self.left = False
        self.up_tele = False
        self.down_tele = False
        self.attack_num = 1
        self.wait_time = 0
        self.skill_num = 'shuriken'
        global player_num
        player_num = p_num
        self.invincible = False
        self.hp = 400
        self.chakra = 0
        self.chakra_lack = False
        self.win = False
        self.hit_state = 0
        self.sx, self.sy = 0, 0
        self.cur_state = Idle
        self.char_name = 'sasuke'


    def skill(self):
        pass

    def attack(self):
        pass

    def set_background(self, bg):
        self.bg = bg
        # self.x = self.bg.w / 2
        # self.y = self.bg.h / 2
    def update(self):
        pass


    def handle_event(self, event):
        pass

    def draw(self):
        self.sx, self.sy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        self.cur_state.draw(self)
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.sx - 30, self.sy - 70, self.sx + 30, self.sy + 70

    def handle_collision(self, group, other):
        pass

class NARUTO_MULTI:
    global skill_num
    def __init__(self, p_num):
        self.up = None
        self.x, self.y = 400, 0
        self.frame = 0
        self.dir = 1
        self.idle = load_image('resource/naruto_idle.png')
        self.run = load_image('resource/naruto_run.png')
        self.jump = load_image('resource/naruto_jump.png')
        self.teleport = load_image('resource/naruto_teleport.png')
        self.teleport_motion = load_image('resource/teleport.png')
        self.attack1 = load_image('resource/naruto_attack1.png')
        self.attack2 = load_image('resource/naruto_attack2.png')
        self.attack3 = load_image('resource/naruto_attack3.png')
        self.attack4 = load_image('resource/naruto_attack4.png')
        self.shuriken_stand = load_image('resource/naruto_shuriken_stand.png')
        self.shuriken_jump = load_image('resource/naruto_shuriken_jump.png')
        self.skill1 = load_image('resource/naruto_skill1.png')
        self.skill2 = load_image('resource/naruto_skill2.png')
        self.run_attack = load_image('resource/naruto_run_attack.png')
        self.jump_attack = load_image('resource/naruto_jump_attack.png')
        self.easy_hit = load_image('resource/naruto_easy_hit.png')
        self.hard_hit = load_image('resource/naruto_hard_hit.png')
        self.win_image = load_image('resource/naruto_win.png')
        self.attack_s_1 = load_wav('sound/naruto_attack1.wav')
        self.attack_s_1.set_volume(10)
        self.attack_s_2 = load_wav('sound/naruto_attack2.wav')
        self.attack_s_2.set_volume(10)
        self.easy_hit_s = load_wav('sound/naruto_easy_hit.wav')
        self.easy_hit_s.set_volume(2)
        self.hard_hit_s = load_wav('sound/naruto_har_hit.wav')
        self.hard_hit_s.set_volume(10)
        self.skill_s = load_wav('sound/naruto_skill.wav')
        self.skill_s.set_volume(10)
        self.skill_s_e = load_wav('sound/naruto_skill_effect.wav')
        self.skill_s_e.set_volume(10)
        self.win_s = load_wav('sound/naruto_win.wav')
        self.win_s.set_volume(10)
        self.right = False
        self.left = False
        self.up_tele = False
        self.down_tele = False
        self.attack_num = 1
        self.skill_num = 'shuriken'
        global player_num
        player_num = p_num
        self.invincible = False
        self.hp = 400
        self.chakra = 0
        self.chakra_lack = False
        self.win = False
        self.hit_state = 0
        self.sx, self.sy = 0, 0
        self.cur_state = Idle
        self.char_name = 'naruto'

    def skill(self):
        pass

    def attack(self):
        pass

    def set_background(self, bg):
        self.bg = bg
        # self.x = self.bg.w / 2
        # self.y = self.bg.h / 2

    def update(self):
        pass


    def handle_event(self, event):
        pass

    def draw(self):
        self.sx, self.sy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        self.cur_state.draw(self)
        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.sx - 30, self.sy - 70, self.sx + 30, self.sy + 70

    def handle_collision(self, group, other):
        pass