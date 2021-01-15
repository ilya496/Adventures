import pygame
from settings import PLAYER_STEP


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('resources/pictures/main_player.png').convert_alpha()
        self.rect = pygame.rect.Rect(100, 100, self.image.get_width(), self.image.get_height())
        self.flipped_right = True
        self.flipped_left = False


    def move(self, key):

        if key == pygame.K_w:
            self.rect.y -= PLAYER_STEP

        elif key == pygame.K_s:
            self.rect.y += PLAYER_STEP

        elif key == pygame.K_d:
            self.rect.x += PLAYER_STEP
            if self.flipped_left:
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipped_right = True
                self.flipped_left = False

        elif key == pygame.K_a:
            self.rect.x -= PLAYER_STEP
            if self.flipped_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipped_right = False
                self.flipped_left = True


    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.move(event.key)
