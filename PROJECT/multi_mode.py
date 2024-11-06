from pico2d import *

import charactor_choose_mode
import game_framework
import play_mode
import single_character_choice_mode
import mode_choose_mode

def init():
    pass
def finish():
    pass
def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            # game_framework.change_mode(charactor_choose_mode)
            # game_framework.change_mode(single_character_choice_mode)
            game_framework.change_mode(mode_choose_mode)

def running():
    pass
def draw():
    clear_canvas()
    pass
    update_canvas()

def update():
    pass