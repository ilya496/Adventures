import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([50, 50])
        self.rect = pygame.rect.Rect(100, 100, self.image.get_width(), self.image.get_height())

        self.image.fill([0, 255, 255])



