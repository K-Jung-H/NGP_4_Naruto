from pico2d import *

import mode_choose_mode
import p1_lose
import p1_win
import result_mode
import title_mode
from map import Map
from sasuke import SASUKE
from naruto import NARUTO
from itachi import ITACHI
from round1_neji import NEJI
from round2_kabuto import KABUTO
from round3_sakura import SAKURA
import game_framework
import game_world
import charactor_choose_mode
import single_character_choice_mode
import round1, round2, round3
def handle_events():
    global running, round_num

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F1:
            p1.win = True
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F2:
            p1.hp = 0
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F3:
            p2.hp = 0
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F4:
            p1.chakra += 30
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F5:
            p2.chakra += 30
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if mode_choose_mode.mode_choose_result() == '1p' and p1.win:
                if round_num == 1:
                    round_num = 2
                    game_framework.change_mode(round2)
                elif round_num == 2:
                    round_num = 3
                    game_framework.change_mode(round3)
                elif round_num == 3:
                    round_num = 1
                    game_framework.change_mode(p1_win)
            elif mode_choose_mode.mode_choose_result() == '1p' and p1.hp <= 0:
                game_framework.change_mode(p1_lose)
            elif mode_choose_mode.mode_choose_result() == '2p' and (p1.win or p2.win):
                game_framework.change_mode(result_mode)
                pass
            # exit(1)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
        #     game_framework.
        else:
            p1.handle_event(event)
            p2.handle_event(event)


def init():
    global running
    global world
    global p1
    global p2
    global map
    global health_bar, health_hp, naruto_mug, sasuke_mug, itachi_mug, chakra_image, chakra_frame
    global ko, fight, fight_frame
    global round_num, neji_mug, kabuto_mug, sakura_mug, p_bgm

    health_bar = load_image('resource/health_bar.png')
    health_hp = load_image('resource/health_hp.png')
    naruto_mug = load_image('resource/naruto_mugshot.png')
    sasuke_mug = load_image('resource/sasuke_mugshot.png')
    itachi_mug = load_image('resource/itachi_mugshot.png')
    neji_mug = load_image('resource/neji_mugshot.png')
    kabuto_mug = load_image('resource/kabuto_mugshot.png')
    sakura_mug = load_image('resource/sakura_mugshot.png')
    chakra_image = load_image('resource/chakra.png')
    chakra_frame = 0
    ko = load_image('resource/ko.png')
    fight = load_image('resource/fight.png')
    fight_frame = 0

    # title_mode.bgm.stop()

    if mode_choose_mode.mode_choose_result() == '2p':
        p_bgm = load_music('sound/playsound.mp3')
        p_bgm.set_volume(8)
        p_bgm.repeat_play()

    # if mode_choose_mode.mode_choose_result() == '1p' and round_num == 3:
    #     p_bgm.stop()
    #     p_bgm = load_music('sound/round3.mp3')
    #     p_bgm.set_volume(12)
    #     p_bgm.repeat_play()


    running = True
    world = []

    map = Map()
    game_world.add_object(map, 1)

    if mode_choose_mode.mode_choose_result() == '1p':
        if single_character_choice_mode.p1_choose_result() == 1:
            p1 = NARUTO(1)
            game_world.add_object(p1, 1)
        elif single_character_choice_mode.p1_choose_result() == 2:
            p1 = SASUKE(1)
            game_world.add_object(p1, 1)
        elif single_character_choice_mode.p1_choose_result() == 3:
            p1 = ITACHI(1)
            game_world.add_object(p1, 1)

        if round_num == 1:
            p2 = NEJI(2)
            game_world.add_object(p2, 1)
        elif round_num == 2:
            p2 = KABUTO(2)
            game_world.add_object(p2, 1)
        elif round_num == 3:
            p2 = SAKURA(2)
            game_world.add_object(p2, 1)

    elif mode_choose_mode.mode_choose_result() == '2p':
        if charactor_choose_mode.p1_choose_result() == 1:
            p1 = NARUTO(1)
            game_world.add_object(p1, 1)
        elif charactor_choose_mode.p1_choose_result() == 2:
            p1 = SASUKE(1)
            game_world.add_object(p1, 1)
        elif charactor_choose_mode.p1_choose_result() == 3:
            p1 = ITACHI(1)
            game_world.add_object(p1, 1)

        if charactor_choose_mode.p2_choose_result() == 1:
            p2 = NARUTO(2)
            game_world.add_object(p2, 1)
        elif charactor_choose_mode.p2_choose_result() == 2:
            p2 = SASUKE(2)
            game_world.add_object(p2, 1)
        elif charactor_choose_mode.p2_choose_result() == 3:
            p2 = ITACHI(2)
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

def finish():
    game_world.remove_object(p1)
    game_world.remove_object(p2)
    game_world.remove_object(map)
    game_world.objects[2] = []
    game_world.collision_pairs = {}
    pass
def update():
    global chakra_frame, fight_frame
    game_world.update()
    game_world.handle_collisions()
    chakra_frame = (chakra_frame + 4 * game_framework.frame_time) % 4
    if fight_frame <= 1500:
        fight_frame += game_framework.frame_time * 800
    if p1.hp <= 0:
        p2.win = True
    if p2.hp <= 0:
        p1.win = True

def draw():
    clear_canvas()
    game_world.render()
    health_bar.clip_composite_draw(0, 0, 402, 22, 0, '', 300, 570, 402, 30)
    health_bar.clip_composite_draw(0, 0, 402, 22, 0, '', 900, 570, 402, 30)
    health_hp.clip_composite_draw(0, 0, 8, 9, 0, '', 300-(400-p2.hp)//2, 570, p2.hp, 28)
    health_hp.clip_composite_draw(0, 0, 8, 9, 0, '', 900-(400-p1.hp)//2, 570, p1.hp, 28)
    if p2.chakra >= 30:
        chakra_image.clip_composite_draw(int(chakra_frame)*32, 0, 32, 56, 0, '', 120, 520, 32, 56)
    if p2.chakra >= 60:
        chakra_image.clip_composite_draw(int(chakra_frame)*32, 0, 32, 56, 0, '', 160, 520, 32, 56)
    if p2.chakra >= 90:
        chakra_image.clip_composite_draw(int(chakra_frame)*32, 0, 32, 56, 0, '', 200, 520, 32, 56)

    if p1.chakra >= 30:
        chakra_image.clip_composite_draw(int(chakra_frame)*32, 0, 32, 56, 0, '', 1080, 520, 32, 56)
    if p1.chakra >= 60:
        chakra_image.clip_composite_draw(int(chakra_frame)*32, 0, 32, 56, 0, '', 1040, 520, 32, 56)
    if p1.chakra >= 90:
        chakra_image.clip_composite_draw(int(chakra_frame)*32, 0, 32, 56, 0, '', 1000, 520, 32, 56)

    if mode_choose_mode.mode_choose_result() == '1p':
        if single_character_choice_mode.p1_choose_result() == 1:
            naruto_mug.clip_composite_draw(0, 0, 104, 112, 0, '', 1150, 550, 80, 80)
        elif single_character_choice_mode.p1_choose_result() == 2:
            sasuke_mug.clip_composite_draw(0, 0, 96, 104, 0, '', 1150, 550, 80, 80)
        elif single_character_choice_mode.p1_choose_result() == 3:
            itachi_mug.clip_composite_draw(0, 0, 112, 112, 0, '', 1150, 550, 80, 80)

        if round_num == 1:
            neji_mug.clip_composite_draw(0, 0, neji_mug.w, neji_mug.h, 0, '', 50, 550, 80, 80)
        elif round_num == 2:
            kabuto_mug.clip_composite_draw(0, 0, kabuto_mug.w, kabuto_mug.h, 0, '', 50, 550, 80, 80)
        elif round_num == 3:
            sakura_mug.clip_composite_draw(0, 0, sakura_mug.w, sakura_mug.h, 0, '', 50, 550, 80, 80)
        pass
    elif mode_choose_mode.mode_choose_result() == '2p':
        if charactor_choose_mode.p1_choose_result() == 1:
            naruto_mug.clip_composite_draw(0, 0, 104, 112, 0, '', 1150, 550, 80, 80)
        elif charactor_choose_mode.p1_choose_result() == 2:
            sasuke_mug.clip_composite_draw(0, 0, 96, 104, 0, '', 1150, 550, 80, 80)
        elif charactor_choose_mode.p1_choose_result() == 3:
            itachi_mug.clip_composite_draw(0, 0, 112, 112, 0, '', 1150, 550, 80, 80)

        if charactor_choose_mode.p2_choose_result() == 1:
            naruto_mug.clip_composite_draw(0, 0, 104, 112, 0, '', 50, 550, 80, 80)
        elif charactor_choose_mode.p2_choose_result() == 2:
            sasuke_mug.clip_composite_draw(0, 0, 96, 104, 0, '', 50, 550, 80, 80)
        elif charactor_choose_mode.p2_choose_result() == 3:
            itachi_mug.clip_composite_draw(0, 0, 112, 112, 0, '', 50, 550, 80, 80)

    if fight_frame <= 600:
        fight.clip_composite_draw(0, 0, 1601, 786, 0, '', 600, 900-int(fight_frame), 473, 228)
    elif 600 < fight_frame <= 900:
        fight.clip_composite_draw(0, 0, 1601, 786, 0, '', 600, 300, 473, 228)
    elif 900 < fight_frame <= 1500:
        fight.clip_composite_draw(0, 0, 1601, 786, 0, '', 600, int(fight_frame)-600, 473, 228)

    if p1.win or p2.win:
        ko.clip_composite_draw(0, 0, 473, 228, 0, '', 600, 300, 473, 228)
    update_canvas()

