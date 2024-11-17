from pico2d import *

import multi_mode

class SkillObject:
    # 클래스 변수로 스프라이트 공유
    skill_sprites = {}

    def __init__(self):
        self.active = False  # 활성화 여부
        self.skill_type = None
        self.x, self.y = 0, 0
        self.dir = 1
        self.sprite_index = 0
        self.sx, self.sy = 0, 0

    @classmethod
    def load_sprites(cls):
        """스킬 타입별 스프라이트를 미리 로드"""
        cls.skill_sprites[1] = load_image('resource/shuriken3.png')
        cls.skill_sprites[2] = load_image('resource/naruto_skill1_effect.png')
        cls.skill_sprites[3] = load_image('resource/naruto_skill2_effect.png')
        # 필요한 스킬 타입 추가

    def activate(self, skill_type, x, y, dir, sprite_index):
        """스킬 객체를 활성화하고 속성을 업데이트"""
        self.active = True
        self.skill_type = skill_type
        self.x, self.y = x, y
        self.dir = dir
        self.sprite_index = sprite_index

    def deactivate(self):
        """스킬 객체를 비활성화"""
        self.active = False

    def draw(self):
        self.sx, self.sy = self.x - multi_mode.map.window_left, self.y - multi_mode.map.window_bottom
        if self.active and self.skill_type in self.skill_sprites:
            sprite = self.skill_sprites[self.skill_type]
            if self.skill_type == 1:
                sprite.clip_composite_draw(
                    int(self.sprite_index) * 46, 0, 46, 35, 0, '', self.sx, self.sy, 46 * 2, 35 * 2)
            elif self.skill_type == 2:
                sprite.clip_composite_draw(
                    int(self.sprite_index) * 193, 0, 193, 136, 0, '', self.sx, self.sy + 20, 543, 382)
            elif self.skill_type == 3:
                sprite.clip_composite_draw(
                    (int(self.sprite_index) - 7) * 159, 0, 159, 88, 0, '', self.sx, self.sy, 447, 247)