import pygame


class HpBar(pygame.sprite.Sprite):

    def __init__(self, pos: list, size: list, max_hp: int):
        pygame.sprite.Sprite.__init__(self)

        self.max_hp = max_hp
        self.image = pygame.Surface([size[0], size[1]])
        self.rect = pygame.rect.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())
        self.set_hp(max_hp)

    def set_hp(self, new_hp: int):
        self.image.fill([0, 0, 0])
        self._hp_scale(new_hp, self.max_hp)
        self._bar_parts(3)

    def _bar_parts(self, number_of_parts):
        percent = (1 / (number_of_parts + 1))
        height = self.rect.height
        width = self.rect.width
        for i in range(number_of_parts):
            pygame.draw.line(self.image, '#e8e8e8', [width * percent * (i + 1), 0],
                             [width * percent * (i + 1), height])

    def _hp_scale(self, current_hp, max_hp):
        percent = current_hp / max_hp
        new_rect = pygame.rect.Rect(0, 0, self.rect.w * percent, self.rect.h)
        pygame.draw.rect(self.image, '#f05454', new_rect)
        pygame.draw.rect(self.image, '#222831', new_rect, 1)

    def check_point(self, position):
        if isinstance(position, pygame.Rect):
            return self.rect.colliderect(position)
        return self.rect.collidepoint(position)

    def get_rect(self):
        return pygame.Rect(self.rect)

