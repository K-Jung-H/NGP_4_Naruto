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
        cls.skill_sprites[1] = [load_image('resource/shuriken3.png')]  # 나루토 수리검
        cls.skill_sprites[2] = [load_image('resource/naruto_skill1_effect.png')]  # 나루토 꼬리 공격
        cls.skill_sprites[3] = [load_image('resource/naruto_skill2_effect.png')]  # 나루토 나선환
        cls.skill_sprites[4] = [load_image('resource/shuriken1.png')]  # 사스케, 이타치 수리검
        cls.skill_sprites[5] = [load_image('resource/sasuke_skill1_effect.png')]  # 사스케, 이타치 화둔
        cls.skill_sprites[6] = [  # 사스케 치도리, 2개의 이미지 사용
            load_image('resource/sasuke_skill2_effect1.png'),
            load_image('resource/sasuke_skill2_effect2.png')
        ]
        cls.skill_sprites[7] = [  # 이타치 아마테라스, 2개의 이미지 사용
            load_image('resource/itachi_skill2_effect1.png'),
            load_image('resource/itachi_skill2_effect2.png')
        ]

    def activate(self, skill_type, x, y, dir, sprite_index):
        """스킬 객체를 활성화하고 속성을 업데이트"""
        self.active = True
        self.skill_type = skill_type
        self.x, self.y = x, y
        self.dir = dir
        self.sprite_index = sprite_index

    def deactivate(self):
        self.active = False

    def draw(self):
        self.sx, self.sy = self.x - multi_mode.map.window_left, self.y - multi_mode.map.window_bottom
        if self.active and self.skill_type in self.skill_sprites:
            sprite_list = self.skill_sprites[self.skill_type]  # 스킬 타입에 해당하는 이미지 리스트 가져오기

            if self.skill_type == 1:  # 나루토 수리검
                sprite_list[0].clip_composite_draw(
                    int(self.sprite_index) * 46, 0, 46, 35, 0, '', self.sx, self.sy, 46 * 2, 35 * 2)
            elif self.skill_type == 2:  # 나루토 꼬리 공격
                if self.dir == 1:
                    sprite_list[0].clip_composite_draw(
                        int(self.sprite_index) * 193, 0, 193, 136, 0, '', self.sx, self.sy + 20, 543, 382)
                elif self.dir == -1:
                    sprite_list[0].clip_composite_draw(
                        int(self.sprite_index) * 193, 0, 193, 136, 0, 'h', self.sx, self.sy + 20, 543, 382)
            elif self.skill_type == 3:  # 나루토 나선환
                if self.sprite_index >= 7:
                    if self.dir == 1:
                        sprite_list[0].clip_composite_draw(
                            (int(self.sprite_index) - 7) * 159, 0, 159, 88, 0, '', self.sx, self.sy, 447, 247)
                    elif self.dir == -1:
                        sprite_list[0].clip_composite_draw(
                            (int(self.sprite_index) - 7) * 159, 0, 159, 88, 0, 'h', self.sx, self.sy, 447, 247)
            elif self.skill_type == 4:  # 사스케, 이타치 수리검
                sprite_list[0].clip_composite_draw(int(self.sprite_index) * 44, 0, 44, 35, 0, '', self.sx,
                                                   self.sy, 44 * 1.5, 35 * 1.5)
            elif self.skill_type == 5:  # 사스케, 이타치 화둔
                if self.dir == 1:
                    sprite_list[0].clip_composite_draw(int(self.sprite_index) * 97, 0, 97, 80, 0, '',
                                                           self.sx, self.sy + 90, 325, 241)
                elif self.dir == -1:
                    sprite_list[0].clip_composite_draw(int(self.sprite_index) * 97, 0, 97, 80, 0, 'h',
                                                           self.sx, self.sy + 90, 325, 241)
            elif self.skill_type == 6:  # 사스케 치도리
                # 첫 번째 효과 (skill2_effect2)
                if self.sprite_index <= 7:
                    sprite_list[1].clip_composite_draw(
                        int(self.sprite_index) * 104, 0, 104, 77, 0, '',
                        self.sx, self.sy + 41, 325, 241
                    )

                # 두 번째 효과 (skill2_effect1)
                if self.sprite_index >= 1:
                    if self.dir == -1:  # 왼쪽 방향
                        if self.sprite_index > 7:
                            sprite_list[0].clip_composite_draw(
                                (int(self.sprite_index) - 1) * 104, 0, 104, 77, 0, 'h',
                                self.sx + 30, self.sy - 10, 325, 241
                            )
                        else:
                            sprite_list[0].clip_composite_draw(
                                (int(self.sprite_index) - 1) * 104, 0, 104, 77, 0, 'h',
                                self.sx + 30, self.sy + 41 - 10, 325, 241
                            )
                    elif self.dir == 1:  # 오른쪽 방향
                        if self.sprite_index > 7:
                            sprite_list[0].clip_composite_draw(
                                (int(self.sprite_index) - 1) * 104, 0, 104, 77, 0, '',
                                self.sx - 30, self.sy - 10, 325, 241
                            )
                        else:
                            sprite_list[0].clip_composite_draw(
                                (int(self.sprite_index) - 1) * 104, 0, 104, 77, 0, '',
                                self.sx - 30, self.sy + 41 - 10, 325, 241
                            )
            elif self.skill_type == 7:  # 이타치 아마테라스
                # reach 함수 어쩔건지 이야기하기
                pass