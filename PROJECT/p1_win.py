from pico2d import *
import game_framework
import play_mode
import single_character_choice_mode
import title_mode


def init():
    global win1, win2, win3, you_win, round_num, frame, backimage, press_space, space_frame, space_up, w_bgm
    win1 = load_image('resource/naruto_win.png')
    win2 = load_image('resource/sasuke_win.png')
    win3 = load_image('resource/itachi_win.png')
    you_win = load_image('resource/you_win.png')
    round_num = load_image('resource/3.png')
    backimage = load_image('resource/round3.png')
    press_space = load_image('resource/press_space.png')
    frame = 0
    space_frame = 0
    space_up = True
    w_bgm = load_music('sound/winsound.mp3')
    w_bgm.set_volume(18)
    w_bgm.repeat_play()
def finish():
    global win1, win2, win3, you_win, round_num, backimage, press_space
    del win1, win2, win3, you_win, round_num, backimage, press_space
def handle_events():
    events = get_events()
    global p1_choose, p2_choose, character_count, dup_on, dup_wait_time
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            play_mode.round_num = 1
            game_framework.change_mode(title_mode)
def running():
    pass
def draw():
    clear_canvas()
    backimage.clip_composite_draw(0, 0, backimage.w, backimage.h, 0, '', 600, 300, 1200, 600)
    if single_character_choice_mode.p1_choose_result() == 1:
        win1.clip_composite_draw(int(frame) * 50, 0, 50, 64, 0, '', 600, 300, 140*2, 180*2)
        pass
    elif single_character_choice_mode.p1_choose_result() == 2:
        win2.clip_composite_draw(int(frame) * 34, 0, 34, 64, 0, 'h', 600+20, 300, 103*2, 200*2)
        pass
    elif single_character_choice_mode.p1_choose_result() == 3:
        win3.clip_composite_draw(int(frame) * 42, 0, 42, 74, 0, '', 600, 300, 90*2, 159*2)
        pass
    # idle.clip_composite_draw(int(frame) * 33, 0, 33, 49, 0, '', 600, 300, 93*2, 138*2)
    you_win.clip_composite_draw(0, 0, you_win.w, you_win.h, 0, '', 600, 500, you_win.w*1.2, you_win.h*1.2)
    # round_num.clip_composite_draw(0, 0, round_num.w, round_num.h, 0, '', 680, 500, round_num.w, round_num.h)
    if space_up:
        press_space.clip_composite_draw(0, 0, press_space.w, press_space.h, 0, '', 600, 60 + space_frame,
                                        press_space.w * 0.15, press_space.h * 0.15)
    else:
        press_space.clip_composite_draw(0, 0, press_space.w, press_space.h, 0, '', 600, 70 - space_frame,
                                        press_space.w * 0.15, press_space.h * 0.15)
    update_canvas()

def update():
    global frame, space_frame, space_up
    if single_character_choice_mode.p1_choose_result() == 1:
        frame = (frame + 8 * 0.7 * game_framework.frame_time) % 8
        pass
    elif single_character_choice_mode.p1_choose_result() == 2:
        frame = (frame + 12 * 0.7 * game_framework.frame_time) % 12
        pass
    elif single_character_choice_mode.p1_choose_result() == 3:
        frame = (frame + 16 * 0.7 * game_framework.frame_time) % 16
        pass

    space_frame = space_frame + 10 * game_framework.frame_time
    if space_frame >= 9:
        if space_up:
            space_up = False
        else:
            space_up = True
        space_frame = 0