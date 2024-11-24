from pico2d import *
import game_framework
import play_mode
import round1
import title_mode

character_count = 3

def init():
    global image1, naruto, sasuke, itachi
    global p1_x, p1_y, p2_x, p2_y, p1_choose, p2_choose, p1_image, p2_image, character_back
    global vs, press_space
    global naruto_frame, sasuke_frame, itachi_frame, space_frame, space_up
    global duplicate, dup_on, dup_wait_time, dir_image
    global naruto_back, sasuke_back, naruto_logo, sasuke_logo, itachi_back
    global itachi_logo
    image1 = load_image('resource/title_main.png')
    naruto = load_image('resource/naruto_idle.png')
    sasuke = load_image('resource/sasuke_idle.png')
    itachi = load_image('resource/itachi_idle.png')
    p1_image = load_image('resource/p1_image.png')
    # p2_image = load_image('resource/p2_image.png')
    character_back = load_image('resource/charactor_back.png')
    # vs = load_image('resource/vs.png')
    press_space = load_image('resource/press_space.png')
    # duplicate = load_image('resource/duplicate.png')
    dir_image = load_image('resource/dir_image.png')
    naruto_back = load_image('resource/naruto_back.png')
    sasuke_back = load_image('resource/sasuke_back.png')
    itachi_back = load_image('resource/itachi_back.png')
    naruto_logo = load_image('resource/naruto_logo1.png')
    sasuke_logo = load_image('resource/sasuke_logo.png')
    itachi_logo = load_image('resource/itachi_logo.png')

    p1_x = 600
    p1_y = 360
    # p2_x = 300
    # p2_y = 360
    p1_choose = 1
    # p2_choose = 3
    naruto_frame, sasuke_frame, itachi_frame = 0, 0, 0
    space_frame = 0
    space_up = True
    dup_on = False
    dup_wait_time = 0
def finish():
    global image1, naruto, sasuke, itachi, character_back, press_space, dir_image, p1_image
    del image1, naruto, sasuke, itachi, character_back, press_space, dir_image, p1_image
def handle_events():
    events = get_events()
    global p1_choose, p2_choose, character_count, dup_on, dup_wait_time
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            # if p1_choose != p2_choose:
            play_mode.round_num = 1
            # game_framework.change_mode(play_mode)
            game_framework.change_mode(round1)
            # else:
            #     dup_on = True
            #     dup_wait_time = get_time()
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
        #     p2_choose = (p2_choose - 1) % character_count
        #     if p2_choose == 0:
        #         p2_choose = character_count
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
        #     p2_choose = (p2_choose + 1) % character_count
        #     if p2_choose == 0:
        #         p2_choose = character_count
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            p1_choose = (p1_choose - 1) % character_count
            if p1_choose == 0:
                p1_choose = character_count
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            p1_choose = (p1_choose + 1) % character_count
            if p1_choose == 0:
                p1_choose = character_count
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F1:
            game_framework.change_mode(title_mode)

def running():
    pass
def draw():
    clear_canvas()
    image1.clip_composite_draw(0, 0, 900, 507, 0, '', 600, 300, 1200, 600)
    # vs.clip_composite_draw(0, 0, 2500, 2500, 0, '', 600, 300, 200, 200)

    # character_back.clip_composite_draw(0, 0, 64, 76, 0, '', 900, 300, 340, 430)
    # p1_image.clip_composite_draw(0, 0, 64, 32, 0, '', 900, 500, 120, 60)
    # p2_image.clip_composite_draw(0, 0, 64, 32, 0, '', 300, 500, 120, 60)
    dir_image.clip_composite_draw(0, 0, dir_image.w, dir_image.h, 0, '', 600 + 160, 370, dir_image.w, dir_image.h)
    dir_image.clip_composite_draw(0, 0, dir_image.w, dir_image.h, 0, 'h', 600 - 160, 370, dir_image.w, dir_image.h)
    if p1_choose == 1:
        naruto_back.clip_composite_draw(0, 0, naruto_back.w, naruto_back.h, 0, 'h', 600, 330,
                                        naruto_back.w*3.5, naruto_back.h*3.5)
        naruto.clip_composite_draw(int(naruto_frame)*32, 0, 32, 48, 0, 'h', p1_x, p1_y, 100, 150)
        naruto_logo.clip_composite_draw(0, 0, naruto_logo.w, naruto_logo.h, 0, 'h', 600 - 70, 330 - 90,
                                        naruto_logo.w * 0.1, naruto_logo.h * 0.1)
        # naruto_s1.clip_composite_draw(8 * 193, 0, 193, 136, 0, '', p1_x - 80, p1_y-110, 543*0.2, 382*0.2)
    elif p1_choose == 2:
        sasuke_back.clip_composite_draw(0, 0, sasuke_back.w, sasuke_back.h, 0, 'h', 600, 330,
                                        sasuke_back.w * 3.5, sasuke_back.h * 3.5)
        sasuke.clip_composite_draw(int(sasuke_frame)*32, 0, 32, 64, 0, 'h', p1_x+10, p1_y, 100, 200)
        sasuke_logo.clip_composite_draw(0, 0, sasuke_logo.w, sasuke_logo.h, 0, 'h', 600 - 70, 330 - 90,
                                        sasuke_logo.w * 0.1, sasuke_logo.h * 0.1)
    elif p1_choose == 3:
        itachi_back.clip_composite_draw(0, 0, itachi_back.w, itachi_back.h, 0, 'h', 600, 330,
                                        itachi_back.w * 3.5, itachi_back.h * 3.5)
        itachi.clip_composite_draw(int(itachi_frame)*32, 0, 32, 64, 0, 'h', p1_x, p1_y+15, 100, 200)
        itachi_logo.clip_composite_draw(0, 0, itachi_logo.w, itachi_logo.h, 0, 'h', 600-60, 330-90,
                                        itachi_logo.w * 0.1, itachi_logo.h * 0.1)
    p1_image.clip_composite_draw(0, 0, 64, 32, 0, '', 600, 520, 120, 60)
    # if p2_choose == 1:
    #     naruto.clip_composite_draw(int(naruto_frame)*32, 0, 32, 48, 0, '', p2_x, p2_y, 100, 150)
    # elif p2_choose == 2:
    #     sasuke.clip_composite_draw(int(sasuke_frame)*32, 0, 32, 64, 0, '', p2_x, p2_y, 100, 200)
    # elif p2_choose == 3:
    #     itachi.clip_composite_draw(int(itachi_frame) * 32, 0, 32, 64, 0, '', p2_x, p2_y+15, 100, 200)
    if space_up:
        press_space.clip_composite_draw(0, 0, press_space.w, press_space.h, 0, '', 600, 60 + space_frame,
                                        press_space.w * 0.15, press_space.h * 0.15)
    else:
        press_space.clip_composite_draw(0, 0, press_space.w, press_space.h, 0, '', 600, 70 - space_frame,
                                        press_space.w * 0.15, press_space.h * 0.15)
    if dup_on:
        duplicate.clip_composite_draw(0, 0, 5906, 4135, 0, '', 600, 300, 600, 300)
    update_canvas()

def update():
    global naruto_frame, sasuke_frame, itachi_frame, space_frame, space_up, dup_wait_time, dup_on
    naruto_frame = (naruto_frame + 6 * game_framework.frame_time) % 6
    sasuke_frame = (sasuke_frame + 6 * game_framework.frame_time) % 6
    itachi_frame = (itachi_frame + 4 * game_framework.frame_time) % 4
    space_frame = space_frame + 10 * game_framework.frame_time
    if space_frame >= 9:
        if space_up:
            space_up = False
        else:
            space_up = True
        space_frame = 0

    # if p1_choose == p2_choose:
    #     dup_wait_time = get_time()
    #     dup_on = True

    if get_time() - dup_wait_time > 1:
        dup_on = False


def p1_choose_result():
    global p1_choose
    return p1_choose

def p2_choose_result():
    global p2_choose
    return p2_choose