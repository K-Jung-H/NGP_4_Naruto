from pico2d import *
import game_framework
import play_mode
import single_character_choice_mode
import title_mode


def init():
    global dead1, dead2, dead3, you_lose, round_num, frame, backimage, press_space, space_frame, space_up, l_bgm
    dead1 = load_image('resource/naruto_hard_hit.png')
    dead2 = load_image('resource/sasuke_hard_hit.png')
    dead3 = load_image('resource/itachi_hard_hit.png')
    you_lose = load_image('resource/you_lose.png')
    round_num = load_image('resource/3.png')
    backimage = load_image('resource/darkback.png')
    press_space = load_image('resource/press_space2.png')
    frame = 0
    space_frame = 0
    space_up = True
    # play_mode.p_bgm.stop()
    l_bgm = load_music('sound/losesound.mp3')
    l_bgm.set_volume(18)
    l_bgm.repeat_play()
def finish():
    global dead1, dead2, dead3, you_lose, round_num, backimage, press_space
    del dead1, dead2, dead3, you_lose, round_num, backimage, press_space
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
        dead1.clip_composite_draw(3 * 48, 0, 48, 40, 0, '', 600, 300, 135*2, 112*2)
        pass
    elif single_character_choice_mode.p1_choose_result() == 2:
        dead2.clip_composite_draw(3 * 64, 0, 64, 40, 0, '', 600, 300, 200*2, 125*2)
        pass
    elif single_character_choice_mode.p1_choose_result() == 3:
        dead3.clip_composite_draw(3 * 64, 0, 64, 40, 0, '', 600-30, 300, 200*2, 125*2)
        pass
    # idle.clip_composite_draw(int(frame) * 33, 0, 33, 49, 0, '', 600, 300, 93*2, 138*2)
    you_lose.clip_composite_draw(0, 0, you_lose.w, you_lose.h, 0, '', 600, 500, you_lose.w*1.2, you_lose.h*1.2)
    # round_num.clip_composite_draw(0, 0, round_num.w, round_num.h, 0, '', 680, 500, round_num.w, round_num.h)
    if space_up:
        press_space.clip_composite_draw(0, 0, press_space.w, press_space.h, 0, '', 600, 60 + space_frame,
                                        press_space.w * 0.7, press_space.h * 0.7)
    else:
        press_space.clip_composite_draw(0, 0, press_space.w, press_space.h, 0, '', 600, 70 - space_frame,
                                        press_space.w * 0.7, press_space.h * 0.7)
    update_canvas()

def update():
    global frame, space_frame, space_up
    frame = (frame + 8 * 0.7 * game_framework.frame_time) % 8
    space_frame = space_frame + 10 * game_framework.frame_time
    if space_frame >= 9:
        if space_up:
            space_up = False
        else:
            space_up = True
        space_frame = 0