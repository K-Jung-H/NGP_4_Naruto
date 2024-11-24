import pico2d

import game_framework

import title_mode as start_mode

# pico2d.open_canvas(1200, 600, sync=True)
pico2d.open_canvas(1200, 600)
game_framework.run(start_mode)
pico2d.close_canvas()