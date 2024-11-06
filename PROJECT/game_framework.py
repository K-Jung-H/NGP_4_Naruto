# from game_world import objects
import time
import keyboard
from network_client import NetworkClient
import threading

running = None
stack = None

# 서버 설정
# SERVER_IP = '192.168.80.227'
SERVER_IP = '127.0.0.1'
SERVER_PORT = 9000

# 네트워크 클라이언트 초기화 및 연결
network_client = NetworkClient(SERVER_IP, SERVER_PORT)
network_client.connect()


# 키 입력을 감지하고 서버로 전송하는 함수
def key_listener():
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key_data = event.name
            print(f"감지된 키 입력: {key_data}")
            # 키 입력 데이터를 서버로 전송
            network_client.client_socket.sendall(key_data.encode('utf-8'))

            if key_data == 'esc':  # esc 키가 눌리면 종료
                break

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

