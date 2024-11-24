from pico2d import *

import charactor_choose_mode
import game_framework
import play_mode
import single_character_choice_mode
import mode_choose_mode

def init():
    global image1, image2, naruto, sasuke, title_frame, sasuke_x, naruto_x
    global mode_num, logo_frame, press_space, space_on, space_frame, space_up, bgm
    image1 = load_image('resource/title_main.png')
    image2 = load_image('resource/naruto_logo.png')
    naruto = load_image('resource/title_naruto.png')
    sasuke = load_image('resource/title_sasuke.png')
    press_space = load_image('resource/press_space.png')
    bgm = load_music('sound/mainsound.mp3')
    bgm.set_volume(12)
    bgm.repeat_play()

    title_frame = 0
    naruto_x, sasuke_x = 1250, 0
    mode_num = 1
    logo_frame = 0
    space_on = False
    space_frame = 0
    space_up = True
def finish():
    global image1, image2, naruto, sasuke, press_space
    del image1, image2, naruto, sasuke, press_space
def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            # game_framework.change_mode(charactor_choose_mode)
            # game_framework.change_mode(single_character_choice_mode)
            game_framework.change_mode(mode_choose_mode)

def running():
    pass
def draw():
    clear_canvas()
    image1.clip_composite_draw(0, 0, 900, 507, 0, '', 600, 300, 1200, 600)
    sasuke.clip_composite_draw(0, 0, 256, 191, 0, '', sasuke_x + title_frame, 300, 500, 380)
    naruto.clip_composite_draw(0, 0, 216, 192, 0, '', naruto_x - title_frame, 300, 430, 380)
    # image2.draw(600, 300)
    image2.clip_composite_draw(0, 0, 300, 144, 0, '', 600, 800 - logo_frame, 500, 230)
    if space_on:
        if space_up:
            press_space.clip_composite_draw(0, 0, press_space.w, press_space.h, 0, '', 600, 60 + space_frame,
                                            press_space.w*0.15, press_space.h*0.15)
        else:
            press_space.clip_composite_draw(0, 0, press_space.w, press_space.h, 0, '', 600, 70 - space_frame,
                                            press_space.w*0.15, press_space.h*0.15)
    update_canvas()

def update():
    global title_frame, mode_num, logo_frame, space_on, space_frame, space_up
    if mode_num == 1:
        title_frame = title_frame + 1000 * game_framework.frame_time
        if title_frame >= 800:
            mode_num = 2
    elif mode_num == 2:
        logo_frame = logo_frame + 600 * game_framework.frame_time
        if logo_frame >= 500:
            mode_num = 3
            space_on = True
    elif mode_num == 3:
        space_frame = space_frame + 10 * game_framework.frame_time
        if space_frame >= 9:
            if space_up:
                space_up = False
            else:
                space_up = True
            space_frame = 0


