import socket

from pico2d import *

import charactor_choose_mode
import game_framework
import game_world
import mode_choose_mode
import keyboard

import multi_result
import title_mode

from network_client import NetworkClient
import threading
import struct
from map import Map
from multi_player_render import (SASUKE_MULTI, NARUTO_MULTI, ITACHI_MULTI, Idle, Run, Jump, Attack,
                                 Skill_motion, Easy_hit, Hard_hit, Win, Lose, Run_Attack, Jump_Attack, Teleport)
from multi_skill_render import SkillObject
import time  # 시간 측정을 위해 추가
from server_connect import server_ip
import multi_char_select_mode

TEST = True
LOCAL = False

# 서버 설정
# if TEST:
#     if LOCAL:
#         SERVER_IP = '127.0.0.1'
#     else:
#         # SERVER_IP = '127.0.0.1'
#         # SERVER_IP = '192.168.81.90'
#         SERVER_IP = server_ip
# else:
#     SERVER_IP = "0"

SERVER_PORT = 9000

# 각 구조체의 포맷 정의
position_format = "2f"  # Position 구조체
player_info_format = "32s2f?3i?"  # Player_Info 구조체
attack_info_format = "2f?2i"  # Attack_Info 구조체
etc_info_format = "5i"  # ETC_Info 구조체
game_data_format = f"{player_info_format * 2}{attack_info_format * 18}{etc_info_format}"  # Game_Data 전체 포맷

# 데이터 크기 계산
data_size = struct.calcsize(game_data_format)


CHARACTER_NARUTO = 1
CHARACTER_SASUKE = 2
CHARACTER_ITACHI = 3

STATE_IDLE = 0
STATE_RUN = 1
STATE_JUMP = 2
STATE_ATTACK_NORMAL_1 = 3
STATE_ATTACK_NORMAL_2 = 4
STATE_ATTACK_NORMAL_3 = 5
STATE_ATTACK_NORMAL_4 = 6
STATE_ATTACK_SKILL_1 = 7
STATE_ATTACK_SKILL_2 = 8
STATE_ATTACK_SKILL_3 = 9
STATE_HIT_EASY = 10
STATE_HIT_HARD = 11
STATE_WIN = 12
STATE_LOSE = 13
STATE_ATTACK_RUN = 14
STATE_ATTACK_JUMP = 15
STATE_TELEPORT = 16

state_mapping = {
    STATE_IDLE: Idle,
    STATE_RUN: Run,
    STATE_JUMP: Jump,
    STATE_ATTACK_NORMAL_1: Attack,
    STATE_ATTACK_NORMAL_2: Attack,
    STATE_ATTACK_NORMAL_3: Attack,
    STATE_ATTACK_NORMAL_4: Attack,
    STATE_ATTACK_SKILL_1: Skill_motion,
    STATE_ATTACK_SKILL_2: Skill_motion,
    STATE_ATTACK_SKILL_3: Skill_motion,
    STATE_HIT_EASY: Easy_hit,
    STATE_HIT_HARD: Hard_hit,
    STATE_WIN: Win,
    STATE_LOSE: Lose,
    STATE_ATTACK_RUN: Run_Attack,
    STATE_ATTACK_JUMP: Jump_Attack,
    STATE_TELEPORT: Teleport
}

# 상태에 따른 추가 데이터 처리
extra_state_data = {
    STATE_ATTACK_NORMAL_1: {"attack_num": 1},
    STATE_ATTACK_NORMAL_2: {"attack_num": 2},
    STATE_ATTACK_NORMAL_3: {"attack_num": 3},
    STATE_ATTACK_NORMAL_4: {"attack_num": 4},
    STATE_ATTACK_SKILL_1: {"skill_num": 'shuriken'},
    STATE_ATTACK_SKILL_2: {"skill_num": 'skill2'},
    STATE_ATTACK_SKILL_3: {"skill_num": 'skill1'},
}

p1_name = ''
p2_name = ''

go_result = False
winner_num = 0

def handle_multi_play_data(unpacked_data):
    """멀티플레이 모드에서 언패킹된 데이터 처리."""
    global p1_chakra, p2_chakra, p1_hp, p2_hp, game_time, winner_num, go_result

    if not unpacked_data[7] or not unpacked_data[15]:
        game_framework.change_mode(multi_char_select_mode)

    # 플레이어 1 업데이트
    p1.x = unpacked_data[1]
    p1.y = unpacked_data[2]
    p1.dir = unpacked_data[3]
    p1_state = unpacked_data[4]

    # p1.cur_state = state_mapping.get(p1_state, Idle)  # 기본값은 Idle로 설정
    p1.frame = unpacked_data[6]

    # 추가 상태 데이터가 있을 경우 처리
    if p1_state in extra_state_data:
        for key, value in extra_state_data[p1_state].items():
            setattr(p1, key, value)

    p1.change_state(state_mapping.get(p1_state, Idle), None)

    # 플레이어 2가 활성화된 경우 업데이트
    if unpacked_data[8]:  # p2가 활성화된 경우
        p2.x = unpacked_data[9]
        p2.y = unpacked_data[10]
        p2.dir = unpacked_data[11]
        p2_state = unpacked_data[12]
        # p2.cur_state = state_mapping.get(p2_state, Idle)
        p2.frame = unpacked_data[14]

        if p2_state in extra_state_data:
            for key, value in extra_state_data[p2_state].items():
                setattr(p2, key, value)

        p2.change_state(state_mapping.get(p2_state, Idle), None)

    # 공격 데이터를 처리
    attacks = [
        unpacked_data[i:i + 5] for i in range(16, 16 + 18 * 5, 5)
    ]

    for i, attack in enumerate(attacks):
        if len(attack) >= 5:  # 공격 데이터 유효성 검사
            if int(attack[3]) > 0:  # 유효한 스킬 데이터만 활성화
                skills[i].activate(
                    skill_type=int(attack[3]),
                    x=attack[0],
                    y=attack[1],
                    dir=attack[2],
                    sprite_index=attack[4]
                )
            else:
                skills[i].deactivate()
        else:
            print(f"Invalid attack data at index {i}: {attack}")

    # 게임 상태 정보 업데이트
    p1_hp = unpacked_data[-5]
    p1_chakra = unpacked_data[-4]
    p2_hp = unpacked_data[-3]
    p2_chakra = unpacked_data[-2]
    game_time = unpacked_data[-1]

    if not go_result:
        print(p1_hp, p2_hp)
        if p1_hp <= 0:
            winner_num = 2
            go_result = True
            print(winner_num)
        elif p2_hp <= 0:
            winner_num = 1
            go_result = True
            print(winner_num)

    # # 디버깅 정보 출력
    # print(f"Player 1: HP={p1_hp}, Chakra={p1_chakra}")
    # print(f"Player 2: HP={p2_hp}, Chakra={p2_chakra}")
    # print(f"Game Time: {game_time}")
    # print(f"Game Time: {game_time}")

def init():
    global network_client
    global p1
    global p2
    global map
    global game_data
    global skills
    global health_bar, health_hp, naruto_mug, sasuke_mug, itachi_mug, chakra_image, chakra_frame
    global ko, fight, fight_frame, p1_chakra, p2_chakra, p1_hp, p2_hp, p1_mug, p2_mug, receiver_thread, p_bgm
    global p1_name, p2_name, result_timer, fo_result, winner_num

    health_bar = load_image('resource/health_bar.png')
    health_hp = load_image('resource/health_hp.png')
    naruto_mug = load_image('resource/naruto_mugshot.png')
    sasuke_mug = load_image('resource/sasuke_mugshot.png')
    itachi_mug = load_image('resource/itachi_mugshot.png')
    chakra_image = load_image('resource/chakra.png')
    chakra_frame = 0
    ko = load_image('resource/ko.png')
    fight = load_image('resource/fight.png')
    fight_frame = 0
    p1_chakra, p2_chakra = 0, 0
    p1_hp, p2_hp = 0, 0
    result_timer = 0
    fo_result = False
    winner_num = 0

    map = Map()
    game_world.add_object(map, 1)

    p_bgm = load_music('sound/playsound.mp3')
    p_bgm.set_volume(8)
    p_bgm.repeat_play()

    # if TEST:
    global network_client
    network_client = game_framework.get_socket()
    if network_client:
        print("소켓 재사용")
        pass
    else:
        # 네트워크 클라이언트 초기화 및 연결
        # network_client = NetworkClient(SERVER_IP, SERVER_PORT)
        # network_client.connect()
        pass

    # 송수신 버퍼 크기 설정
    # new_buf_size = 512
    # network_client.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, new_buf_size)
    # network_client.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, new_buf_size)
    #
    # recv_buf_size = network_client.client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    # send_buf_size = network_client.client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    #
    # print(f"수신 버퍼 크기: {recv_buf_size} bytes")
    # print(f"송신 버퍼 크기: {send_buf_size} bytes")

    # game_framework.set_socket(network_client)

    data = b""
    while len(data) < game_framework.data_size:
        # print(data_size)
        packet = game_framework.network_client.client_socket.recv(game_framework.data_size - len(data))
        if not packet:
            print("연결이 종료되었습니다.")
            return None
        data += packet
    unpacked_data = struct.unpack(game_data_format, data)

    if multi_char_select_mode.p1_choose_result() == 1:
        p1 = NARUTO_MULTI(1)
    elif multi_char_select_mode.p1_choose_result() == 2:
        p1 = SASUKE_MULTI(1)
    elif multi_char_select_mode.p1_choose_result() == 3:
        p1 = ITACHI_MULTI(1)
    game_world.add_object(p1, 1)

    if multi_char_select_mode.p2_choose_result() == 1:
        p2 = NARUTO_MULTI(1)
    elif multi_char_select_mode.p2_choose_result() == 2:
        p2 = SASUKE_MULTI(1)
    elif multi_char_select_mode.p2_choose_result() == 3:
        p2 = ITACHI_MULTI(1)
    game_world.add_object(p2, 1)

    # if unpacked_data[5] == 1:
    #     p1 = NARUTO_MULTI(1)
    # elif unpacked_data[5] == 2:
    #     p1 = SASUKE_MULTI(1)
    # elif unpacked_data[5] == 3:
    #     p1 = ITACHI_MULTI(1)
    # game_world.add_object(p1, 1)
    #
    # if unpacked_data[12]:
    #     if unpacked_data[12] == 1:
    #         p2 = NARUTO_MULTI(2)
    #     elif unpacked_data[12] == 2:
    #         p2 = SASUKE_MULTI(2)
    #     elif unpacked_data[12] == 3:
    #         p2 = ITACHI_MULTI(2)
    #     game_world.add_object(p2, 1)
    # else:
    #     p2 = ITACHI_MULTI(2)
    #     game_world.add_object(p2, 1)

    p1_mug = p1.char_name
    p2_mug = p2.char_name

    SkillObject.load_sprites()  # 스프라이트 이미지를 한 번만 로드
    skills = [SkillObject() for _ in range(18)]  # 18개의 Skill 객체 생성
    for skill in skills:
        game_world.add_object(skill, 2)
        skill.set_background(map)

    game_framework.set_data_handler(handle_multi_play_data)
    # receiver_thread = threading.Thread(target=receive_game_data_loop, args=(network_client.client_socket,))
    # receiver_thread.daemon = True  # 메인 프로그램 종료 시 함께 종료되도록 설정
    # receiver_thread.start()
    # receiver_thread = threading.Thread(target=Decoding, args=(network_client.client_socket,))
    # receiver_thread.start()

    p1.x = 1200
    p1.dir = -1
    p2.x = 400
    p1.y, p2.y = 400, 400
    p1.frame, p2.frame = 2, 2

    p1_hp, p2_hp = 400, 400

    p1.set_background(map)
    p2.set_background(map)
    # 맵 크기 확인
    print(map.w, map.h)
    # else:
    #     # p1 = NARUTO_MULTI(1)
    #     # p1 = SASUKE_MULTI(1)
    #     p1 = ITACHI_MULTI(1)
    #     game_world.add_object(p1, 1)
    #     # p2 = NARUTO_MULTI(2)
    #     p2 = SASUKE_MULTI(2)
    #     game_world.add_object(p2, 1)
    #
    #     p1.x = 1200
    #     p1.dir = -1
    #     p2.x = 400
    #     p1.y, p2.y = 400, 400
    #     p1.frame, p2.frame = 2, 2
    #
    #     p1.set_background(map)
    #     p2.set_background(map)

    # game_framework.start_key_listener()
    if game_framework.my_player_num == 1:
        p1_name = game_framework.my_player_name
        p2_name = game_framework.enemy_player_name
    elif game_framework.my_player_num == 2:
        p2_name = game_framework.my_player_name
        p1_name = game_framework.enemy_player_name


    pass
def finish():
    global network_client, receiver_thread
    network_client = game_framework.get_socket()
    if network_client:
        # network_client.disconnect()
        pass
    if TEST:
        # network_client.disconnect()
        pass
    # receiver_thread.join()
    game_world.remove_object(p1)
    game_world.remove_object(p2)
    game_world.remove_object(map)
    game_world.objects[2] = []

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            # game_framework.change_mode(mode_choose_mode)
            pass
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_F1):
            game_framework.change_mode(title_mode)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_F2):
            game_framework.change_mode(mode_choose_mode)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_d):
            # p2.x = 500
            pass
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            # p2.x = 100
            pass
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_t):
            # p1.hit_state = 'hard'
            # p1.dir = 1
            # p1.frame = 0
            # p1.skill_num = 'skill1'
            # (event.type, event.key) = (SDL_KEYDOWN, SDLK_LEFT)
            # # p1의 상태를 변경하기 위해 handle_event에 e 전달
            # p1.handle_event(event)
            # p1.cur_state = Run
            p1.cur_state = Jump
            pass

def running():
    pass
def draw():
    global skills, p1_name, p2_name
    clear_canvas()
    # 게임 월드에 추가까지 해서 그렸어야 했나? 그냥 여기서 그리는거랑 차이가 있나?
    game_world.render()
    health_bar.clip_composite_draw(0, 0, 402, 22, 0, '', 300, 570, 402, 30)
    health_bar.clip_composite_draw(0, 0, 402, 22, 0, '', 900, 570, 402, 30)
    health_hp.clip_composite_draw(0, 0, 8, 9, 0, '', 300 - (400 - p2_hp) // 2, 570, p2_hp, 28)
    health_hp.clip_composite_draw(0, 0, 8, 9, 0, '', 900 - (400 - p1_hp) // 2, 570, p1_hp, 28)
    if p2_chakra >= 30:
        chakra_image.clip_composite_draw(int(chakra_frame) * 32, 0, 32, 56, 0, '', 120, 520, 32, 56)
    if p2_chakra >= 60:
        chakra_image.clip_composite_draw(int(chakra_frame) * 32, 0, 32, 56, 0, '', 160, 520, 32, 56)
    if p2_chakra >= 90:
        chakra_image.clip_composite_draw(int(chakra_frame) * 32, 0, 32, 56, 0, '', 200, 520, 32, 56)

    if p1_chakra >= 30:
        chakra_image.clip_composite_draw(int(chakra_frame) * 32, 0, 32, 56, 0, '', 1080, 520, 32, 56)
    if p1_chakra >= 60:
        chakra_image.clip_composite_draw(int(chakra_frame) * 32, 0, 32, 56, 0, '', 1040, 520, 32, 56)
    if p1_chakra >= 90:
        chakra_image.clip_composite_draw(int(chakra_frame) * 32, 0, 32, 56, 0, '', 1000, 520, 32, 56)

    if p1_mug == 'naruto':
        naruto_mug.clip_composite_draw(0, 0, 104, 112, 0, '', 1150, 550, 80, 80)
    elif p1_mug == 'sasuke':
        sasuke_mug.clip_composite_draw(0, 0, 96, 104, 0, '', 1150, 550, 80, 80)
    elif p1_mug == 'itachi':
        itachi_mug.clip_composite_draw(0, 0, 112, 112, 0, '', 1150, 550, 80, 80)
    if p2_mug == 'naruto':
        naruto_mug.clip_composite_draw(0, 0, 104, 112, 0, '', 50, 550, 80, 80)
    elif p2_mug == 'sasuke':
        sasuke_mug.clip_composite_draw(0, 0, 96, 104, 0, '', 50, 550, 80, 80)
    elif p2_mug == 'itachi':
        itachi_mug.clip_composite_draw(0, 0, 112, 112, 0, '', 50, 550, 80, 80)

    if fight_frame <= 600:
        fight.clip_composite_draw(0, 0, 1601, 786, 0, '', 600, 900-int(fight_frame), 473, 228)
    elif 600 < fight_frame <= 900:
        fight.clip_composite_draw(0, 0, 1601, 786, 0, '', 600, 300, 473, 228)
    elif 900 < fight_frame <= 1500:
        fight.clip_composite_draw(0, 0, 1601, 786, 0, '', 600, int(fight_frame)-600, 473, 228)

    draw_text(p1_name, 1200 - len(p1_name) * 15, 480, 20)
    draw_text(p2_name, 10, 480, 20)
    # print(p1_name, p2_name)

    if p1.hp == 0 or p2.hp == 0:

        ko.clip_composite_draw(0, 0, 473, 228, 0, '', 600, 300, 473, 228)
    update_canvas()

def draw_text(text, x, y, size):
    # font = load_font("C:/Windows/Fonts/Arial.ttf", size)
    font = load_font("resource/Arial.ttf", size)
    font.draw(x, y, text, (0, 0, 0))  # 흰색 텍스트

def clean_name(name_bytes):
    """바이트 문자열에서 깨끗한 문자열 추출"""
    return name_bytes.decode('utf-8', errors='ignore').rstrip('\x00').strip()

def update():
    global chakra_frame, fight_frame, go_result, result_timer
    game_world.update()
    chakra_frame = (chakra_frame + 4 * game_framework.frame_time) % 4
    if fight_frame <= 1500:
        fight_frame += game_framework.frame_time * 800

    if go_result:
        result_timer += game_framework.frame_time
        if result_timer > 3:
            go_result = False
            game_framework.change_mode(multi_result)
    pass