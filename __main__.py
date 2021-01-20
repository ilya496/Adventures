import pygame
import player
import settings
import hp_bar

pygame.init()
screen = pygame.display.set_mode([settings.WIDTH, settings.HEIGHT])
clock = pygame.time.Clock()
pygame.key.set_repeat(50)

player = player.Player()
hp_bar = hp_bar.HpBar()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(hp_bar)


while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
    screen.fill([0, 50, 0])
    player.process_events(events)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)
