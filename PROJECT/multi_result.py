from pico2d import *
import game_framework
import multi_char_select_mode
import multi_mode
import play_mode
import single_character_choice_mode
import title_mode


def init():
    global dead1, dead2, dead3, you_lose, round_num, frame, lose_backimage, press_space, space_frame, space_up, l_bgm
    global win1, win2, win3, you_win, win_backimage, im_win
    dead1 = load_image('resource/naruto_hard_hit.png')
    dead2 = load_image('resource/sasuke_hard_hit.png')
    dead3 = load_image('resource/itachi_hard_hit.png')
    you_lose = load_image('resource/you_lose.png')
    round_num = load_image('resource/3.png')
    lose_backimage = load_image('resource/darkback.png')
    win1 = load_image('resource/naruto_win.png')
    win2 = load_image('resource/sasuke_win.png')
    win3 = load_image('resource/itachi_win.png')
    you_win = load_image('resource/you_win.png')
    press_space = load_image('resource/press_space2.png')
    win_backimage = load_image('resource/madahashimap.png')
    frame = 0
    space_frame = 0
    space_up = True
    im_win = False
    # play_mode.p_bgm.stop()
    if multi_mode.winner_num == game_framework.my_player_num:
        w_bgm = load_music('sound/winsound.mp3')
        w_bgm.set_volume(18)
        w_bgm.repeat_play()
        im_win = True
    else:
        l_bgm = load_music('sound/losesound.mp3')
        l_bgm.set_volume(18)
        l_bgm.repeat_play()
        im_win = False
    # if game_framework.get_socket():
    #     game_framework.network_client.disconnect()
    #     print("소켓 해제")
    #     game_framework.stop_receiver_thread()
    #     game_framework.stop_key_listener()
    #     game_framework.network_client = None
    #     print("타이틀 초기화 테스트 : ", game_framework.get_socket())
    #     pass
def finish():
    global dead1, dead2, dead3, you_lose, round_num, press_space
    del dead1, dead2, dead3, you_lose, round_num, press_space
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
    if multi_mode.winner_num == game_framework.my_player_num:
        win_backimage.clip_composite_draw(0, 0, win_backimage.w, win_backimage.h, 0, '', 600, 300, 1200, 600)
    else:
        lose_backimage.clip_composite_draw(0, 0, lose_backimage.w, lose_backimage.h, 0, '', 600, 300, 1200, 600)
    if im_win:
        if game_framework.my_char_num == 1:
            win1.clip_composite_draw(int(frame) * 50, 0, 50, 64, 0, '', 600, 300, 140 * 2, 180 * 2)
        elif game_framework.my_char_num == 2:
            win2.clip_composite_draw(int(frame) * 34, 0, 34, 64, 0, 'h', 600 + 20, 300, 103 * 2, 200 * 2)
        elif game_framework.my_char_num == 3:
                win3.clip_composite_draw(int(frame) * 42, 0, 42, 74, 0, '', 600, 300, 90 * 2, 159 * 2)
        you_win.clip_composite_draw(0, 0, you_win.w, you_win.h, 0, '', 600, 500, you_win.w * 1.2, you_win.h * 1.2)
    else:
        if game_framework.my_char_num == 1:
            dead1.clip_composite_draw(3 * 48, 0, 48, 40, 0, '', 600, 300, 135*2, 112*2)
        elif game_framework.my_char_num == 2:
            dead2.clip_composite_draw(3 * 64, 0, 64, 40, 0, '', 600, 300, 200 * 2, 125 * 2)
        elif game_framework.my_char_num == 3:
            dead3.clip_composite_draw(3 * 64, 0, 64, 40, 0, '', 600 - 30, 300, 200 * 2, 125 * 2)
        you_lose.clip_composite_draw(0, 0, you_lose.w, you_lose.h, 0, '', 600, 500, you_lose.w * 1.2, you_lose.h * 1.2)

    # idle.clip_composite_draw(int(frame) * 33, 0, 33, 49, 0, '', 600, 300, 93*2, 138*2)

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