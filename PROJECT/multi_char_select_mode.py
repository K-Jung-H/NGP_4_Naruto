import struct
import threading
import time

from pico2d import *
import game_framework
import play_mode
import mode_choose_mode
import title_mode
import multi_mode
from network_client import NetworkClient

character_count = 3

p1_ready = False
p2_ready = False

def handle_char_select_data(data):
    global p1_choose, p2_choose, p1_ready, p2_ready, p1_name, p2_name
    # 플레이어 1과 2의 상태 확인
    p1_ready = data[7]
    p2_ready = data[15]
    p1_choose = data[5]
    p2_choose = data[13]

    p1_name = data[0]
    p2_name = data[8]
    # print(p1_name, p2_name)

    # 캐릭터 선택 상태 출력
    # print(f"Player 1 Ready: {p1_ready}, Selected Character: {p1_selected_char}")
    # print(f"Player 2 Ready: {p2_ready}, Selected Character: {p2_selected_char}")

    # 필요에 따라 추가 로직 작성
    if p1_ready and p2_ready:
        print("Both players are ready! Starting the game...")

def init():
    global image1, naruto, sasuke, itachi
    global p1_x, p1_y, p2_x, p2_y, p1_choose, p2_choose, p1_image, p2_image, character_back
    global vs, press_space
    global naruto_frame, sasuke_frame, itachi_frame, space_frame, space_up
    global duplicate, dup_on, dup_wait_time, dir_image, mode_choose
    global naruto_back, sasuke_back, itachi_back, naruto_logo, sasuke_logo, itachi_logo, ready_logo
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
    naruto_back = load_image('resource/naruto_back.png')
    sasuke_back = load_image('resource/sasuke_back.png')
    itachi_back = load_image('resource/itachi_back.png')
    naruto_logo = load_image('resource/naruto_logo1.png')
    sasuke_logo = load_image('resource/sasuke_logo.png')
    itachi_logo = load_image('resource/itachi_logo.png')
    ready_logo = load_image('resource/ready.png')
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
    mode_choose = mode_choose_mode.mode_choose_result()
    # global network_client
    # network_client = game_framework.get_socket()
    # if network_client:
    #     print("소켓 재사용")
    game_framework.set_data_handler(handle_char_select_data)
    # init_data = game_framework.receive_game_data(game_framework.network_client.client_socket)


    game_framework.reset_stop_event()
    game_framework.start_receiver_thread()
    # receiver_thread = threading.Thread(target=receive_game_data_loop, args=(network_client.client_socket,))
    # receiver_thread.daemon = True  # 메인 프로그램 종료 시 함께 종료되도록 설정
    # receiver_thread.start()
    game_framework.start_key_listener()
    # 이름 업데이트를 위한 센드
    game_framework.send_key_info('z', 1, game_framework.my_player_name)
    pass
    # else:
    #     print("전역소켓 설정안된듯")

def finish():
    global image1, naruto, sasuke, itachi, p1_image, p2_image, character_back, vs, press_space, duplicate, dir_image
    del image1, naruto, sasuke, itachi, p1_image, p2_image, character_back, vs, press_space, duplicate, dir_image


def handle_events():
    events = get_events()
    global p1_choose, p2_choose, character_count, dup_on, dup_wait_time
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            # 이게 원래 써야되는 코드
            # print(game_framework.my_player_name, clean_name(p1_name))
            # if clean_name(p1_name) == game_framework.my_player_name:
            #     game_framework.my_player_num = 1
            #     game_framework.enemy_player_name = clean_name(p2_name)
            #     print(game_framework.my_player_name, p1_name)
            # elif clean_name(p2_name) == game_framework.my_player_name:
            #     game_framework.my_player_num = 2
            #     game_framework.enemy_player_name = clean_name(p1_name)
            # 테스트용
            game_framework.my_player_num = 1
            game_framework.enemy_player_name = clean_name(p2_name)
            print(game_framework.my_player_name, game_framework.enemy_player_name)
            game_framework.change_mode(multi_mode)
            # if p1_choose != p2_choose:
            #     game_framework.change_mode(play_mode)
            # else:
            #     dup_on = True
            #     dup_wait_time = get_time()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F1:
            game_framework.change_mode(title_mode)

def running():
    pass
def draw():
    clear_canvas()
    image1.clip_composite_draw(0, 0, 900, 507, 0, '', 600, 300, 1200, 600)
    vs.clip_composite_draw(0, 0, 2500, 2500, 0, '', 600, 300, 200, 200)
    dir_image.clip_composite_draw(0, 0, dir_image.w, dir_image.h, 0, '', 300 + 160, 370, dir_image.w, dir_image.h)
    dir_image.clip_composite_draw(0, 0, dir_image.w, dir_image.h, 0, 'h', 300 - 160, 370, dir_image.w, dir_image.h)
    dir_image.clip_composite_draw(0, 0, dir_image.w, dir_image.h, 0, '', 900 + 160, 370, dir_image.w, dir_image.h)
    dir_image.clip_composite_draw(0, 0, dir_image.w, dir_image.h, 0, 'h', 900 - 160, 370, dir_image.w, dir_image.h)
    # p1_image.clip_composite_draw(0, 0, 64, 32, 0, '', 900, 520, 120, 60)
    # p2_image.clip_composite_draw(0, 0, 64, 32, 0, '', 300, 520, 120, 60)

    if p1_choose == 1:
        naruto_back.clip_composite_draw(0, 0, naruto_back.w, naruto_back.h, 0, 'h', 900, 330,
                                        naruto_back.w * 3.5, naruto_back.h * 3.5)
        naruto.clip_composite_draw(int(naruto_frame)*32, 0, 32, 48, 0, 'h', p1_x, p1_y, 100, 150)
        naruto_logo.clip_composite_draw(0, 0, naruto_logo.w, naruto_logo.h, 0, 'h', 900 + 70, 330 - 90,
                                        naruto_logo.w * 0.1, naruto_logo.h * 0.1)
    elif p1_choose == 2:
        sasuke_back.clip_composite_draw(0, 0, sasuke_back.w, sasuke_back.h, 0, 'h', 900, 330,
                                        sasuke_back.w * 3.5, sasuke_back.h * 3.5)
        sasuke.clip_composite_draw(int(sasuke_frame)*32, 0, 32, 64, 0, 'h', p1_x+10, p1_y, 100, 200)
        sasuke_logo.clip_composite_draw(0, 0, sasuke_logo.w, sasuke_logo.h, 0, 'h', 900 + 70, 330 - 90,
                                        sasuke_logo.w * 0.1, sasuke_logo.h * 0.1)
    elif p1_choose == 3:
        itachi_back.clip_composite_draw(0, 0, itachi_back.w, itachi_back.h, 0, 'h', 900, 330,
                                        itachi_back.w * 3.5, itachi_back.h * 3.5)
        itachi.clip_composite_draw(int(itachi_frame)*32, 0, 32, 64, 0, 'h', p1_x, p1_y+15, 100, 200)
        itachi_logo.clip_composite_draw(0, 0, itachi_logo.w, itachi_logo.h, 0, 'h', 900 + 60, 330 - 90,
                                        itachi_logo.w * 0.1, itachi_logo.h * 0.1)

    if p2_choose == 1:
        naruto_back.clip_composite_draw(0, 0, naruto_back.w, naruto_back.h, 0, '', 300, 330,
                                        naruto_back.w * 3.5, naruto_back.h * 3.5)
        naruto.clip_composite_draw(int(naruto_frame)*32, 0, 32, 48, 0, '', p2_x, p2_y, 100, 150)
        naruto_logo.clip_composite_draw(0, 0, naruto_logo.w, naruto_logo.h, 0, '', 300 - 70, 330 - 90,
                                        naruto_logo.w * 0.1, naruto_logo.h * 0.1)
    elif p2_choose == 2:
        sasuke_back.clip_composite_draw(0, 0, sasuke_back.w, sasuke_back.h, 0, '', 300, 330,
                                        sasuke_back.w * 3.5, sasuke_back.h * 3.5)
        sasuke.clip_composite_draw(int(sasuke_frame)*32, 0, 32, 64, 0, '', p2_x-10, p2_y, 100, 200)
        sasuke_logo.clip_composite_draw(0, 0, sasuke_logo.w, sasuke_logo.h, 0, '', 300 - 70, 330 - 90,
                                        sasuke_logo.w * 0.1, sasuke_logo.h * 0.1)
    elif p2_choose == 3:
        itachi_back.clip_composite_draw(0, 0, itachi_back.w, itachi_back.h, 0, '', 300, 330,
                                        itachi_back.w * 3.5, itachi_back.h * 3.5)
        itachi.clip_composite_draw(int(itachi_frame) * 32, 0, 32, 64, 0, '', p2_x, p2_y+15, 100, 200)
        itachi_logo.clip_composite_draw(0, 0, itachi_logo.w, itachi_logo.h, 0, '', 300 - 60, 330 - 90,
                                        itachi_logo.w * 0.1, itachi_logo.h * 0.1)

    if p1_ready:
        ready_logo.clip_composite_draw(0, 0, ready_logo.w, ready_logo.h, 0, '', 900, 120, ready_logo.w*0.3, ready_logo.h*0.3)
    if p2_ready:
        ready_logo.clip_composite_draw(0, 0, ready_logo.w, ready_logo.h, 0, '', 300, 120, ready_logo.w*0.3, ready_logo.h*0.3)

    if space_up:
        press_space.clip_composite_draw(0, 0, press_space.w, press_space.h, 0, '', 600, 60 + space_frame,
                                        press_space.w * 0.15, press_space.h * 0.15)
    else:
        press_space.clip_composite_draw(0, 0, press_space.w, press_space.h, 0, '', 600, 70 - space_frame,
                                        press_space.w * 0.15, press_space.h * 0.15)

    draw_text(clean_name(p1_name), 800, 520, 50)
    draw_text(clean_name(p2_name), 150, 520, 50)

    if dup_on:
        duplicate.clip_composite_draw(0, 0, 5906, 4135, 0, '', 600, 300, 600, 300)
    update_canvas()

def draw_text(text, x, y, size):
    # font = load_font("C:/Windows/Fonts/Arial.ttf", size)
    font = load_font("resource/Arial.ttf", size)
    font.draw(x, y, text, (0, 0, 0))  # 흰색 텍스트

def clean_name(name_bytes):
    """바이트 문자열에서 깨끗한 문자열 추출"""
    return name_bytes.decode('utf-8', errors='ignore').rstrip('\x00').strip()

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

    if get_time() - dup_wait_time > 1:
        dup_on = False


def p1_choose_result():
    global p1_choose
    return p1_choose

def p2_choose_result():
    global p2_choose
    return p2_choose