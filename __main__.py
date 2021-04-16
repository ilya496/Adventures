import pygame

import game
import settings

pygame.init()
game = game.Game(settings.WIDTH, settings.HEIGHT)

while True:
    events = pygame.event.get()
    game.process_events(events)
    game.draw()
