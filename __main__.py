import pygame, player

pygame.init()
screen = pygame.display.set_mode([600, 400])

player = player.Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

while True:
    pygame.event.get()
    all_sprites.draw(screen)
    pygame.display.flip()

