import pygame
import json, os
from pygame_gui import UIManager, elements, UI_BUTTON_PRESSED
from player import Player
from hp_bar import HpBar
from camera import GroupWithCamera
from settings import PLAYER_STEP
from ground import Water, Land, Sand


class Game():
    def __init__(self, surface_x, surface_y):
        # Создание экрана и менеджера
        self.screen = pygame.display.set_mode((surface_x, surface_y))
        self.manager = UIManager((surface_x, surface_y))
        self.background = pygame.Surface((surface_x, surface_y))
        self.background.fill(pygame.Color('#30475e'))

        # Создание кнопок и окон текста
        self.text_box_html_text = 'Hello text, Hello text,Hello text,Hello textHello textHello text'
        self.quest_text_box = self.add_text_box([0, 0], [100, 100], self.text_box_html_text)
        self.quest_text_box.hide()
        self.quest_button = self.add_button([0, 0], [30, 30], '?', callback=self.show_quest)
        self.close_button = self.add_button([70, 0], [30, 30], 'X', callback=self.hide_quest)
        self.close_button.hide()
        self.clock = pygame.time.Clock()
        self.quest_file = os.path.abspath('quests.json')
        self.inventory = {}

        # Создание спрайтов
        self.bar_hp = HpBar([20, 350], [150, 25], 500)
        self.water = Water([600, 200], [0, 0])
        self.land = Land([2000, 2000], [0, 200])
        self.sand = Sand([200, 600], [-200, 0])
        self.ground_sprites = pygame.sprite.Group()
        self.ground_sprites.add(self.sand)
        self.ground_sprites.add(self.water)
        self.ground_sprites.add(self.land)

        # Создание группы и добавление в группу спрайтов
        self.main_player = Player(PLAYER_STEP, self.ground_sprites)
        self.camera_sprites = GroupWithCamera(self.main_player.rect, surface_x, surface_y)
        self.common_sprites = pygame.sprite.Group()
        self.common_sprites.add(self.bar_hp)
        self.camera_sprites.add(self.land)
        self.camera_sprites.add(self.sand)
        self.camera_sprites.add(self.water)
        self.camera_sprites.add(self.main_player)

    def add_text_box(self, position: list, size: list, text: str):
        text_box_rect = pygame.Rect((position[0], position[1]), (size[0], size[1]))
        text_box = elements.UITextBox(html_text=text, relative_rect=text_box_rect, manager=self.manager,
                                      wrap_to_height=True)
        return text_box

    def add_button(self, position: list, size: list, text: str, callback):
        button_rect = pygame.Rect((position[0], position[1]), (size[0], size[1]))
        button = elements.UIButton(relative_rect=button_rect, text=text, manager=self.manager,
                                   starting_height=10)
        button.callback = callback
        return button

    def show_quest(self):
        self.quest_text_box.show()
        self.close_button.show()
        self.quest_button.hide()

    def hide_quest(self):
        self.quest_text_box.hide()
        self.close_button.hide()
        self.quest_button.show()

    def set_text_box_html_text(self, html_text: str):
        self.text_box_html_text = html_text

    def read_quest(self):
        try:
            file = open(self.quest_file, 'r')
            return json.load(file)
        except:
            return False

    def process_events(self, pg_events):
        time_delta = self.clock.tick(60) / 1000.0
        events = pg_events
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == UI_BUTTON_PRESSED:
                    event.ui_element.callback()
                    if event.ui_element == self.quest_button:
                        self.main_player.lock_moving()
                    elif event.ui_element == self.close_button:
                        self.main_player.unlock_moving()

            self.manager.process_events(event)

        self.manager.update(time_delta)

        self.main_player.process_events(events)
        self.bar_hp.set_hp(300)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.manager.draw_ui(self.screen)
        self.camera_sprites.draw(self.screen)
        self.common_sprites.draw(self.screen)
        pygame.display.update()
