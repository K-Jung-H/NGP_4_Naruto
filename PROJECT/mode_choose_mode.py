from pico2d import *

import charactor_choose_mode
import game_framework
import play_mode
import single_character_choice_mode
import multi_room_select_mode
import title_mode
import multi_mode
import server_connect

character_count = 3

connect_fail_flag = False

def init():
    global image1, naruto, sasuke, itachi
    global p1_x, p1_y, p2_x, p2_y, p1_choose, p2_choose, p1_image, p2_image, character_back
    global vs, press_space
    global naruto_frame, sasuke_frame, itachi_frame, space_frame, space_up
    global duplicate, dup_on, dup_wait_time, dir_image, single_image, multi_image, mode_choose, hand, mode_back,\
        multi_font, connect_fail, cf_frame
    image1 = load_image('resource/title_main.png')
    naruto = load_image('resource/naruto_idle.png')
    sasuke = load_image('resource/sasuke_idle.png')
    itachi = load_image('resource/itachi_idle.png')
    p1_image = load_image('resource/p1_image.png')
    p2_image = load_image('resource/p2_image.png')
    character_back = load_image('resource/charactor_back.png')
    vs = load_image('resource/vs.png')
    press_space = load_image('resource/press_space.png')
    duplicate = load_image('resource/duplicate.png')
    dir_image = load_image('resource/dir_image.png')
    single_image = load_image('resource/single_play_image.png')
    multi_image = load_image('resource/multi_play_image.png')
    hand = load_image('resource/hand_image.png')
    mode_back = load_image('resource/mode_choice_back.png')
    multi_font = load_image('resource/multi_font.png')
    connect_fail = load_image('resource/connect_fail.png')
    p1_x = 900
    p1_y = 360
    p2_x = 300
    p2_y = 360
    p1_choose = 2
    p2_choose = 3
    naruto_frame, sasuke_frame, itachi_frame = 0, 0, 0
    space_frame = 0
    space_up = True
    dup_on = False
    dup_wait_time = 0
    mode_choose = '1p'
    cf_frame = 0

def finish():
    global image1, naruto, sasuke, itachi, p1_image, p2_image, character_back, vs, press_space
    global duplicate, dir_image, single_image, multi_image, hand, multi_font, connect_fail
    del image1, naruto, sasuke, itachi, p1_image, p2_image, character_back, vs, press_space, duplicate, dir_image
    del single_image, multi_image, hand, multi_font, connect_fail
def handle_events():
    events = get_events()
    global p1_choose, p2_choose, character_count, dup_on, dup_wait_time, mode_choose
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            if mode_choose == '1p':
                game_framework.change_mode(single_character_choice_mode)
            elif mode_choose == '2p':
                game_framework.change_mode(charactor_choose_mode)
            elif mode_choose == 'multi':
                game_framework.change_mode(server_connect)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            if mode_choose == '2p':
                mode_choose = '1p'
            elif mode_choose == 'multi':
                mode_choose = '2p'
        elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
            if mode_choose == '1p':
                mode_choose = '2p'
            elif mode_choose == '2p':
                mode_choose = 'multi'
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            if mode_choose == '2p':
                mode_choose = '1p'
            elif mode_choose == 'multi':
                mode_choose = '2p'
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            if mode_choose == '1p':
                mode_choose = '2p'
            elif mode_choose == '2p':
                mode_choose = 'multi'
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F1:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_z:
            mode_choose = 'multi'

def running():
    pass
def draw():
    clear_canvas()
    image1.clip_composite_draw(0, 0, 900, 507, 0, '', 600, 300, 1200, 600)
    mode_back.clip_composite_draw(0, 0, mode_back.w, mode_back.h, 0, '', 600, 300, mode_back.w*3.8, mode_back.h*3.8)
    # vs.clip_composite_draw(0, 0, 2500, 2500, 0, '', 600, 300, 200, 200)
    single_image.clip_composite_draw(int(naruto_frame)*single_image.w//3, 0, single_image.w//3, single_image.h,
                                     0, '', 350, 300,
                                     single_image.w//3*2, single_image.h*2)
    multi_image.clip_composite_draw(int(naruto_frame)*multi_image.w//3, 0, multi_image.w//3, multi_image.h,
                                    0, '', 600, 300,
                                     multi_image.w//3*2, multi_image.h*2)
    multi_image.clip_composite_draw(int(naruto_frame) * multi_image.w // 3, 0, multi_image.w // 3, multi_image.h,
                                    0, '', 850, 300,
                                    multi_image.w // 3 * 2, multi_image.h * 2)
    multi_font.clip_composite_draw(0, 0, multi_font.w, multi_font.h, 0, '', 840, 340, multi_font.w, multi_font.h)

    if mode_choose == '1p':
        hand.clip_composite_draw(0, 0, hand.w, hand.h, 0, '', 370, 430+naruto_frame*3,
                                        hand.w*2.5, hand.h*2.5)
    elif mode_choose == '2p':
        hand.clip_composite_draw(0, 0, hand.w, hand.h, 0, '', 620, 430+naruto_frame*3,
                                 hand.w*2.5, hand.h*2.5)
    elif mode_choose == 'multi':
        hand.clip_composite_draw(0, 0, hand.w, hand.h, 0, '', 870, 430+naruto_frame*3,
                                 hand.w*2.5, hand.h*2.5)

    if space_up:
        press_space.clip_composite_draw(0, 0, press_space.w, press_space.h, 0, '', 600, 60 + space_frame,
                                        press_space.w * 0.15, press_space.h * 0.15)
    else:
        press_space.clip_composite_draw(0, 0, press_space.w, press_space.h, 0, '', 600, 70 - space_frame,
                                        press_space.w * 0.15, press_space.h * 0.15)

    if connect_fail_flag:
        connect_fail.clip_composite_draw(0, 0, connect_fail.w, connect_fail.h, 0, '', 600, 300, connect_fail.w * 1,
                                      connect_fail.h * 1)
    update_canvas()

def update():
    global naruto_frame, sasuke_frame, itachi_frame, space_frame, space_up, dup_wait_time, dup_on, cf_frame, \
        connect_fail_flag
    naruto_frame = (naruto_frame + 3 * game_framework.frame_time) % 3
    space_frame = space_frame + 10 * game_framework.frame_time
    if space_frame >= 9:
        if space_up:
            space_up = False
        else:
            space_up = True
        space_frame = 0
    if connect_fail_flag:
        cf_frame += 1 * game_framework.frame_time
        if cf_frame > 5:
            connect_fail_flag = False
            cf_frame = 0




def mode_choose_result():
    global mode_choose
    return mode_choose
