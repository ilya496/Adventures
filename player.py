import pygame
from settings import PLAYER_STEP


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('resources/pictures/main_player.png').convert_alpha()
        self.rect = pygame.rect.Rect(100, 100, self.image.get_width(), self.image.get_height())
        self.hp = 100
        self.damage = 3

        self.flipped = 'right'

    def flip_image(self):
        self.image = pygame.transform.flip(self.image, True, False)

    # OPTIMIZE эта функция знает слишком много:
    #   назначение клавиш, правила перемещения игрока, правила подготовки картинки игрока
    def move_rect(self, obj: pygame.Rect, axis: str, amount: int):
        # Определяем по какой оси нужно двигать
        if axis == 'y':
            obj.y += amount
        elif axis == 'x':
            obj.x += amount
            # Проверяем если двигаем вправо
            if amount > 0:
                if self.flipped == 'left':
                    self.flip_image()
                    self.flipped = 'right'
            # Иначе двигаем влево
            else:
                if self.flipped == 'right':
                    self.flip_image()
                    self.flipped = 'left'

        # if key == pygame.K_w:
        #     obj.y -= PLAYER_STEP
        #
        # elif key == pygame.K_s:
        #     obj.y += PLAYER_STEP
        #
        # elif key == pygame.K_d:
        #     obj.x += PLAYER_STEP
        #     if self.flipped == 'left':
        #         self.flip_image()
        #         self.flipped = 'right'
        #
        # elif key == pygame.K_a:
        #     obj.x -= PLAYER_STEP
        #     if self.flipped == 'right':
        #         self.flip_image()
        #         self.flipped = 'left'

    def process_events(self, events):
        # FIXME с этим будут проблемы. Никто другой события обработать уже не сможет
        #   Чтобы понять, в чем проблема - попробуй сделать закрытие на крестик не меняя эту строку.
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.move_rect(self.rect, 'y', -PLAYER_STEP)
                elif event.key == pygame.K_a:
                    self.move_rect(self.rect, 'x', -PLAYER_STEP)
                elif event.key == pygame.K_s:
                    self.move_rect(self.rect, 'y', PLAYER_STEP)
                elif event.key == pygame.K_d:
                    self.move_rect(self.rect, 'x', PLAYER_STEP)
