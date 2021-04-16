import pygame
from pygame_gui import UIManager, elements, UI_BUTTON_PRESSED

from camera import GroupWithCamera
from game_object import Water, Land, Sand, Boat, Stone, DefaultGround
from hp_bar import HpBar
from inventory import Inventory
from player import Player
from settings import PLAYER_STEP


class Game:
    def __init__(self, surface_x, surface_y):
        # Создание экрана и менеджера
        self.screen = pygame.display.set_mode((surface_x, surface_y))
        self.manager = UIManager((surface_x, surface_y))
        self.background = pygame.Surface((surface_x, surface_y))
        self.background.fill(pygame.Color('#30475e'))

        # Прочее
        self.max_hp_player = 500
        self.default_layer = 1
        self.inventory_cells = 20
        self.clock = pygame.time.Clock()
        self.inventory = Inventory.get_inventory(self.inventory_cells)

        # Создание спрайтов и земли
        self.bar_hp = HpBar([20, 350], [150, 25], self.max_hp_player)
        self.ground_sprites = pygame.sprite.LayeredUpdates()

        # Создание группы и добавление в группу спрайтов
        self.generate_map()
        self.camera_sprites = GroupWithCamera(None, surface_x, surface_y)
        self.main_player = Player(PLAYER_STEP, self.max_hp_player, self.camera_sprites)
        self.main_player.set_hp_callback(self.bar_hp.set_hp)
        self.camera_sprites.change_focus_rect(self.main_player.rect)
        self.camera_sprites.add(self.main_player, layer=self.ground_sprites.get_top_layer() + 1)
        self.camera_sprites.add(self.ground_sprites.sprites())

        self.common_sprites = pygame.sprite.LayeredUpdates(default_layer=self.default_layer)
        self.common_sprites.add(self.bar_hp)
        self.common_sprites.add(self.inventory)

        # Создание кнопок и окон текста
        self.text_box_html_text = 'Hello text, Hello text, Hello text, Hello text, Hello text, Hello text'
        self.quest_text_box = self.add_text_box([0, 0], [100, 100], self.text_box_html_text)
        self.quest_text_box.hide()

        self.quest_button = self.add_button([0, 0], [30, 30], '?', callback=self.show_quest)
        self.close_button = self.add_button([70, 0], [30, 30], 'X', callback=self.hide_quest)
        self.inventory_close_button = self.add_button([self.inventory.rect.right - 28, self.inventory.rect.y - 2],
                                                      [30, 30], 'x', callback=self.hide_inventory)
        self.close_button.hide()
        self.hide_inventory()

    def generate_map(self):
        self.default_ground = self.add_default_ground((10000, 10000), (-5000, -5000))
        self.water = self.add_water([600, 200], [400, 600])
        self.land = self.add_land([1000, 1000], [0, 200])
        self.sand = self.add_sand([200, 600], [-100, 0])
        self.boat = self.add_boat([0, 0], [50, 50])
        self.stone = self.add_stone([100, 100], [-50, 200])
        self.stone2 = self.add_stone([100, 100], [250, 200])

    def add_default_ground(self, size, pos):
        default_ground = DefaultGround(size, pos)
        self.ground_sprites.add(default_ground)
        return default_ground

    def add_water(self, size, pos):
        water = Water(size, pos)
        self.ground_sprites.add(water)
        return water

    def add_land(self, size, pos):
        land = Land(size, pos)
        self.ground_sprites.add(land)
        return land

    def add_sand(self, size, pos):
        sand = Sand(size, pos)
        self.ground_sprites.add(sand)
        return sand

    def add_stone(self, size, pos):
        stone = Stone(size, pos)
        self.ground_sprites.add(stone)
        return stone

    def add_boat(self, size, pos):
        boat = Boat(size, pos)
        self.ground_sprites.add(boat)
        return boat

    def add_text_box(self, position, size, text):
        text_box_rect = pygame.Rect((position[0], position[1]), (size[0], size[1]))
        text_box = elements.UITextBox(html_text=text, relative_rect=text_box_rect, manager=self.manager,
                                      wrap_to_height=True)
        return text_box

    def add_button(self, position, size, text, callback):
        button_rect = pygame.Rect((position[0], position[1]), (size[0], size[1]))
        button = elements.UIButton(relative_rect=button_rect, text=text, manager=self.manager,
                                   starting_height=10)
        button.callback = callback
        return button

    def show_inventory(self):
        self.common_sprites.add(self.inventory)
        self.inventory_close_button.show()

    def hide_inventory(self):
        self.inventory.kill()
        self.inventory_close_button.hide()

    def show_quest(self):
        self.quest_text_box.show()
        self.close_button.show()
        self.quest_button.hide()

    def hide_quest(self):
        self.quest_text_box.hide()
        self.close_button.hide()
        self.quest_button.show()

    def set_text_box_html_text(self, html_text):
        self.text_box_html_text = html_text

    def process_events(self, pg_events):
        time_delta = self.clock.tick(60) / 1000.0
        events = pg_events
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e: #OPTIMIZE можно его и скрывать на повторное нажатие этой же клавиши
                    self.show_inventory()
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

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.camera_sprites.draw(self.screen)
        self.common_sprites.draw(self.screen)
        self.manager.draw_ui(self.screen)
        pygame.display.update()
