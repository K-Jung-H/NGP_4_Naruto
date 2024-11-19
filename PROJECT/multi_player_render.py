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
            if not p1.dir:
                p1.idle.clip_composite_draw(int(p1.frame) * 32, 0, 32, 48, 0, 'h', p1.sx, p1.sy - 15, 90, 135)
            else:
                p1.idle.clip_composite_draw(int(p1.frame) * 32, 0, 32, 48, 0, '', p1.sx, p1.sy - 15, 90, 135)
        elif p1.char_name == 'sasuke':
            if not p1.dir:
                p1.idle.clip_composite_draw(int(p1.frame) * 32, 0, 32, 64, 0, 'h', p1.sx+10, p1.sy, 100, 200)
            else:
                p1.idle.clip_composite_draw(int(p1.frame) * 32, 0, 32, 64, 0, '', p1.sx-10, p1.sy, 100, 200)
        elif p1.char_name == 'itachi':
            if not p1.dir:
                p1.idle.clip_composite_draw(int(p1.frame) * 32, 0, 32, 64, 0, 'h', p1.sx, p1.sy + 15, 100, 200)
            else:
                p1.idle.clip_composite_draw(int(p1.frame) * 32, 0, 32, 64, 0, '', p1.sx, p1.sy + 15, 100, 200)

class Run:

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
            if not p1.dir:
                p1.run.clip_composite_draw(int(p1.frame) * 48, 0, 48, 48, 0, 'h', p1.sx, p1.sy-15, 135, 135)
            else:
                p1.run.clip_composite_draw(int(p1.frame) * 48, 0, 48, 48, 0, '', p1.sx, p1.sy-15, 135, 135)
        elif p1.char_name == 'sasuke':
            if not p1.dir:
                p1.run.clip_composite_draw(int(p1.frame) * 64, 0, 64, 32, 0, 'h', p1.sx, p1.sy - 15, 200, 100)
            else:
                p1.run.clip_composite_draw(int(p1.frame) * 64, 0, 64, 32, 0, '', p1.sx, p1.sy - 15, 200, 100)
        elif p1.char_name == 'itachi':
            if not p1.dir:
                p1.run.clip_composite_draw(int(p1.frame) * 50, 0, 50, 48, 0, 'h', p1.sx, p1.sy - 10, 153, 150)
            else:
                p1.run.clip_composite_draw(int(p1.frame) * 50, 0, 50, 48, 0, '', p1.sx, p1.sy - 10, 153, 150)


class Jump:
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
            if not p1.dir:
                if int(p1.frame) < 2:
                    p1.jump.clip_composite_draw(int(p1.frame) * 32, 0, 32, 48, 0, 'h', p1.sx, p1.sy, 90, 135)
                else:
                    p1.jump.clip_composite_draw(64 + (int(p1.frame) - 2) * 40, 0, 40, 48, 0, 'h', p1.sx, p1.sy, 112, 135)
            else:
                if int(p1.frame) < 2:
                    p1.jump.clip_composite_draw(int(p1.frame) * 32, 0, 32, 48, 0, '', p1.sx, p1.sy, 90, 135)
                else:
                    p1.jump.clip_composite_draw(64 + (int(p1.frame) - 2) * 40, 0, 40, 48, 0, '', p1.sx, p1.sy, 112, 135)
        elif p1.char_name == 'sasuke':
            if not p1.dir:
                p1.jump.clip_composite_draw(int(p1.frame) * 32, 0, 32, 64, 0, 'h', p1.sx, p1.sy, 100, 200)
            else:
                p1.jump.clip_composite_draw(int(p1.frame) * 32, 0, 32, 64, 0, '', p1.sx, p1.sy, 100, 200)
        elif p1.char_name == 'itachi':
            if not p1.dir:
                p1.jump.clip_composite_draw(int(p1.frame) * 50, 0, 50, 64, 0, 'h', p1.sx, p1.sy, 153, 200)
            else:
                p1.jump.clip_composite_draw(int(p1.frame) * 50, 0, 50, 64, 0, '', p1.sx, p1.sy, 153, 200)

class Attack:
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
            if p1.attack_num == 1:
                if not p1.dir:
                    p1.attack1.clip_composite_draw(int(p1.frame) * 56, 0, 56, 48, 0, 'h', p1.sx - 10, p1.sy - 15, 158, 135)
                else:
                    p1.attack1.clip_composite_draw(int(p1.frame) * 56, 0, 56, 48, 0, '', p1.sx + 10, p1.sy - 15, 158, 135)
            elif p1.attack_num == 2:
                if not p1.dir:
                    p1.attack2.clip_composite_draw(int(p1.frame) * 48, 0, 48, 48, 0, 'h', p1.sx-10, p1.sy - 15, 135, 135)
                else:
                    p1.attack2.clip_composite_draw(int(p1.frame) * 48, 0, 48, 48, 0, '', p1.sx+10, p1.sy - 15, 135, 135)
            elif p1.attack_num == 3:
                if not p1.dir:
                        p1.attack3.clip_composite_draw(int(p1.frame) * 48, 0, 48, 48, 0, 'h', p1.sx - 10, p1.sy-15, 135, 135)
                else:
                        p1.attack3.clip_composite_draw(int(p1.frame) * 48, 0, 48, 48, 0, '', p1.sx + 10, p1.sy-15, 135, 135)
            elif p1.attack_num == 4:
                if not p1.dir:
                        p1.attack4.clip_composite_draw(int(p1.frame) * 40, 0, 40, 56, 0, 'h', p1.sx, p1.sy, 113, 158)
                else:
                        p1.attack4.clip_composite_draw(int(p1.frame) * 40, 0, 40, 56, 0, '', p1.sx, p1.sy, 113, 158)
        elif p1.char_name == 'sasuke':
            if p1.attack_num == 1:
                if not p1.dir:
                    p1.attack1.clip_composite_draw(int(p1.frame) * 61, 0, 61, 64, 0, 'h', p1.sx - 35, p1.sy, 191, 200)
                else:
                    p1.attack1.clip_composite_draw(int(p1.frame) * 61, 0, 61, 64, 0, '', p1.sx + 35, p1.sy, 191, 200)
            elif p1.attack_num == 2:
                if not p1.dir:
                    p1.attack2.clip_composite_draw(int(p1.frame) * 64, 0, 64, 64, 0, 'h', p1.sx - 40, p1.sy, 200, 200)
                else:
                    p1.attack2.clip_composite_draw(int(p1.frame) * 64, 0, 64, 64, 0, '', p1.sx + 40, p1.sy, 200, 200)
            elif p1.attack_num == 3:
                if not p1.dir:
                    p1.attack3.clip_composite_draw(int(p1.frame) * 77, 0, 77, 64, 0, 'h', p1.sx - 70, p1.sy, 241, 200)
                else:
                    p1.attack3.clip_composite_draw(int(p1.frame) * 77, 0, 77, 64, 0, '', p1.sx + 70, p1.sy, 241, 200)
            elif p1.attack_num == 4:
                if not p1.dir:
                    p1.attack4.clip_composite_draw(int(p1.frame) * 72, 0, 72, 66, 0, 'h', p1.sx - 62, p1.sy + 3, 225,
                                                   206)
                else:
                    p1.attack4.clip_composite_draw(int(p1.frame) * 72, 0, 72, 66, 0, '', p1.sx + 62, p1.sy + 3, 225,
                                                   206)
        elif p1.char_name == 'itachi':
            if p1.attack_num == 1:
                if not p1.dir:
                    p1.attack1.clip_composite_draw(int(p1.frame) * 42, 0, 42, 64, 0, 'h', p1.sx, p1.sy - 15, 131, 200)
                else:
                    p1.attack1.clip_composite_draw(int(p1.frame) * 42, 0, 42, 64, 0, '', p1.sx, p1.sy - 15, 131, 200)
            elif p1.attack_num == 2:
                if not p1.dir:
                    p1.attack2.clip_composite_draw(int(p1.frame) * 58, 0, 58, 72, 0, 'h', p1.sx - 40, p1.sy, 181, 225)
                else:
                    p1.attack2.clip_composite_draw(int(p1.frame) * 58, 0, 58, 72, 0, '', p1.sx + 40, p1.sy, 181, 225)
            elif p1.attack_num == 3:
                if not p1.dir:
                    p1.attack3.clip_composite_draw(int(p1.frame) * 74, 0, 74, 72, 0, 'h', p1.sx - 40, p1.sy, 227, 225)
                else:
                    p1.attack3.clip_composite_draw(int(p1.frame) * 74, 0, 74, 72, 0, '', p1.sx + 40, p1.sy, 227, 225)
            elif p1.attack_num == 4:
                if not p1.dir:
                    p1.attack4.clip_composite_draw(int(p1.frame) * 42, 0, 42, 72, 0, 'h', p1.sx - 20, p1.sy + 15, 131,
                                                   225)
                else:
                    p1.attack4.clip_composite_draw(int(p1.frame) * 42, 0, 42, 72, 0, '', p1.sx + 20, p1.sy + 15, 131,
                                                   225)

class Skill_motion:
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
            if p1.skill_num == 'skill1':
                print(p1.frame)
                if p1.dir:
                    p1.skill1.clip_composite_draw(int(p1.frame) * 193, 0, 193, 136, 0, '', p1.sx + 60, p1.sy + 70, 543,
                                                  382)
                else:
                    p1.skill1.clip_composite_draw(int(p1.frame) * 193, 0, 193, 136, 0, 'h', p1.sx - 60, p1.sy + 70, 543,
                                                  382)
            elif p1.skill_num == 'skill2':
                if p1.dir:
                    p1.skill2.clip_composite_draw(int(p1.frame) * 83, 0, 83, 50, 0, '', p1.sx + 20, p1.sy - 15, 233,
                                                  140)
                else:
                    p1.skill2.clip_composite_draw(int(p1.frame) * 83, 0, 83, 50, 0, 'h', p1.sx - 20, p1.sy - 15, 233,
                                                  140)
            elif p1.skill_num == 'shuriken':
                # if p1.jump_state:
                #     if p1.dir == -1:
                #         p1.shuriken_jump.clip_composite_draw(int(p1.frame) * 40, 0, 40, 64, 0, 'h', p1.sx, p1.sy - 30,
                #                                              112, 180)
                #     elif p1.dir == 1:
                #         p1.shuriken_jump.clip_composite_draw(int(p1.frame) * 40, 0, 40, 64, 0, '', p1.sx, p1.sy - 30,
                #                                              112, 180)
                # else:
                if p1.dir:
                    p1.shuriken_stand.clip_composite_draw(int(p1.frame) * 40, 0, 40, 48, 0, '', p1.sx + 10,
                                                          p1.sy - 15, 112, 135)
                else:
                    p1.shuriken_stand.clip_composite_draw(int(p1.frame) * 40, 0, 40, 48, 0, 'h', p1.sx - 10,
                                                          p1.sy - 15, 112, 135)
        elif p1.char_name == 'sasuke':
            if p1.skill_num == 'skill1':
                if p1.dir:
                    p1.skill1.clip_composite_draw(int(p1.frame) * 37, 0, 37, 64, 0, '', p1.sx, p1.sy+22, 115, 200)
                else:
                    p1.skill1.clip_composite_draw(int(p1.frame) * 37, 0, 37, 64, 0, 'h', p1.sx, p1.sy+22, 115, 200)
            elif p1.skill_num == 'skill2':
                if p1.dir:
                    p1.skill2.clip_composite_draw(int(p1.frame) * 104, 0, 104, 77, 0, '', p1.sx, p1.sy+41, 325, 241)
                else:
                    p1.skill2.clip_composite_draw(int(p1.frame) * 104, 0, 104, 77, 0, 'h', p1.sx, p1.sy+41, 325, 241)
            elif p1.skill_num == 'shuriken':
                # if p1.jump_state:
                #     if p1.dir == -1:
                #         p1.shuriken_jump.clip_composite_draw(int(p1.frame) * 40, 0, 40, 64, 0, 'h', p1.sx, p1.sy, 125, 200)
                #     elif p1.dir == 1:
                #         p1.shuriken_jump.clip_composite_draw(int(p1.frame) * 40, 0, 40, 64, 0, '', p1.sx, p1.sy, 125, 200)
                # else:
                if p1.dir:
                    p1.shuriken_stand.clip_composite_draw(int(p1.frame) * 40, 0, 40, 64, 0, '', p1.sx, p1.sy, 125, 200)
                else:
                    p1.shuriken_stand.clip_composite_draw(int(p1.frame) * 40, 0, 40, 64, 0, 'h', p1.sx, p1.sy, 125, 200)
        elif p1.char_name == 'itachi':
            if p1.skill_num == 'skill1':
                if p1.dir:
                    p1.skill1.clip_composite_draw(int(p1.frame) * 170, 0, 170, 152, 0, '', p1.sx + 60, p1.sy - 25, 531,
                                                  475)
                else:
                    p1.skill1.clip_composite_draw(int(p1.frame) * 170, 0, 170, 152, 0, 'h', p1.sx - 60, p1.sy - 25, 531,
                                                  475)
            elif p1.skill_num == 'skill2':
                if p1.dir:
                    p1.skill2.clip_composite_draw(int(p1.frame) * 42, 0, 42, 72, 0, '', p1.sx - 10, p1.sy + 5, 90, 155)
                else:
                    p1.skill2.clip_composite_draw(int(p1.frame) * 42, 0, 42, 72, 0, 'h', p1.sx + 10, p1.sy + 5, 90, 155)
            elif p1.skill_num == 'shuriken':
                # if p1.jump_state:
                #     if p1.dir == -1:
                #         p1.shuriken_jump.clip_composite_draw(int(p1.frame) * 42, 0, 42, 56, 0, 'h', p1.sx, p1.sy - 25,
                #                                              131, 175)
                #     elif p1.dir == 1:
                #         p1.shuriken_jump.clip_composite_draw(int(p1.frame) * 42, 0, 42, 56, 0, '', p1.sx, p1.sy - 25,
                #                                              131, 175)
                # else:
                if p1.dir:
                    p1.shuriken_stand.clip_composite_draw(int(p1.frame) * 50, 0, 50, 64, 0, '', p1.sx - 15,
                                                          p1.sy + 15, 156, 200)
                else:
                    p1.shuriken_stand.clip_composite_draw(int(p1.frame) * 50, 0, 50, 64, 0, 'h', p1.sx + 15,
                                                          p1.sy + 15, 156, 200)

class Easy_hit:
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
            if not p1.dir:
                p1.easy_hit.clip_composite_draw(int(p1.frame) * 40, 0, 40, 48, 0, 'h', p1.sx, p1.sy - 15, 112, 135)
            else:
                p1.easy_hit.clip_composite_draw(int(p1.frame) * 40, 0, 40, 48, 0, '', p1.sx, p1.sy - 15, 112, 135)
        elif p1.char_name == 'sasuke':
            if not p1.dir:
                p1.easy_hit.clip_composite_draw(int(p1.frame) * 40, 0, 40, 64, 0, 'h', p1.sx, p1.sy, 125, 200)
            else:
                p1.easy_hit.clip_composite_draw(int(p1.frame) * 40, 0, 40, 64, 0, '', p1.sx, p1.sy, 125, 200)
        elif p1.char_name == 'itachi':
            if not p1.dir:
                p1.easy_hit.clip_composite_draw(int(p1.frame) * 43, 0, 43, 64, 0, 'h', p1.sx + 15, p1.sy + 15, 134, 200)
            else:
                p1.easy_hit.clip_composite_draw(int(p1.frame) * 43, 0, 43, 64, 0, '', p1.sx - 15, p1.sy + 15, 134, 200)

class Hard_hit:
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
            if p1.frame > 3:
                if not p1.dir:
                    p1.hard_hit.clip_composite_draw(3 * 48, 0, 48, 40, 0, 'h', p1.sx, p1.sy - 15, 135, 112)
                else:
                    p1.hard_hit.clip_composite_draw(3 * 48, 0, 48, 40, 0, '', p1.sx, p1.sy - 15, 135, 112)
            else:
                if not p1.dir:
                    p1.hard_hit.clip_composite_draw(int(p1.frame) * 48, 0, 48, 40, 0, 'h', p1.sx, p1.sy - 15, 135, 112)
                else:
                    p1.hard_hit.clip_composite_draw(int(p1.frame) * 48, 0, 48, 40, 0, '', p1.sx, p1.sy - 15, 135, 112)
        elif p1.char_name == 'sasuke':
            if p1.frame > 3:
                if not p1.dir:
                    p1.hard_hit.clip_composite_draw(3 * 64, 0, 64, 40, 0, 'h', p1.sx, p1.sy - 15, 200, 125)
                else:
                    p1.hard_hit.clip_composite_draw(3 * 64, 0, 64, 40, 0, '', p1.sx, p1.sy - 15, 200, 125)
            else:
                if not p1.dir:
                    p1.hard_hit.clip_composite_draw(int(p1.frame) * 64, 0, 64, 40, 0, 'h', p1.sx, p1.sy-15, 200, 125)
                else:
                    p1.hard_hit.clip_composite_draw(int(p1.frame) * 64, 0, 64, 40, 0, '', p1.sx, p1.sy-15, 200, 125)
        elif p1.char_name == 'itachi':
            if p1.frame > 3:
                if not p1.dir:
                    p1.hard_hit.clip_composite_draw(3 * 66, 0, 66, 40, 0, 'h', p1.sx, p1.sy - 15, 206, 125)
                else:
                    p1.hard_hit.clip_composite_draw(3 * 66, 0, 66, 40, 0, '', p1.sx, p1.sy - 15, 206, 125)
            else:
                if not p1.dir:
                    p1.hard_hit.clip_composite_draw(int(p1.frame) * 66, 0, 66, 40, 0, 'h', p1.sx, p1.sy - 15, 206, 125)
                else:
                    p1.hard_hit.clip_composite_draw(int(p1.frame) * 66, 0, 66, 40, 0, '', p1.sx, p1.sy - 15, 206, 125)

class Win:
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
            p1.win_image.clip_composite_draw(int(p1.frame) * 50, 0, 50, 64, 0, '', p1.sx, p1.sy, 140, 180)
        elif p1.char_name == 'sasuke':
            if p1.dir:
                p1.win_image.clip_composite_draw(int(p1.frame) * 34, 0, 34, 64, 0, '', p1.sx-10, p1.sy-6, 103, 200)
            else:
                p1.win_image.clip_composite_draw(int(p1.frame) * 34, 0, 34, 64, 0, 'h', p1.sx + 10, p1.sy - 6, 103, 200)
        elif p1.char_name == 'itachi':
            if p1.dir:
                p1.win_image.clip_composite_draw(int(p1.frame) * 42, 0, 42, 74, 0, '', p1.sx, p1.sy, 90, 159)
            else:
                p1.win_image.clip_composite_draw(int(p1.frame) * 42, 0, 42, 74, 0, 'h', p1.sx, p1.sy, 90, 159)

class Lose:
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
            if not p1.dir:
                p1.hard_hit.clip_composite_draw(int(p1.frame) * 48, 0, 48, 40, 0, 'h', p1.sx, p1.sy - 15, 135, 112)
            else:
                p1.hard_hit.clip_composite_draw(int(p1.frame) * 48, 0, 48, 40, 0, '', p1.sx, p1.sy - 15, 135, 112)
        elif p1.char_name == 'sasuke':
            if not p1.dir:
                p1.hard_hit.clip_composite_draw(int(p1.frame) * 64, 0, 64, 40, 0, 'h', p1.sx, p1.sy - 15, 200, 125)
            else:
                p1.hard_hit.clip_composite_draw(int(p1.frame) * 64, 0, 64, 40, 0, '', p1.sx, p1.sy - 15, 200, 125)
        elif p1.char_name == 'itachi':
            if not p1.dir:
                p1.hard_hit.clip_composite_draw(int(p1.frame) * 64, 0, 64, 40, 0, 'h', p1.sx, p1.sy - 15, 200, 125)
            else:
                p1.hard_hit.clip_composite_draw(int(p1.frame) * 64, 0, 64, 40, 0, '', p1.sx, p1.sy - 15, 200, 125)

class Run_Attack:
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
            if not p1.dir:
                p1.run_attack.clip_composite_draw(int(p1.frame) * 40, 0, 40, 48, 0, 'h', p1.sx, p1.sy-15, 113, 135)
            else:
                p1.run_attack.clip_composite_draw(int(p1.frame) * 40, 0, 40, 48, 0, '', p1.sx, p1.sy-15, 113, 135)
        elif p1.char_name == 'sasuke':
            if not p1.dir:
                p1.run_attack.clip_composite_draw(int(p1.frame) * 79, 0, 79, 64, 0, 'h', p1.sx - 35, p1.sy, 247, 200)
            else:
                p1.run_attack.clip_composite_draw(int(p1.frame) * 79, 0, 79, 64, 0, '', p1.sx + 35, p1.sy, 247, 200)
        elif p1.char_name == 'itachi':
            if not p1.dir:
                p1.run_attack.clip_composite_draw(int(p1.frame) * 66, 0, 66, 49, 0, 'h', p1.sx - 50, p1.sy, 206, 153)
            else:
                p1.run_attack.clip_composite_draw(int(p1.frame) * 66, 0, 66, 49, 0, '', p1.sx + 50, p1.sy, 206, 153)

class Jump_Attack:
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
            if not p1.dir:
                p1.jump_attack.clip_composite_draw(int(p1.frame) * 48, 0, 48, 52, 0, 'h', p1.sx, p1.sy, 135, 146)
            else:
                p1.jump_attack.clip_composite_draw(int(p1.frame) * 48, 0, 48, 52, 0, '', p1.sx, p1.sy, 135, 146)
        elif p1.char_name == 'sasuke':
            if not p1.dir:
                p1.jump_attack.clip_composite_draw(int(p1.frame) * 56, 0, 56, 64, 0, 'h', p1.sx, p1.sy, 175, 200)
            else:
                p1.jump_attack.clip_composite_draw(int(p1.frame) * 56, 0, 56, 64, 0, '', p1.sx, p1.sy, 175, 200)
        elif p1.char_name == 'itachi':
            if not p1.dir:
                p1.jump_attack.clip_composite_draw(int(p1.frame) * 50, 0, 50, 48, 0, 'h', p1.sx, p1.sy, 156, 150)
            else:
                p1.jump_attack.clip_composite_draw(int(p1.frame) * 50, 0, 50, 48, 0, '', p1.sx, p1.sy, 156, 150)

class Teleport:
    @staticmethod
    def enter(p1, e):
        # p1.attack_s_1.play()
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
            if not p1.dir:
                p1.teleport.clip_composite_draw(int(p1.frame) * 32, 0, 32, 56, 0, 'h', p1.sx, p1.sy, 90, 158)
                p1.teleport_motion.clip_composite_draw(int(p1.frame) * 72, 0, 72, 75, 0, 'h', p1.sx, p1.sy, 150, 250)
            else:
                p1.teleport.clip_composite_draw(int(p1.frame) * 32, 0, 32, 56, 0, '', p1.sx, p1.sy, 90, 158)
                p1.teleport_motion.clip_composite_draw(int(p1.frame) * 72, 0, 72, 75, 0, '', p1.sx, p1.sy, 150, 250)
        elif p1.char_name == 'sasuke':
            if not p1.dir:
                p1.teleport.clip_composite_draw(int(p1.frame) * 32, 0, 32, 64, 0, 'h', p1.sx, p1.sy, 100, 200)
                p1.teleport_motion.clip_composite_draw(int(p1.frame) * 72, 0, 72, 75, 0, 'h', p1.sx, p1.sy, 150, 250)
            else:
                p1.teleport.clip_composite_draw(int(p1.frame) * 32, 0, 32, 64, 0, '', p1.sx, p1.sy, 100, 200)
                p1.teleport_motion.clip_composite_draw(int(p1.frame) * 72, 0, 72, 75, 0, '', p1.sx, p1.sy, 150, 250)
        elif p1.char_name == 'itachi':
            if not p1.dir:
                p1.teleport.clip_composite_draw(int(p1.frame) * 40, 0, 40, 66, 0, 'h', p1.sx, p1.sy, 125, 202)
                p1.teleport_motion.clip_composite_draw(int(p1.frame) * 72, 0, 72, 75, 0, 'h', p1.sx, p1.sy, 150, 250)
            else:
                p1.teleport.clip_composite_draw(int(p1.frame) * 40, 0, 40, 66, 0, '', p1.sx, p1.sy, 125, 202)
                p1.teleport_motion.clip_composite_draw(int(p1.frame) * 72, 0, 72, 75, 0, '', p1.sx, p1.sy, 150, 250)

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
        self.x = clamp(50.0, self.x, self.bg.w - 50.0)
        self.y = clamp(50.0, self.y, self.bg.h - 50.0)
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
        self.x = clamp(50.0, self.x, self.bg.w - 50.0)
        self.y = clamp(50.0, self.y, self.bg.h - 50.0)
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

class ITACHI_MULTI:
    global skill_num
    def __init__(self, p_num):
        self.x, self.y = 400, 0
        self.frame = 0
        self.dir = 1
        self.idle = load_image('resource/itachi_idle.png')
        self.run = load_image('resource/itachi_run.png')
        self.jump = load_image('resource/itachi_jump.png')
        self.teleport = load_image('resource/itachi_teleport.png')
        self.teleport_motion = load_image('resource/teleport.png')
        self.attack1 = load_image('resource/itachi_attack1.png')
        self.attack2 = load_image('resource/itachi_attack2.png')
        self.attack3 = load_image('resource/itachi_attack3.png')
        self.attack4 = load_image('resource/itachi_attack4.png')
        self.shuriken_stand = load_image('resource/itachi_shuriken_stand.png')
        self.shuriken_jump = load_image('resource/itachi_shuriken_jump.png')
        self.skill1 = load_image('resource/itachi_skill1.png')
        self.skill2 = load_image('resource/itachi_skill2.png')
        self.run_attack = load_image('resource/itachi_run_attack.png')
        self.jump_attack = load_image('resource/itachi_jump_attack.png')
        self.easy_hit = load_image('resource/itachi_easy_hit.png')
        self.hard_hit = load_image('resource/itachi_hard_hit.png')
        self.win_image = load_image('resource/itachi_win.png')
        self.attack_s_1 = load_wav('sound/itachi_attack1.wav')
        self.attack_s_1.set_volume(10)
        self.attack_s_2 = load_wav('sound/itachi_attack2.wav')
        self.attack_s_2.set_volume(10)
        self.easy_hit_s = load_wav('sound/itachi_easy_hit.wav')
        self.easy_hit_s.set_volume(10)
        self.hard_hit_s = load_wav('sound/itachi_hard_hit.wav')
        self.hard_hit_s.set_volume(10)
        self.skill1_s = load_wav('sound/itachi_skill1.wav')
        self.skill1_s.set_volume(10)
        self.skill2_s = load_wav('sound/itachi_skill2.wav')
        self.skill2_s.set_volume(10)
        self.skill1_s_e = load_wav('sound/itachi_skill1_effect.wav')
        self.skill1_s_e.set_volume(10)
        self.win_s = load_wav('sound/itachi_win.wav')
        self.win_s.set_volume(10)
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
        self.char_name = 'itachi'

    def skill(self):
        pass

    def attack(self):
        pass

    def set_background(self, bg):
        self.bg = bg
        # self.x = self.bg.w / 2
        # self.y = self.bg.h / 2

    def update(self):
        self.x = clamp(50.0, self.x, self.bg.w - 50.0)
        self.y = clamp(50.0, self.y, self.bg.h - 50.0)


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