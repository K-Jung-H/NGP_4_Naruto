from pico2d import *

import charactor_choose_mode
import game_framework
import game_world
import single_character_choice_mode
import mode_choose_mode
import keyboard

import title_mode

from network_client import NetworkClient
import threading
import struct
from map import Map
from multi_player_render import (SASUKE_MULTI, NARUTO_MULTI, ITACHI_MULTI, Idle, Run, Jump, Attack,
                                 Skill_motion, Easy_hit, Hard_hit, Win, Lose)
from multi_skill_render import SkillObject

TEST = True
LOCAL = False

Input_thread_running = True

# 서버 설정
if TEST:
    if LOCAL:
        SERVER_IP = '127.0.0.1'
    else:
        SERVER_IP = '192.168.81.90'
else:
    SERVER_IP = "0"

SERVER_PORT = 9000

pressed_keys = set()
# 키 동작 정의
KEY_DOWN = 1
KEY_UP = 2

# key_name에 해당하는 키 코드 매핑 예시
key_codes = {
    'a': 65,
    'd': 68,
    's': 83,
    'w': 87,
    'left': 65,
    'right': 68,
    'down': 83,
    'up': 87,
    ',': 44,
    'l': 76,
    ':': 58,
    ';': 59,
    '/': 47
}

def send_key_info(key_name, key_action):
    """키 정보를 패킹하여 서버로 전송"""
    key_code = key_codes.get(key_name, 0)  # key_name을 key_code로 변환
    data = struct.pack('ii', key_code, key_action)
    network_client.client_socket.sendall(data)


# 키 입력을 감지하고 서버로 전송하는 함수
def key_listener():
    global Input_thread_running
    while Input_thread_running:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key_data = event.name

            # 키가 처음 눌린 경우에만 서버로 전송
            if key_data not in pressed_keys:
                print(f"감지된 키 다운 입력: {key_data}")
                if TEST:
                    # 서버로 키 다운 정보 전송
                    send_key_info(key_data, KEY_DOWN)
                # 눌린 키로 등록
                pressed_keys.add(key_data)

        elif event.event_type == keyboard.KEY_UP:
            key_data = event.name

            # 키가 처음 떼어진 경우에만 서버로 전송
            if key_data in pressed_keys:
                print(f"감지된 키 업 입력: {key_data}")
                if TEST:
                    # 서버로 키 업 정보 전송
                    send_key_info(key_data, KEY_UP)  # 키 업 전송
                # 눌린 키에서 제거
                pressed_keys.remove(key_data)

# 각 구조체의 포맷 정의
position_format = "2f"  # Position 구조체
player_info_format = "32s2f?3i"  # Player_Info 구조체
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

def receive_game_data(client_socket):
    global p1_chakra, p2_chakra, p1_hp, p2_hp, game_time
    data = b""
    while len(data) < data_size:
        packet = client_socket.recv(data_size - len(data))
        if not packet:
            print("연결이 종료되었습니다.")
            return None
        data += packet
    # 데이터 언패킹
    unpacked_data = struct.unpack(game_data_format, data)
    # print("Unpacked data:", unpacked_data)  # 디버깅용

    # 플레이어 1 업데이트
    p1.x = unpacked_data[1]
    p1.y = unpacked_data[2]
    p1.dir = unpacked_data[3]
    p1_state = unpacked_data[4]
    p1.cur_state = state_mapping.get(p1_state, Idle)  # 기본값은 Idle로 설정
    p1.frame = unpacked_data[6]

    # extra_state_data에 여러개의 값이 있는 경우를 위한 for?
    if p1_state in extra_state_data:
        for key, value in extra_state_data[p1_state].items():
            setattr(p1, key, value)

    # 플레이어 2 업데이트
    p2.x = unpacked_data[8]
    p2.y = unpacked_data[9]
    p2.dir = unpacked_data[10]
    p2_state = unpacked_data[11]
    p2.cur_state = state_mapping.get(p2_state, Idle)
    p2.frame = unpacked_data[13]

    if p2_state in extra_state_data:
        for key, value in extra_state_data[p2_state].items():
            setattr(p2, key, value)

    # 공격 업데이트
    for i, attack in enumerate(unpacked_data[14:14 + 18 * 5:5]):
        if attack[3] > 0:  # 유효한 스킬 데이터만 활성화
            skills[i].activate(
                skill_type=attack[3],
                x=attack[0],
                y=attack[1],
                dir=attack[2],
                sprite_index=attack[4]
            )
        else:
            skills[i].deactivate()

    p1_hp = unpacked_data[-5]
    p1_chakra = unpacked_data[-4]
    p2_hp = unpacked_data[-3]
    p2_chakra = unpacked_data[-2]
    game_time = unpacked_data[-1]

    # # 데이터 매핑
    # game_data = {
    #     "players": [
    #         {
    #             # player_ID를 ASCII로 디코딩, 예외 발생 시 기본값으로 대체
    #             # 플레이어 ID는 왜 필요하지? 서버에서 1p 2p 설정되있는거 아닌가?
    #             "player_ID": unpacked_data[0].decode('ascii', errors='ignore').strip("\x00"),
    #             "position": {"x": unpacked_data[1], "y": unpacked_data[2]},
    #             "X_Direction": unpacked_data[3],
    #             "player_state": unpacked_data[4],
    #             "selected_character": unpacked_data[5],
    #             "sprite_index": unpacked_data[6]
    #         },
    #         {
    #             "player_ID": unpacked_data[7].decode('ascii', errors='ignore').strip("\x00"),
    #             "position": {"x": unpacked_data[8], "y": unpacked_data[9]},
    #             "X_Direction": unpacked_data[10],
    #             "player_state": unpacked_data[11],
    #             "selected_character": unpacked_data[12],
    #             "sprite_index": unpacked_data[13]
    #         }
    #     ],
    #     "attacks": [
    #         {
    #             "position": {"x": unpacked_data[i], "y": unpacked_data[i + 1]},
    #             "X_Direction": unpacked_data[i + 2],
    #             # "selected_character": unpacked_data[i + 3],
    #             "attack_type": unpacked_data[i + 3],
    #             "sprite_index": unpacked_data[i + 4]
    #         }
    #         for i in range(14, 14 + 18 * 5, 5)
    #         # for i in range(14, 14 + 18 * 6, 6)
    #     ],
    #     "etc": {
    #         "player1_hp": unpacked_data[-5],
    #         "player1_sp": unpacked_data[-4],
    #         "player2_hp": unpacked_data[-3],
    #         "player2_sp": unpacked_data[-2],
    #         "game_time": unpacked_data[-1]
    #     }
    # }
    # return game_data

def receive_game_data_loop(client_socket):
    """서버로부터 데이터를 계속 수신하고 게임 객체를 업데이트."""
    while True:
        try:
            receive_game_data(client_socket)
        except Exception as e:
            print(f"데이터 수신 중 오류 발생: {e}")
            break

# def Decoding(client_socket):
#     global game_data
#     global p1, p2
#     while True:
#         game_data = receive_game_data(client_socket)
#         if game_data:
#             # print(game_data)
#             p1.x = game_data["players"][0]["position"]["x"]
#             p1.y = game_data["players"][0]["position"]["y"]
#             p1_state = game_data["players"][0]["player_state"]
#             if p1_state == STATE_IDLE:
#                 p1.cur_state = Idle
#             elif p1_state == STATE_RUN:
#                 p1.cur_state = Run
#             elif p1_state == STATE_JUMP:
#                 p1.cur_state = Jump
#             elif p1_state == STATE_ATTACK_NORMAL_1:
#                 p1.cur_state = Attack
#                 p1.attack_num = 1
#             elif p1_state == STATE_ATTACK_NORMAL_2:
#                 p1.cur_state = Attack
#                 p1.attack_num = 2
#             elif p1_state == STATE_ATTACK_NORMAL_3:
#                 p1.cur_state = Attack
#                 p1.attack_num = 3
#             elif p1_state == STATE_ATTACK_NORMAL_4:
#                 p1.cur_state = Attack
#                 p1.attack_num = 4
#             elif p1_state == STATE_ATTACK_SKILL_1:
#                 p1.cur_state = Skill_motion
#                 p1.skill_num = 'shuriken'
#             elif p1_state == STATE_ATTACK_SKILL_2:
#                 p1.cur_state = Skill_motion
#                 p1.skill_num = 'skill2'
#             elif p1_state == STATE_ATTACK_SKILL_3:
#                 p1.cur_state = Skill_motion
#                 p1.skill_num = 'skill1'
#             elif p1_state == STATE_HIT_EASY:
#                 p1.cur_state = Easy_hit
#             elif p1_state == STATE_HIT_HARD:
#                 p1.cur_state = Hard_hit
#             elif p1_state == STATE_WIN:
#                 p1.cur_state = Win
#             elif p1_state == STATE_LOSE:
#                 p1.cur_state = Lose
#
#             p1.frame = game_data["players"][0]["sprite_index"]
#             # print("Player 1 Dir:", game_data["players"][0]["X_Direction"])
#             p1.dir = game_data["players"][0]["X_Direction"]
#
#             # print("Player 2 Name:", game_data["players"][1]["player_ID"])
#             # print("Player 2 Position:", game_data["players"][1]["position"])
#             # p2.x = game_data["players"][1]["position"]["x"]
#             # p2.y = game_data["players"][1]["position"]["y"]
#             # p2_state = game_data["players"][1]["player_state"]
#             # if p2_state == STATE_IDLE:
#             #     p2.cur_state = Idle
#             # elif p2_state == STATE_RUN:
#             #     p2.cur_state = Run
#             # elif p2_state == STATE_JUMP:
#             #     p2.cur_state = Jump
#             # p2.frame = game_data["players"][1]["sprite_index"]
#             # if game_data["players"][1]["X_Direction"]:
#             #     p2.dir = 1
#             # else:
#             #     p2.dir = -1
#             # print(game_data["attacks"])
#             for i, attack in enumerate(game_data["attacks"]):
#                 # print(attack["attack_type"])
#                 if attack["attack_type"] > 0:  # 유효한 스킬 데이터만 활성화
#                     # print(attack)
#                     skills[i].activate(
#                         skill_type=attack["attack_type"],
#                         x=attack["position"]["x"],
#                         y=attack["position"]["y"],
#                         dir=attack["X_Direction"],
#                         sprite_index=attack["sprite_index"]
#                     )
#                     # print(i, skills[i].skill_type, skills[i].x, skills[i].y, skills[i].dir, skills[i].sprite_index)
#                 else:
#                     skills[i].deactivate()
#         else:
#             print("데이터 없음")

def init():
    global network_client
    global p1
    global p2
    global map
    global game_data
    global skills
    global health_bar, health_hp, naruto_mug, sasuke_mug, itachi_mug, chakra_image, chakra_frame
    global ko, fight, fight_frame, p1_chakra, p2_chakra, p1_hp, p2_hp, p1_mug, p2_mug

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

    map = Map()
    game_world.add_object(map, 1)

    if TEST:
        # p1 = SASUKE_MULTI(1)
        p1 = NARUTO_MULTI(1)
        # p1 = ITACHI_MULTI(1)
        game_world.add_object(p1, 1)

        p2 = NARUTO_MULTI(2)
        # p1 = ITACHI_MULTI(1)
        game_world.add_object(p2, 1)

        p1_mug = p1.char_name
        p2_mug = p2.char_name

        SkillObject.load_sprites()  # 스프라이트 이미지를 한 번만 로드
        skills = [SkillObject() for _ in range(18)]  # 18개의 Skill 객체 생성
        for skill in skills:
            game_world.add_object(skill, 2)
            skill.set_background(map)

        # 네트워크 클라이언트 초기화 및 연결
        network_client = NetworkClient(SERVER_IP, SERVER_PORT)
        network_client.connect()
        receiver_thread = threading.Thread(target=receive_game_data_loop, args=(network_client.client_socket,))
        receiver_thread.daemon = True  # 메인 프로그램 종료 시 함께 종료되도록 설정
        receiver_thread.start()
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
    else:
        # p1 = NARUTO_MULTI(1)
        # p1 = SASUKE_MULTI(1)
        p1 = ITACHI_MULTI(1)
        game_world.add_object(p1, 1)
        # p2 = NARUTO_MULTI(2)
        p2 = SASUKE_MULTI(2)
        game_world.add_object(p2, 1)

        p1.x = 1200
        p1.dir = -1
        p2.x = 400
        p1.y, p2.y = 400, 400
        p1.frame, p2.frame = 2, 2

        p1.set_background(map)
        p2.set_background(map)



    # 키 입력 감지 쓰레드 시작
    client_Input_thread = threading.Thread(target=key_listener)
    client_Input_thread.start()

    pass
def finish():
    global Input_thread_running
    if TEST:
        network_client.disconnect()
    game_world.remove_object(p1)
    game_world.remove_object(p2)
    game_world.remove_object(map)
    game_world.objects[2] = []
    Input_thread_running = False

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
    global skills
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

    update_canvas()

def update():
    game_world.update()
    pass