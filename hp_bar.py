import pygame


class HpBar(pygame.sprite.Sprite):

    def __init__(self, max_hp):
        pygame.sprite.Sprite.__init__(self)

        self.max_hp = max_hp
        self.image = pygame.Surface([150, 50])
        self.rect = pygame.rect.Rect(100, 100, self.image.get_width(), self.image.get_height())
        self.set_hp(max_hp)

    def set_hp(self, new_hp):
        self._hp_scale(self.image, new_hp, self.max_hp)

    def _bar_parts(self, surface, number_of_parts):
        pass

    def _hp_scale(self, surface, current_hp, max_hp):
        pass


