from pico2d import *

import charactor_choose_mode
import game_framework
import game_world
import play_mode
import single_character_choice_mode
import mode_choose_mode
import keyboard

import title_mode
from network_client import NetworkClient
import threading
import struct
from map import Map
from sasuke import SASUKE
from naruto import NARUTO

TEST = False
LOCAL = False

Input_thread_running = True

# 서버 설정
if TEST:
    if LOCAL:
        SERVER_IP = '127.0.0.1'
    else:
        SERVER_IP = '192.168.81.47'
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
    'w': 87
    # 필요한 키들을 추가로 정의
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

# struct 포맷: 'ff?iii' -> float 2개, bool 1개, int 3개
player_info_format = 'ff?iii'
data_size = struct.calcsize(player_info_format)

def receive_player_info(client_socket):
    # 서버에서 Player_Info 구조체 크기만큼 데이터 수신
    data = client_socket.recv(data_size)
    if len(data) != data_size:
        print("수신된 데이터 크기가 올바르지 않습니다.")
        return None

    # 데이터 언패킹
    x, y, direction, state, character, sprite_index = struct.unpack(player_info_format, data)

    # 언패킹된 데이터를 딕셔너리 형태로 반환
    return {
        "position": {"x": x, "y": y},
        "direction": direction,
        "state": state,
        "character": character,
        "sprite_index": sprite_index
    }

def data_receiver(client_socket):
    while True:
        player_info = receive_player_info(client_socket)
        if player_info:
            print(player_info)

def init():
    global network_client
    global p1
    global p2
    global map
    if TEST:
        # 네트워크 클라이언트 초기화 및 연결
        network_client = NetworkClient(SERVER_IP, SERVER_PORT)
        network_client.connect()
        receiver_thread = threading.Thread(target=data_receiver, args=(network_client.client_socket))
        receiver_thread.start()

    # 키 입력 감지 쓰레드 시작
    client_Input_thread = threading.Thread(target=key_listener)
    client_Input_thread.start()

    map = Map()
    game_world.add_object(map, 1)

    p1 = SASUKE(1)
    game_world.add_object(p1, 1)

    p2 = NARUTO(2)
    game_world.add_object(p2, 1)

    p1.set_background(map)
    p2.set_background(map)

    p1.x = 1200
    p1.dir = -1
    p2.x = 400
    p1.y, p2.y = 400, 400
    p1.frame, p2.frame = 2, 2

    game_world.add_collision_pair('p1:p2_attack', p1, None)
    game_world.add_collision_pair('p1:p2_shuriken', p1, None)
    game_world.add_collision_pair('p1:p2_skill1', p1, None)
    game_world.add_collision_pair('p1:p2_skill2', p1, None)

    game_world.add_collision_pair('p2:p1_attack', p2, None)
    game_world.add_collision_pair('p2:p1_shuriken', p2, None)
    game_world.add_collision_pair('p2:p1_skill1', p2, None)
    game_world.add_collision_pair('p2:p1_skill2', p2, None)

    pass
def finish():
    global Input_thread_running
    if TEST:
        network_client.disconnect()
    game_world.remove_object(p1)
    game_world.remove_object(p2)
    game_world.remove_object(map)
    game_world.objects[2] = []
    game_world.collision_pairs = {}
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

def running():
    pass
def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def update():
    game_world.update()
    game_world.handle_collisions()
    pass