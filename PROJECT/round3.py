from pico2d import *
import game_framework
import play_mode

def init():
    global idle, round, round_num, frame, backimage, press_space, space_frame, space_up, r3_bgm
    idle = load_image('resource/sakura_idle.png')
    round = load_image('resource/round.png')
    round_num = load_image('resource/3.png')
    backimage = load_image('resource/round3.png')
    press_space = load_image('resource/press_space.png')
    frame = 0
    space_frame = 0
    space_up = True
    r3_bgm = load_music('sound/round3.mp3')
    r3_bgm.set_volume(8)
    r3_bgm.repeat_play()
def finish():
    global idle, round, round_num, backimage, press_space
    del idle, round, round_num, backimage, press_space
def handle_events():
    events = get_events()
    global p1_choose, p2_choose, character_count, dup_on, dup_wait_time
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            play_mode.round_num = 3
            game_framework.change_mode(play_mode)
def running():
    pass
def draw():
    clear_canvas()
    backimage.clip_composite_draw(0, 0, backimage.w, backimage.h, 0, '', 600, 300, 1200, 600)
    idle.clip_composite_draw(int(frame) * 34, 0, 34, 49, 0, '', 600, 300, 96*2, 138*2)
    round.clip_composite_draw(0, 0, round.w, round.h, 0, '', 560, 500, round.w, round.h)
    round_num.clip_composite_draw(0, 0, round_num.w, round_num.h, 0, '', 680, 500, round_num.w, round_num.h)
    if space_up:
        press_space.clip_composite_draw(0, 0, press_space.w, press_space.h, 0, '', 600, 60 + space_frame,
                                        press_space.w * 0.15, press_space.h * 0.15)
    else:
        press_space.clip_composite_draw(0, 0, press_space.w, press_space.h, 0, '', 600, 70 - space_frame,
                                        press_space.w * 0.15, press_space.h * 0.15)
    update_canvas()

def update():
    global frame, space_frame, space_up
    frame = (frame + 6 * 0.7 * game_framework.frame_time) % 6
    space_frame = space_frame + 10 * game_framework.frame_time
    if space_frame >= 9:
        if space_up:
            space_up = False
        else:
            space_up = True
        space_frame = 0