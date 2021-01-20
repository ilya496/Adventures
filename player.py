import pygame
from settings import PLAYER_STEP


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('resources/pictures/main_player.png').convert_alpha()
        self.rect = pygame.rect.Rect(100, 100, self.image.get_width(), self.image.get_height())
        self.hp = 100
        self.damage = 5

        self.flipped = 'right'

    def flip_image(self, direction_to_flip):
        if direction_to_flip == 'right' and self.flipped == 'left':
            self.image = pygame.transform.flip(self.image, True, False)
            self.flipped = 'right'
        elif direction_to_flip == 'left' and self.flipped == 'right':
            self.image = pygame.transform.flip(self.image, True, False)
            self.flipped = 'left'

    def move_rect_x(self, obj: pygame.Rect, amount: int):
        obj.x += amount
        # Проверяем если двигаем вправо
        if amount > 0:
            self.flip_image('right')
        # Иначе двигаем влево
        else:
            self.flip_image('left')

    def move_rect_y(self, obj: pygame.Rect, amount: int):
        obj.y += amount

    def process_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.move_rect_y(self.rect, -PLAYER_STEP)
                elif event.key == pygame.K_a:
                    self.move_rect_x(self.rect, -PLAYER_STEP)
                elif event.key == pygame.K_s:
                    self.move_rect_y(self.rect, PLAYER_STEP)
                elif event.key == pygame.K_d:
                    self.move_rect_x(self.rect, PLAYER_STEP)
