# from game_world import objects
import time
import threading
import struct
import keyboard

pressed_keys = set()
Input_thread_running = False
client_Input_thread = None
receiver_thread = None
data_handler = None  # 데이터를 처리할 콜백 함수
stop_event = threading.Event()

running = None
stack = None
network_client = None  # 전역 소켓 객체 선언

KEY_DOWN = 1
KEY_UP = 2

key_codes = {
    'a': 65, 'd': 68, 's': 83, 'w': 87,
    'left': 65, 'right': 68, 'down': 83, 'up': 87,
    'l': 76, ';': 59, ',': 44, '/': 47, '.': 46,
    'f': 76, 'g': 59, 'c': 44, 'v': 46, 'b': 47
}

# 데이터 포맷 정의
position_format = "2f"
player_info_format = "32s2f?3i?"
attack_info_format = "2f?2i"
etc_info_format = "5i"
game_data_format = f"{player_info_format * 2}{attack_info_format * 18}{etc_info_format}"
data_size = struct.calcsize(game_data_format)

def send_key_info(key_name, key_action):
    """키 정보를 패킹하여 서버로 전송"""
    key_code = key_codes.get(key_name, 0)  # key_name을 key_code로 변환
    if network_client.client_socket:
        data = struct.pack('ii', key_code, key_action)
        network_client.client_socket.sendall(data)

def key_listener():
    """키 입력을 감지하고 서버로 전송"""
    global Input_thread_running
    while Input_thread_running:
        try:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                key_data = event.name
                if key_data not in pressed_keys:
                    send_key_info(key_data, KEY_DOWN)
                    pressed_keys.add(key_data)

            elif event.event_type == keyboard.KEY_UP:
                key_data = event.name
                if key_data in pressed_keys:
                    send_key_info(key_data, KEY_UP)
                    pressed_keys.remove(key_data)
        except Exception as e:
            print(f"Error in key listener: {e}")

def start_key_listener():
    """키 입력 스레드 시작"""
    global Input_thread_running, client_Input_thread
    if client_Input_thread is None or not client_Input_thread.is_alive():
        Input_thread_running = True
        client_Input_thread = threading.Thread(target=key_listener)
        client_Input_thread.daemon = True
        client_Input_thread.start()
        print("Key listener thread started.")

def stop_key_listener():
    """키 입력 스레드 종료"""
    global Input_thread_running, client_Input_thread
    Input_thread_running = False
    if client_Input_thread and client_Input_thread.is_alive():
        client_Input_thread.join()
        print("Key listener thread stopped.")

def set_data_handler(handler):
    global data_handler
    data_handler = handler

def receive_game_data(client_socket):
    """서버로부터 고정된 크기의 게임 데이터를 수신."""
    data = b""
    while len(data) < data_size:
        packet = client_socket.recv(data_size - len(data))
        if not packet:
            print("연결이 종료되었습니다.")
            return None
        data += packet

    # 데이터 언패킹
    unpacked_data = struct.unpack(game_data_format, data)
    return unpacked_data

def receive_game_data_loop():
    """서버로부터 데이터를 계속 수신하고 핸들러에 전달."""
    try:
        while not stop_event.is_set():
            unpacked_data = receive_game_data(network_client.client_socket)
            if unpacked_data is None:  # 연결 종료
                break
            if data_handler:
                data_handler(unpacked_data)  # 언패킹된 데이터 전달
    except Exception as e:
        print(f"Error in receive thread: {e}")
    finally:
        network_client.client_socket.close()
        print("Receiver thread terminated.")
        pass

def start_receiver_thread():
    global receiver_thread
    receiver_thread = threading.Thread(target=receive_game_data_loop)
    receiver_thread.daemon = True
    receiver_thread.start()

def stop_receiver_thread():
    global receiver_thread
    stop_event.set()
    if receiver_thread:
        receiver_thread.join()

def reset_stop_event():
    """stop_event 초기화."""
    global stop_event
    stop_event.clear()

def set_socket(client_socket):
    global network_client
    network_client = client_socket

def get_socket():
    global network_client
    return network_client

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

    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()

