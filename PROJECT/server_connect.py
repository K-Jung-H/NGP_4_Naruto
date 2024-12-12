from pico2d import *
import game_framework
import play_mode
import mode_choose_mode
import multi_char_select_mode
import title_mode
import multi_room_select_mode
from network_client import NetworkClient

character_count = 3

# server_ip = "127.0.0.1"  # 사용자가 입력할 서버 IP
# server_ip = "192.168.81.15"  # 사용자가 입력할 서버 IP
server_ip = "1.242.69.251"  # 사용자가 입력할 서버 IP
input_active = True  # 입력 중인지 여부

SERVER_PORT = 9000

def init():
    global image1, naruto, sasuke, itachi
    global p1_x, p1_y, p2_x, p2_y, p1_choose, p2_choose, p1_image, p2_image, character_back
    global vs, press_space
    global naruto_frame, sasuke_frame, itachi_frame, space_frame, space_up
    global duplicate, dup_on, dup_wait_time, dir_image, mode_choose
    global naruto_back, sasuke_back, itachi_back, naruto_logo, sasuke_logo, itachi_logo, server_ip
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
    server_ip = server_ip
    #server_ip = ""


def finish():
    global image1, naruto, sasuke, itachi, p1_image, p2_image, character_back, vs, press_space, duplicate, dir_image
    del image1, naruto, sasuke, itachi, p1_image, p2_image, character_back, vs, press_space, duplicate, dir_image
def handle_events():
    events = get_events()
    global p1_choose, p2_choose, character_count, dup_on, dup_wait_time
    global server_ip, input_active
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            print("서버 커넥트 소켓 유무 테스트 : ", game_framework.get_socket())
            network_client = NetworkClient(server_ip, SERVER_PORT)
            game_framework.set_socket(network_client)
            game_framework.network_client.connect()
            if not network_client.is_connected:
                print("서버 안열림 or ip 잘못 치심")
                mode_choose_mode.connect_fail_flag = True
                game_framework.change_mode(mode_choose_mode)
                break
            game_framework.change_mode(multi_room_select_mode)
            pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F1:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_BACKSPACE:
            if len(server_ip) > 0:  # 문자열이 비어있지 않을 때만 삭제
                server_ip = server_ip[:-1]
        elif event.type == SDL_KEYDOWN:
            # event.key가 None인지 확인
            if event.key is None:
                continue
            if is_valid_ip_key(event.key):  # 유효한 키 입력만 추가
                server_ip += key_to_char(event.key)

def is_valid_ip_key(key):
    """숫자 및 점에 해당하는 키인지 확인."""
    return (SDLK_0 <= key <= SDLK_9) or (key == SDLK_PERIOD)


def key_to_char(key):
    """키를 문자로 변환."""
    if SDLK_0 <= key <= SDLK_9:
        return chr(key)  # 숫자 키
    elif key == SDLK_PERIOD:
        return '.'
    return ''

def running():
    pass
def draw():
    clear_canvas()
    image1.clip_composite_draw(0, 0, 900, 507, 0, '', 600, 300, 1200, 600)

    draw_text(f"Server IP: {server_ip}", 200, 300, 50)

    if space_up:
        press_space.clip_composite_draw(0, 0, press_space.w, press_space.h, 0, '', 600, 60 + space_frame,
                                        press_space.w * 0.15, press_space.h * 0.15)
    else:
        press_space.clip_composite_draw(0, 0, press_space.w, press_space.h, 0, '', 600, 70 - space_frame,
                                        press_space.w * 0.15, press_space.h * 0.15)

    if dup_on:
        duplicate.clip_composite_draw(0, 0, 5906, 4135, 0, '', 600, 300, 600, 300)
    update_canvas()

def draw_text(text, x, y, size):
    font = load_font("resource/Arial.ttf", size)
    font.draw(x, y, text, (0, 0, 0))  # 흰색 텍스트

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