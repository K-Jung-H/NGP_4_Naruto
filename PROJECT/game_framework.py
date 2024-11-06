# from game_world import objects
import struct
import time
import keyboard
from network_client import NetworkClient
import threading

running = None
stack = None

TEST = True

# 서버 설정
if TEST:
    SERVER_IP = '127.0.0.1'
else:
    SERVER_IP = '192.168.81.193'
SERVER_PORT = 9000

# 네트워크 클라이언트 초기화 및 연결
network_client = NetworkClient(SERVER_IP, SERVER_PORT)
network_client.connect()

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


                # 키 입력 감지 쓰레드 시작
client_IO_thread = threading.Thread(target=key_listener)
client_IO_thread.start()

def change_mode(mode):
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()

    # execute resume function of the previous mode
    if (len(stack) > 0):
        stack[-1].resume()


def quit():
    global running
    running = False
    network_client.disconnect()


def run(start_mode):
    global running, stack, frame_rate
    running = True
    stack = [start_mode]
    start_mode.init()

    global frame_time
    frame_time = 0.0
    current_time = time.time()
    while (running):
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        frame_time = time.time() - current_time
        frame_rate = 1.0 / frame_time
        current_time += frame_time
        # print(f'Frame Time: {frame_time}, Frame Rate: {frame_rate}')

        # try:
        #     # 키가 눌리면 해당 키 값을 서버로 전송
        #     event = keyboard.read_event()
        #     if event.event_type == keyboard.KEY_DOWN:
        #         key_data = event.name
        #         print(f"게임에서 감지한 키 입력: {key_data}")
        #
        #         # 네트워크로 키 입력 데이터를 전송
        #         network_client.send_key_data(key_data)
        #
        #         # esc 키가 눌리면 게임 종료
        #         if key_data == 'esc':
        #             break
        # except Exception as e:
        #     print(f"키보드 입력 오류 발생: {e}")

    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()

