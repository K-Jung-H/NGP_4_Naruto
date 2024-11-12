from pico2d import *

class SASUKE:
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
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.jump_move = False
        self.jump_state = False
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


    def skill(self):
        pass

    def attack(self):
        # attack_range = Attack_range(self.x, self.y, self.dir, self.attack_num)
        # game_world.add_object(attack_range, 2)
        # if self.attack_num == 2 or self.attack_num == 'jump':
        #     self.attack_s_1.play()
        # if self.attack_num == 4 or self.attack_num == 'run':
        #     self.attack_s_2.play()
        # if player_num == 1:
        #     game_world.add_collision_pair('p2:p1_attack', None, attack_range)
        # elif player_num == 2:
        #     game_world.add_collision_pair('p1:p2_attack', None, attack_range)
        pass

    def set_background(self, bg):
        self.bg = bg
        # self.x = self.bg.w / 2
        # self.y = self.bg.h / 2
    def update(self):
        # if self.hit_state == 'hard':
        #     if not self.state_machine.cur_state == Hard_hit:
        #         self.hard_hit_s.play()
        #     self.state_machine.cur_state = Hard_hit
        #     self.hit_state = 0
        # if self.hit_state == 'easy':
        #     self.easy_hit_s.play()
        #     self.state_machine.cur_state = Easy_hit
        #     self.hit_state = 0
        # self.state_machine.update()
        # if self.chakra <= 100:
        #     self.chakra += 4 * game_framework.frame_time
        # self.x = clamp(50.0, self.x, self.bg.w - 50.0)
        # self.y = clamp(50.0, self.y, self.bg.h - 50.0)
        pass


    def handle_event(self, event):
        # self.state_machine.handle_event(('INPUT', event))
        # if right_up(('INPUT', event)):
        #     self.right = False
        # if left_up(('INPUT', event)):
        #     self.left = False
        # if right_down(('INPUT', event)):
        #     self.right = True
        # if left_down(('INPUT', event)):
        #     self.left = True
        pass

    def draw(self):
        self.sx, self.sy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        self.state_machine.draw()
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.sx - 30, self.sy - 70, self.sx + 30, self.sy + 70

    def handle_collision(self, group, other):
        pass