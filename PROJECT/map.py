from pico2d import *
import play_mode
import mode_choose_mode
class Map:
    def __init__(self):
        # self.uchihamap = load_image('resource/uchihamap.png')
        self.madahashimap = load_image('resource/madahashimap.png')
        self.bridgemap = load_image('resource/Bridge.png')
        self.round3map = load_image('resource/round3.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        if mode_choose_mode.mode_choose_result() == '1p':
            if play_mode.round_num == 1:
                self.w = self.madahashimap.w
                self.h = self.madahashimap.h
            elif play_mode.round_num == 2:
                self.w = self.bridgemap.w
                self.h = self.bridgemap.h
            elif play_mode.round_num == 3:
                self.w = self.round3map.w
                self.h = self.round3map.h
        elif mode_choose_mode.mode_choose_result() == '2p':
            self.w = self.madahashimap.w
            self.h = self.madahashimap.h

    def update(self):
        if mode_choose_mode.mode_choose_result() == '1p':
            self.window_left = clamp(0, int(play_mode.p1.x) - self.cw // 2,
                                     self.w - self.cw - 1)
            self.window_bottom = clamp(0, int(play_mode.p1.y) - self.ch // 2,
                                       self.h - self.ch - 1)
        elif mode_choose_mode.mode_choose_result() == '2p':
            self.window_left = clamp(0, int((play_mode.p1.x+play_mode.p2.x)//2) - self.cw // 2,
                                     self.w - self.cw - 1)
            self.window_bottom = clamp(0, int((play_mode.p1.y + play_mode.p2.y) // 2) - self.ch // 2,
                                       self.h - self.ch - 1)

    def draw(self):
        if mode_choose_mode.mode_choose_result() == '1p':
            if play_mode.round_num == 1:
                self.madahashimap.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
            elif play_mode.round_num == 2:
                self.bridgemap.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
            elif play_mode.round_num == 3:
                self.round3map.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
        elif mode_choose_mode.mode_choose_result() == '2p':
            self.madahashimap.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)