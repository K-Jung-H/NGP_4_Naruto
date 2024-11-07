from pico2d import *

import charactor_choose_mode
import game_framework
import play_mode
import single_character_choice_mode
import mode_choose_mode
import keyboard
from network_client import NetworkClient
import threading
import struct

TEST = True
LOCAL = True

# 서버 설정
if TEST:
    if LOCAL:
        SERVER_IP = '127.0.0.1'
    else:
        SERVER_IP = '192.168.81.193'
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
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key_data = event.name

            # 키가 처음 눌린 경우에만 서버로 전송
            if key_data not in pressed_keys:
                print(f"감지된 키 다운 입력: {key_data}")
                if not TEST:
                    # 서버로 키 다운 정보 전송
                    send_key_info(key_data, KEY_DOWN)
                # 눌린 키로 등록
                pressed_keys.add(key_data)

        elif event.event_type == keyboard.KEY_UP:
            key_data = event.name

            # 키가 처음 떼어진 경우에만 서버로 전송
            if key_data in pressed_keys:
                print(f"감지된 키 업 입력: {key_data}")
                if not TEST:
                    # 서버로 키 업 정보 전송
                    send_key_info(key_data, KEY_UP)  # 키 업 전송
                # 눌린 키에서 제거
                pressed_keys.remove(key_data)
#
# if __name__ == "__main__":
#
def init():
    global network_client
    if TEST:
        # 네트워크 클라이언트 초기화 및 연결
        network_client = NetworkClient(SERVER_IP, SERVER_PORT)
        network_client.connect()

    if TEST:
        # 키 입력 감지 쓰레드 시작
        client_IO_thread = threading.Thread(target=key_listener)
        client_IO_thread.start()

    pass
def finish():
    if TEST:
        network_client.disconnect()
    pass
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

def running():
    pass
def draw():
    clear_canvas()
    update_canvas()

def update():
    pass