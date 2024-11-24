# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import *

import game_framework
import game_world
from sasuke_attack_range import Shuriken, Skill1, Skill2, Attack_range

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 50.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

ground_y = 120
tele_dis = 220
player_num = 0
delay_shu = False
t_time = 0
delay_tel = False
t_time2 = 0
delay_jum = False
t_time3 = 0

def up_down(e):
    global delay_jum
    if get_time() - t_time3 >= 0.45:
        delay_jum = False
    if not delay_jum:
        if player_num == 1:
            return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP
        elif player_num == 2:
            return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w

def up_up(e):
    if player_num == 1:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP
    elif player_num == 2:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w

def down_down(e):
    if player_num == 1:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN
    elif player_num == 2:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s

def down_up(e):
    if player_num == 1:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN
    elif player_num == 2:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s

def right_down(e):
    if player_num == 1:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
    elif player_num == 2:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

def right_up(e):
    if player_num == 1:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
    elif player_num == 2:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d

def left_down(e):
    if player_num == 1:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
    elif player_num == 2:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def left_up(e):
    if player_num == 1:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
    elif player_num == 2:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def teleport_down(e):
    global delay_tel
    if get_time() - t_time2 >= 1:
        delay_tel = False
    if not delay_tel:
        if player_num == 1:
            return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_PERIOD
        elif player_num == 2:
            return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_v

def attack_down(e):
    if player_num == 1:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_COMMA
    elif player_num == 2:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c

def shuriken_down(e):
    global delay_shu
    if get_time() - t_time >= 1:
        delay_shu = False
    if not delay_shu:
        if player_num == 1:
            return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SLASH
        elif player_num == 2:
            return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_b

def skill1_down(e):
    if player_num == 1:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_l
    elif player_num == 2:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f

def skill2_down(e):
    if player_num == 1:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SEMICOLON
    elif player_num == 2:
        return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_g

def time_out(e):
    return e[0] == 'TIME_OUT'

def jump_end(e):
    return e[0] == 'JUMP_END'

def jump_end_run(e):
    return e[0] == 'JUMP_END_RUN'

def teleport(e):
    return e[0] == 'TELEPORT'

def jump_state(e):
    return e[0] == 'JUMP_STATE'

def run_state(e):
    return e[0] == 'RUN_STATE'

def stop(e):
    return e[0] == 'STOP'

class Idle:

    @staticmethod
    def enter(p1, e):
        pass

    @staticmethod
    def exit(p1, e):
        p1.frame = 0

        if shuriken_down(e):
            global delay_shu
            p1.skill_num = 'shuriken'
            p1.skill()
            delay_shu = True
        if skill1_down(e):
            p1.skill_num = 'skill1'
            # p1.skill()
            if p1.chakra >= 30:
                p1.chakra -= 30
                p1.chakra_lack = False
                p1.skill1_s.play()
                # p1.skill()
            else:
                p1.chakra_lack = True
        if skill2_down(e):
            p1.skill_num = 'skill2'
            if p1.chakra >= 30:
                p1.skill2_s_e.play()
                p1.chakra -= 30
                p1.chakra_lack = False
                p1.skill()
            else:
                p1.chakra_lack = True

        if right_down(e):
            p1.right = True
        elif left_down(e):
            p1.left = True
        elif right_up(e):
            p1.right = False
        elif left_up(e):
            p1.left = False

    @staticmethod
    def do(p1):
        if p1.win:
            p1.win_s.play()
            p1.state_machine.cur_state = Win
        if p1.hp <= 0:
            p1.state_machine.cur_state = Lose

        if p1.y > ground_y:
            p1.state_machine.handle_event(('JUMP_STATE', None))
        if p1.right and not p1.left:
            p1.state_machine.handle_event(('RUN_STATE', None))
        if not p1.right and p1.left:
            p1.state_machine.handle_event(('RUN_STATE', None))
        p1.frame = (p1.frame + 6 * 1 * game_framework.frame_time) % 6

    @staticmethod
    def draw(p1):
        if p1.dir == -1:
            p1.idle.clip_composite_draw(int(p1.frame) * 32, 0, 32, 64, 0, 'h', p1.sx+10, p1.sy, 100, 200)
        elif p1.dir == 1:
            p1.idle.clip_composite_draw(int(p1.frame) * 32, 0, 32, 64, 0, '', p1.sx-10, p1.sy, 100, 200)


class Run:

    @staticmethod
    def enter(p1, e):

        if p1.right and not p1.left:
            p1.dir = 1
        elif p1.left and not p1.right:
            p1.dir = -1

    @staticmethod
    def exit(p1, e):
        p1.frame = 0
        if shuriken_down(e):
            global delay_shu
            p1.skill_num = 'shuriken'
            p1.skill()
            delay_shu = True

    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + 6 * 2 * game_framework.frame_time) % 6
        p1.x += p1.dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(p1):
        if p1.dir == -1:
            p1.run.clip_composite_draw(int(p1.frame) * 64, 0, 64, 32, 0, 'h', p1.sx, p1.sy-15, 200, 100)
        elif p1.dir == 1:
            p1.run.clip_composite_draw(int(p1.frame) * 64, 0, 64, 32, 0, '', p1.sx, p1.sy-15, 200, 100)


class Jump:
    @staticmethod
    def enter(p1, e):
        if right_down(e):
            p1.right = True
        if left_down(e):
            p1.left = True
        if right_up(e):
            p1.right = False
        if left_up(e):
            p1.left = False
        if up_down(e):
            p1.up_tele = True
            global delay_jum
            delay_jum = True
            global t_time3
            t_time3 = get_time()
        if up_up(e):
            p1.up_tele = False
        if down_down(e):
            p1.down_tele = True
        if down_up(e):
            p1.down_tele = False
        if p1.right and not p1.left:
            p1.dir = 1
            p1.jump_move = True
        elif p1.left and not p1.right:
            p1.dir = -1
            p1.jump_move = True

        if jump_state(e):
            p1.frame = 2

        p1.jump_state = True

    @staticmethod
    def exit(p1, e):
        if up_down(e):
            p1.frame = 0
        if shuriken_down(e):
            global delay_shu
            p1.skill_num = 'shuriken'
            p1.skill()
            delay_shu = True
            p1.frame = 0
        if teleport_down(e):
            p1.frame = 0
    @staticmethod
    def do(p1):
        if not p1.right and not p1.left:
            p1.jump_move = False
        if p1.right and p1.left:
            p1.jump_move = False
        if p1.frame >= 3:
            p1.frame = 3
        else:
            p1.frame = (p1.frame + 4 * 1.5 * game_framework.frame_time) % 4

        p1.y += 1.2 * RUN_SPEED_PPS * game_framework.frame_time * (2 - p1.frame)

        if p1.jump_move:
            p1.x += p1.dir * RUN_SPEED_PPS * game_framework.frame_time

        if p1.y <= ground_y:
            p1.y = ground_y
            p1.frame = 0
            p1.state_machine.handle_event(('JUMP_END', None))
            p1.jump_state = False
            p1.jump_move = False

    @staticmethod
    def draw(p1):
        if p1.dir == -1:
            p1.jump.clip_composite_draw(int(p1.frame) * 32, 0, 32, 64, 0, 'h', p1.sx, p1.sy, 100, 200)
        elif p1.dir == 1:
            p1.jump.clip_composite_draw(int(p1.frame) * 32, 0, 32, 64, 0, '', p1.sx, p1.sy, 100, 200)

class Teleport:
    @staticmethod
    def enter(p1, e):
        if right_down(e):
            p1.dir = 1
            p1.right = True
        elif left_down(e):
            p1.dir = -1
            p1.left = True
        elif right_up(e):
            p1.right = False
        elif left_up(e):
            p1.left = False
        else:
            p1.attack_s_1.play()

    @staticmethod
    def exit(p1, e):
        if p1.frame >= 3:
            if p1.up_tele:
                if p1.right and not p1.left:
                    p1.x += tele_dis
                elif p1.left and not p1.right:
                    p1.x -= tele_dis
                p1.y += tele_dis
                p1.up_tele = False
            elif p1.down_tele:
                if p1.right and not p1.left:
                    p1.x += tele_dis
                elif p1.left and not p1.right:
                    p1.x -= tele_dis
                p1.y -= tele_dis
                if p1.y <= ground_y:
                    p1.y = ground_y
                p1.down_tele = False
            else:
                if p1.right and not p1.left:
                    p1.x += tele_dis
                elif p1.left and not p1.right:
                    p1.x -= tele_dis
        global delay_tel
        delay_tel = True
        global t_time2
        t_time2 = get_time()

    @staticmethod
    def do(p1):
        p1.frame = p1.frame + 4 * 4 * game_framework.frame_time
        if p1.frame >= 3:
            p1.state_machine.handle_event(('TELEPORT', None))

    @staticmethod
    def draw(p1):
        if p1.dir == -1:
            p1.teleport.clip_composite_draw(int(p1.frame) * 32, 0, 32, 64, 0, 'h', p1.sx, p1.sy, 100, 200)
            p1.teleport_motion.clip_composite_draw(int(p1.frame) * 72, 0, 72, 75, 0, 'h', p1.sx, p1.sy, 150, 250)
        elif p1.dir == 1:
            p1.teleport.clip_composite_draw(int(p1.frame) * 32, 0, 32, 64, 0, '', p1.sx, p1.sy, 100, 200)
            p1.teleport_motion.clip_composite_draw(int(p1.frame) * 72, 0, 72, 75, 0, '', p1.sx, p1.sy, 150, 250)

class Attack:
    @staticmethod
    def enter(p1, e):
        if get_time() - p1.wait_time > 0.5:
            p1.attack_num = 1
        if right_down(e):
            p1.right = True
        elif left_down(e):
            p1.left = True
        elif right_up(e):
            p1.right = False
        elif left_up(e):
            p1.left = False
        else:
            p1.attack()

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.frame = p1.frame + 7 * 3 * game_framework.frame_time
        if p1.attack_num == 1:
            if p1.frame >= 4:
                p1.state_machine.handle_event(('STOP', None))
                p1.attack_num = 2
                p1.frame = 0
                p1.wait_time = get_time()
        if p1.attack_num == 2:
            if p1.frame >= 5:
                p1.state_machine.handle_event(('STOP', None))
                p1.attack_num = 3
                p1.frame = 0
                p1.wait_time = get_time()
        if p1.attack_num == 3:
            if p1.frame >= 7:
                p1.state_machine.handle_event(('STOP', None))
                p1.attack_num = 4
                p1.frame = 0
                p1.wait_time = get_time()
        if p1.attack_num == 4:
            if p1.frame >= 6.5:
                p1.state_machine.handle_event(('STOP', None))
                p1.attack_num = 1
                p1.frame = 0
                p1.wait_time = get_time()

    @staticmethod
    def draw(p1):
        if p1.attack_num == 1:
            if p1.dir == -1:
                p1.attack1.clip_composite_draw(int(p1.frame) * 61, 0, 61, 64, 0, 'h', p1.sx-35, p1.sy, 191, 200)
            elif p1.dir == 1:
                p1.attack1.clip_composite_draw(int(p1.frame) * 61, 0, 61, 64, 0, '', p1.sx+35, p1.sy, 191, 200)
        elif p1.attack_num == 2:
            if p1.dir == -1:
                p1.attack2.clip_composite_draw(int(p1.frame) * 64, 0, 64, 64, 0, 'h', p1.sx-40, p1.sy, 200, 200)
            elif p1.dir == 1:
                p1.attack2.clip_composite_draw(int(p1.frame) * 64, 0, 64, 64, 0, '', p1.sx+40, p1.sy, 200, 200)
        elif p1.attack_num == 3:
            if p1.dir == -1:
                    p1.attack3.clip_composite_draw(int(p1.frame) * 77, 0, 77, 64, 0, 'h', p1.sx - 70, p1.sy, 241, 200)
            elif p1.dir == 1:
                    p1.attack3.clip_composite_draw(int(p1.frame) * 77, 0, 77, 64, 0, '', p1.sx + 70, p1.sy, 241, 200)
        elif p1.attack_num == 4:
            if p1.dir == -1:
                    p1.attack4.clip_composite_draw(int(p1.frame) * 72, 0, 72, 66, 0, 'h', p1.sx - 62, p1.sy+3, 225, 206)
            elif p1.dir == 1:
                    p1.attack4.clip_composite_draw(int(p1.frame) * 72, 0, 72, 66, 0, '', p1.sx + 62, p1.sy+3, 225, 206)

class Run_Attack:
    @staticmethod
    def enter(p1, e):
        p1.frame = 0
        p1.attack_num = 'run'
        p1.attack()

    @staticmethod
    def exit(p1, e):
        p1.attack_num = 1
        p1.frame = 0
    @staticmethod
    def do(p1):
        p1.frame = p1.frame + 6 * 3 * game_framework.frame_time
        if p1.frame >= 5.9:
            p1.state_machine.handle_event(('STOP', None))
        p1.x += p1.dir * RUN_SPEED_PPS * 1 * game_framework.frame_time

    @staticmethod
    def draw(p1):
        if p1.dir == -1:
            p1.run_attack.clip_composite_draw(int(p1.frame) * 79, 0, 79, 64, 0, 'h', p1.sx-35, p1.sy, 247, 200)
        elif p1.dir == 1:
            p1.run_attack.clip_composite_draw(int(p1.frame) * 79, 0, 79, 64, 0, '', p1.sx+35, p1.sy, 247, 200)

class Jump_Attack:
    @staticmethod
    def enter(p1, e):
        p1.frame = 0
        p1.attack_num = 'jump'
        p1.attack()

    @staticmethod
    def exit(p1, e):
        p1.attack_num = 1
        p1.frame = 2

    @staticmethod
    def do(p1):
        p1.frame = p1.frame + 5 * 3.5 * game_framework.frame_time
        if p1.frame >= 4.9:
            p1.state_machine.handle_event(('STOP', None))

    @staticmethod
    def draw(p1):
        if p1.dir == -1:
            p1.jump_attack.clip_composite_draw(int(p1.frame) * 56, 0, 56, 64, 0, 'h', p1.sx, p1.sy, 175, 200)
        elif p1.dir == 1:
            p1.jump_attack.clip_composite_draw(int(p1.frame) * 56, 0, 56, 64, 0, '', p1.sx, p1.sy, 175, 200)

class Skill_motion:
    @staticmethod
    def enter(p1, e):
        if right_down(e):
            p1.right = True
        elif left_down(e):
            p1.left = True
        elif right_up(e):
            p1.right = False
        elif left_up(e):
            p1.left = False

        p1.invincible = True

        if p1.chakra_lack:
            p1.invincible = False
            p1.state_machine.cur_state = Idle
        global t_time
        t_time = get_time()



    @staticmethod
    def exit(p1, e):
        p1.invincible = False
        pass

    @staticmethod
    def do(p1):
        if p1.skill_num == 'skill1':
            p1.frame = (p1.frame + 12 * 0.8 * game_framework.frame_time) % 12
            if p1.frame >= 11:
                p1.skill()
                p1.frame = 0
                p1.state_machine.handle_event(('STOP', None))
        elif p1.skill_num == 'skill2':
            p1.frame = (p1.frame + 19 * 1.0 * game_framework.frame_time) % 19
            if int(p1.frame) == 8:
                p1.skill2_s.play()
            if p1.frame >= 8:
                p1.x += p1.dir * RUN_SPEED_PPS * 2 * game_framework.frame_time
            if p1.frame >= 18:
                p1.frame = 0
                p1.state_machine.handle_event(('STOP', None))
        elif p1.skill_num == 'shuriken':
            p1.frame = (p1.frame + 4 * 4 * game_framework.frame_time) % 4
            if p1.frame >= 3:
                p1.frame = 0
                p1.state_machine.handle_event(('STOP', None))

    @staticmethod
    def draw(p1):
        if p1.skill_num == 'skill1':
            if p1.dir == -1:
                p1.skill1.clip_composite_draw(int(p1.frame) * 37, 0, 37, 64, 0, 'h', p1.sx, p1.sy+22, 115, 200)
            elif p1.dir == 1:
                p1.skill1.clip_composite_draw(int(p1.frame) * 37, 0, 37, 64, 0, '', p1.sx, p1.sy+22, 115, 200)
        elif p1.skill_num == 'skill2':
            if p1.dir == -1:
                p1.skill2.clip_composite_draw(int(p1.frame) * 104, 0, 104, 77, 0, 'h', p1.sx, p1.sy+41, 325, 241)
            elif p1.dir == 1:
                p1.skill2.clip_composite_draw(int(p1.frame) * 104, 0, 104, 77, 0, '', p1.sx, p1.sy+41, 325, 241)
        elif p1.skill_num == 'shuriken':
            if p1.jump_state:
                if p1.dir == -1:
                    p1.shuriken_jump.clip_composite_draw(int(p1.frame) * 40, 0, 40, 64, 0, 'h', p1.sx, p1.sy, 125, 200)
                elif p1.dir == 1:
                    p1.shuriken_jump.clip_composite_draw(int(p1.frame) * 40, 0, 40, 64, 0, '', p1.sx, p1.sy, 125, 200)
            else:
                if p1.dir == -1:
                    p1.shuriken_stand.clip_composite_draw(int(p1.frame) * 40, 0, 40, 64, 0, 'h', p1.sx, p1.sy, 125, 200)
                elif p1.dir == 1:
                    p1.shuriken_stand.clip_composite_draw(int(p1.frame) * 40, 0, 40, 64, 0, '', p1.sx, p1.sy, 125, 200)

class Easy_hit:
    @staticmethod
    def enter(p1, e):
        if right_down(e):
            p1.right = True
        elif left_down(e):
            p1.left = True
        elif right_up(e):
            p1.right = False
        elif left_up(e):
            p1.left = False

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.frame = p1.frame + 2 * 5 * game_framework.frame_time
        if p1.frame >= 1.9:
            p1.frame = 0
            p1.hit_state = 0
            p1.state_machine.handle_event(('STOP', None))


    @staticmethod
    def draw(p1):
        if p1.dir == -1:
            p1.easy_hit.clip_composite_draw(int(p1.frame) * 40, 0, 40, 64, 0, 'h', p1.sx, p1.sy, 125, 200)
        elif p1.dir == 1:
            p1.easy_hit.clip_composite_draw(int(p1.frame) * 40, 0, 40, 64, 0, '', p1.sx, p1.sy, 125, 200)

class Hard_hit:
    @staticmethod
    def enter(p1, e):
        if right_down(e):
            p1.right = True
        elif left_down(e):
            p1.left = True
        elif right_up(e):
            p1.right = False
        elif left_up(e):
            p1.left = False

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.frame = p1.frame + 4 * 2 * game_framework.frame_time
        if p1.frame >= 15:
            p1.invincible = False
            p1.frame = 0
            p1.hit_state = 0
            p1.state_machine.handle_event(('STOP', None))
        if p1.frame < 2.8:
            p1.x += -p1.dir * RUN_SPEED_PPS * 1 * game_framework.frame_time
        if p1.y > ground_y and p1.frame >= 2.8:
            p1.x += -p1.dir * RUN_SPEED_PPS * 0.7 * game_framework.frame_time
            p1.y -= RUN_SPEED_PPS * game_framework.frame_time * 0.6
            if p1.y < ground_y:
                p1.y = ground_y


    @staticmethod
    def draw(p1):
        if p1.frame > 3:
            if p1.dir == -1:
                p1.hard_hit.clip_composite_draw(3 * 64, 0, 64, 40, 0, 'h', p1.sx, p1.sy - 15, 200, 125)
            elif p1.dir == 1:
                p1.hard_hit.clip_composite_draw(3 * 64, 0, 64, 40, 0, '', p1.sx, p1.sy - 15, 200, 125)
        else:
            if p1.dir == -1:
                p1.hard_hit.clip_composite_draw(int(p1.frame) * 64, 0, 64, 40, 0, 'h', p1.sx, p1.sy-15, 200, 125)
            elif p1.dir == 1:
                p1.hard_hit.clip_composite_draw(int(p1.frame) * 64, 0, 64, 40, 0, '', p1.sx, p1.sy-15, 200, 125)

class Win:
    @staticmethod
    def enter(p1, e):
        p1.frame = 0
        p1.invincible = True
        pass

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + 12 * 0.7 * game_framework.frame_time) % 12
        if p1.y > ground_y:
            p1.y -= RUN_SPEED_PPS * game_framework.frame_time * 0.6
            if p1.y < ground_y:
                p1.y = ground_y

    @staticmethod
    def draw(p1):
        if p1.dir == 1:
            p1.win_image.clip_composite_draw(int(p1.frame) * 34, 0, 34, 64, 0, '', p1.sx-10, p1.sy-6, 103, 200)
        elif p1.dir == -1:
            p1.win_image.clip_composite_draw(int(p1.frame) * 34, 0, 34, 64, 0, 'h', p1.sx + 10, p1.sy - 6, 103, 200)

class Lose:
    @staticmethod
    def enter(p1, e):
        p1.frame = 0
        p1.invincible = True
        pass

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        if p1.frame <= 3:
            p1.frame = p1.frame + 4 * 0.5 * game_framework.frame_time
        if p1.y > ground_y:
            p1.x += -p1.dir * RUN_SPEED_PPS * 0.2 * game_framework.frame_time
            p1.y -= RUN_SPEED_PPS * game_framework.frame_time * 0.15
            if p1.y < ground_y:
                p1.y = ground_y

    @staticmethod
    def draw(p1):
        if p1.dir == -1:
            p1.hard_hit.clip_composite_draw(int(p1.frame) * 64, 0, 64, 40, 0, 'h', p1.sx, p1.sy - 15, 200, 125)
        elif p1.dir == 1:
            p1.hard_hit.clip_composite_draw(int(p1.frame) * 64, 0, 64, 40, 0, '', p1.sx, p1.sy - 15, 200, 125)

class StateMachine:
    def __init__(self, p1):
        self.p1 = p1
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, right_up: Idle, left_up: Idle, run_state: Run,
                   up_down: Jump, jump_state: Jump, attack_down: Attack, shuriken_down: Skill_motion,
                   skill1_down: Skill_motion, skill2_down: Skill_motion},
            Run: {right_up: Idle, left_up: Idle, right_down: Idle, left_down: Idle, up_down: Jump, stop: Idle
                  , teleport_down: Teleport, attack_down: Run_Attack, shuriken_down: Skill_motion},
            Jump: {jump_end: Idle, jump_end_run: Run, up_down: Jump, up_up: Jump, down_down: Jump, down_up: Jump,
                   teleport_down: Teleport, shuriken_down: Skill_motion, attack_down: Jump_Attack,
                   right_down: Jump, left_down: Jump, right_up: Jump, left_up: Jump},
            Teleport: {right_down: Teleport, left_down: Teleport, right_up: Teleport, left_up: Teleport,
                       teleport: Idle},
            Attack: {stop: Idle, right_down: Attack, left_down: Attack, right_up: Attack, left_up: Attack},
            Run_Attack: {stop: Idle},
            Jump_Attack: {stop: Jump},
            Easy_hit: {stop: Idle}, Hard_hit: {stop: Idle},
            Skill_motion: {stop: Idle, right_up: Skill_motion, left_up: Skill_motion,
                           right_down: Skill_motion, left_down: Skill_motion},
            Win: {stop: Idle}, Lose: {stop: Idle}
        }

    def start(self):
        self.cur_state.enter(self.p1, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.p1)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.p1, e)
                self.cur_state = next_state
                self.cur_state.enter(self.p1, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.p1)


class SASUKE:
    global skill_num
    def __init__(self, p_num):
        self.x, self.y = 400, ground_y
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
        if self.skill_num == 'shuriken':
            self.attack_s_1.play()
            shuriken = Shuriken(self.x, self.y + 10, self.dir)
            game_world.add_object(shuriken, 2)
            if player_num == 1:
                game_world.add_collision_pair('p2:p1_shuriken', None, shuriken)
            elif player_num == 2:
                game_world.add_collision_pair('p1:p2_shuriken', None, shuriken)
        elif self.skill_num == 'skill1':
            self.skill1_s_e.play()
            skill1 = Skill1(self.x, self.y, self.dir)
            game_world.add_object(skill1, 2)
            if player_num == 1:
                game_world.add_collision_pair('p2:p1_skill1', None, skill1)
            elif player_num == 2:
                game_world.add_collision_pair('p1:p2_skill1', None, skill1)
        elif self.skill_num == 'skill2':
            skill2 = Skill2(self.x, self.y, self.dir)
            game_world.add_object(skill2, 2)
            if player_num == 1:
                game_world.add_collision_pair('p2:p1_skill2', None, skill2)
            elif player_num == 2:
                game_world.add_collision_pair('p1:p2_skill2', None, skill2)

    def attack(self):
        attack_range = Attack_range(self.x, self.y, self.dir, self.attack_num)
        game_world.add_object(attack_range, 2)
        if self.attack_num == 2 or self.attack_num == 'jump':
            self.attack_s_1.play()
        if self.attack_num == 4 or self.attack_num == 'run':
            self.attack_s_2.play()
        if player_num == 1:
            game_world.add_collision_pair('p2:p1_attack', None, attack_range)
        elif player_num == 2:
            game_world.add_collision_pair('p1:p2_attack', None, attack_range)

    def set_background(self, bg):
        self.bg = bg
        # self.x = self.bg.w / 2
        # self.y = self.bg.h / 2
    def update(self):
        if self.hit_state == 'hard':
            if not self.state_machine.cur_state == Hard_hit:
                self.hard_hit_s.play()
            self.state_machine.cur_state = Hard_hit
            self.hit_state = 0
        if self.hit_state == 'easy':
            self.easy_hit_s.play()
            self.state_machine.cur_state = Easy_hit
            self.hit_state = 0
        self.state_machine.update()
        if self.chakra <= 100:
            self.chakra += 4 * game_framework.frame_time
        self.x = clamp(50.0, self.x, self.bg.w - 50.0)
        self.y = clamp(50.0, self.y, self.bg.h - 50.0)


    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        if right_up(('INPUT', event)):
            self.right = False
        if left_up(('INPUT', event)):
            self.left = False
        if right_down(('INPUT', event)):
            self.right = True
        if left_down(('INPUT', event)):
            self.left = True

    def draw(self):
        self.sx, self.sy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        self.state_machine.draw()
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.sx - 30, self.sy - 70, self.sx + 30, self.sy + 70

    def handle_collision(self, group, other):
        pass