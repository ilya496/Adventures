from typing import Union, Tuple

import pygame
import pygame_gui
from player import Player


class Game:
    def __init__(self, surface_x: int, surface_y: int):
        self.screen: pygame.Surface = ...
        self.manager: pygame_gui.UIManager = ...
        self.background: pygame.Surface = ...

        self.max_hp_player: int = ...
        self.default_layer: int = ...
        self.inventory_cells: int = ...
        self.clock: pygame.time.Clock = ...
        self.inventory: pygame.sprite.Sprite = ...

        # Создание спрайтов и земли
        self.bar_hp: pygame.sprite.Sprite = ...
        self.ground_sprites: pygame.sprite.LayeredUpdates = ...

        # Создание группы и добавление в группу спрайтов
        self.camera_sprites: pygame.sprite.LayeredUpdates = ...
        self.main_player: Player = ...

        self.common_sprites: pygame.sprite.LayeredUpdates = ...

        # Создание кнопок и окон текста
        self.text_box_html_text: str = ...
        self.quest_text_box: pygame_gui.elements.UITextBox = ...

        self.quest_button: pygame_gui.elements.UIButton = ...
        self.close_button: pygame_gui.elements.UIButton = ...
        self.inventory_close_button: pygame_gui.elements.UIButton = ...

    def generate_map(self): ...

    def add_default_ground(self, size: Union[list, Tuple[int, int]],
                           pos: Union[list, Tuple[int, int]]): ...

    def add_water(self, size: Union[list, Tuple[int, int]],
                  pos: Union[list, Tuple[int, int]]): ...

    def add_land(self, size: Union[list, Tuple[int, int]],
                 pos: Union[list, Tuple[int, int]]): ...

    def add_sand(self, size: Union[list, Tuple[int, int]],
                 pos: Union[list, Tuple[int, int]]): ...

    def add_stone(self, size: Union[list, Tuple[int, int]],
                  pos: Union[list, Tuple[int, int]]): ...

    def add_boat(self, size: Union[list, Tuple[int, int]],
                 pos: Union[list, Tuple[int, int]]): ...

    def add_text_box(self, position: list, size: list, text: str): ...

    def add_button(self, position: list, size: list, text: str, callback: callable): ...

    def show_inventory(self): ...

    def hide_inventory(self): ...

    def show_quest(self): ...

    def hide_quest(self): ...

    def set_text_box_html_text(self, html_text: str): ...

    def process_events(self, pg_events: iter): ...

    def draw(self): ...
