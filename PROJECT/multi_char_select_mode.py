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

# 각 구조체의 포맷 정의
position_format = "2f"  # Position 구조체
player_info_format = "32s2f?3i?"  # Player_Info 구조체
attack_info_format = "2f?2i"  # Attack_Info 구조체
etc_info_format = "5i"  # ETC_Info 구조체
game_data_format = f"{player_info_format * 2}{attack_info_format * 18}{etc_info_format}"  # Game_Data 전체 포맷

# 데이터 크기 계산
data_size = struct.calcsize(game_data_format)

def receive_game_data(client_socket):
    global p1_chakra, p2_chakra, p1_hp, p2_hp, game_time

    data = b""
    while len(data) < data_size:
        # print(data_size)
        packet = client_socket.recv(data_size - len(data))
        if not packet:
            print("연결이 종료되었습니다.")
            return None
        data += packet

    # # 클라이언트의 IPv4 주소 출력
    # client_ipv4 = network_client.get_ipv4_address()
    # if client_ipv4:
    #     print(f"클라이언트의 IPv4 주소: {client_ipv4}")
    # else:
    #     print("IPv4 주소를 가져오는 데 실패했습니다.")

    # data += client_socket.recv(data_size)
    # 데이터 언패킹
    unpacked_data = struct.unpack(game_data_format, data)
    # print("Unpacked data:", unpacked_data)  # 디버깅용

    # 플레이어 1 업데이트
    # p1.x = unpacked_data[1]
    # p1.y = unpacked_data[2]
    # p1.dir = unpacked_data[3]
    # p1_state = unpacked_data[4]
    # p1.cur_state = state_mapping.get(p1_state, Idle)  # 기본값은 Idle로 설정
    # p1.frame = unpacked_data[6]
    #
    # # extra_state_data에 여러개의 값이 있는 경우를 위한 for?
    # if p1_state in extra_state_data:
    #     for key, value in extra_state_data[p1_state].items():
    #         setattr(p1, key, value)
    #
    # print(unpacked_data[0], unpacked_data[8])
    print("p1 ready : ", unpacked_data[7], "p2 ready : ", unpacked_data[15])
    # if unpacked_data[8]:
    #     # 플레이어 2 업데이트
    #     p2.x = unpacked_data[9]
    #     p2.y = unpacked_data[10]
    #     p2.dir = unpacked_data[11]
    #     p2_state = unpacked_data[12]
    #     p2.cur_state = state_mapping.get(p2_state, Idle)
    #     p2.frame = unpacked_data[14]
    #
    #     if p2_state in extra_state_data:
    #         for key, value in extra_state_data[p2_state].items():
    #             setattr(p2, key, value)

    print("p1 select char : ", unpacked_data[5], "p2 select char : ", unpacked_data[13])

    p1_hp = unpacked_data[-5]
    p1_chakra = unpacked_data[-4]
    p2_hp = unpacked_data[-3]
    p2_chakra = unpacked_data[-2]
    game_time = unpacked_data[-1]

def receive_game_data_loop(client_socket):
    """서버로부터 데이터를 계속 수신하고 게임 객체를 업데이트."""
    count = 0  # 수신 횟수 카운트
    start_time = time.time()  # 시작 시간
    while True:
        # try:
        #     receive_game_data(client_socket)
        # except Exception as e:
        #     print(f"데이터 수신 중 오류 발생: {e}")
        #     break
        receive_game_data(client_socket)
        count += 1

        # 1초가 지났는지 확인
        elapsed_time = time.time() - start_time
        if elapsed_time >= 1.0:
            print(f"초당 수신 횟수: {count}")
            count = 0  # 카운트 초기화
            start_time = time.time()  # 시간 초기화

def init():
    global image1, naruto, sasuke, itachi
    global p1_x, p1_y, p2_x, p2_y, p1_choose, p2_choose, p1_image, p2_image, character_back
    global vs, press_space
    global naruto_frame, sasuke_frame, itachi_frame, space_frame, space_up
    global duplicate, dup_on, dup_wait_time, dir_image, mode_choose
    global naruto_back, sasuke_back, itachi_back, naruto_logo, sasuke_logo, itachi_logo
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
    global network_client
    network_client = game_framework.get_socket()
    if network_client:
        print("소켓 재사용")
        receiver_thread = threading.Thread(target=receive_game_data_loop, args=(network_client.client_socket,))
        receiver_thread.daemon = True  # 메인 프로그램 종료 시 함께 종료되도록 설정
        receiver_thread.start()
        pass
    else:
        print("전역소켓 설정안된듯")

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
            game_framework.change_mode(multi_mode)
            # if p1_choose != p2_choose:
            #     game_framework.change_mode(play_mode)
            # else:
            #     dup_on = True
            #     dup_wait_time = get_time()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            p2_choose = (p2_choose - 1) % character_count
            if p2_choose == 0:
                p2_choose = character_count
        elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
            p2_choose = (p2_choose + 1) % character_count
            if p2_choose == 0:
                p2_choose = character_count
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
    vs.clip_composite_draw(0, 0, 2500, 2500, 0, '', 600, 300, 200, 200)
    dir_image.clip_composite_draw(0, 0, dir_image.w, dir_image.h, 0, '', 300 + 160, 370, dir_image.w, dir_image.h)
    dir_image.clip_composite_draw(0, 0, dir_image.w, dir_image.h, 0, 'h', 300 - 160, 370, dir_image.w, dir_image.h)
    dir_image.clip_composite_draw(0, 0, dir_image.w, dir_image.h, 0, '', 900 + 160, 370, dir_image.w, dir_image.h)
    dir_image.clip_composite_draw(0, 0, dir_image.w, dir_image.h, 0, 'h', 900 - 160, 370, dir_image.w, dir_image.h)
    p1_image.clip_composite_draw(0, 0, 64, 32, 0, '', 900, 520, 120, 60)
    p2_image.clip_composite_draw(0, 0, 64, 32, 0, '', 300, 520, 120, 60)

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

    if get_time() - dup_wait_time > 1:
        dup_on = False


def p1_choose_result():
    global p1_choose
    return p1_choose

def p2_choose_result():
    global p2_choose
    return p2_choose