from typing import Union, Tuple

import pygame

from inventory import Inventory


class GameObject(pygame.sprite.Sprite):
    def __init__(self, size: Union[list, Tuple[int, int]],
                 pos: Union[list, Tuple[int, int]]):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())
        self.layer = 1
        self.multiplier = 1
        self.access = True

    @classmethod
    def __repr__(cls):
        return cls.__name__

    def change_bg_color(self, color: Union[str, list]):
        self.image.fill(pygame.Color(color))

    def change_image(self, image):
        self.image = image

    def collide_point(self, point):
        return self.rect.collidepoint(point)

    def collide_rect(self, rect):
        return self.rect.colliderect(rect)

    def access_to_enter(self):
        return self.access


class Ground(GameObject):
    def __init__(self, size: Union[list, Tuple[int, int]],
                 pos: Union[list, Tuple[int, int]]):
        GameObject.__init__(self, size=size, pos=pos)
        self.image = pygame.Surface(size)
        self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())
        self.layer = 1
        self.multiplier = 1
        self._is_transparent = False

    def move_player_x(self, start_pos, distance):
        return [start_pos[0] + distance * self.multiplier, start_pos[1]]

    def _move_to_border_x(self, start_pos, distance):
        if distance > 0:
            return [self.rect.left - 1, start_pos[1]]
        elif distance < 0:
            return [self.rect.right + 1, start_pos[1]]
        else:
            return start_pos

    def max_move_player_x(self, start_pos, distance):
        return self._move_to_border_x(start_pos, distance * self.multiplier)

    def move_player_y(self, start_pos, distance):
        return [start_pos[0], start_pos[1] + distance * self.multiplier]

    def _move_to_border_y(self, start_pos, distance):
        if distance > 0:
            return [start_pos[0], self.rect.top - 1]
        elif distance < 0:
            return [start_pos[0], self.rect.bottom + 1]
        else:
            return start_pos

    def max_move_player_y(self, start_pos, distance):
        return self._move_to_border_y(start_pos, distance * self.multiplier)

    def is_transparent(self):
        return self._is_transparent


class InteractiveObject(GameObject):
    def __init__(self, size: Union[list, Tuple[int, int]],
                 pos: Union[list, Tuple[int, int]]):
        GameObject.__init__(self, size=size, pos=pos)
        self.inventory = Inventory.get_inventory()
        self.image = pygame.Surface(size)
        self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())
        self.layer = 1

    def interaction(self):
        raise Exception('Method must be overridden')


class Stone(Ground, InteractiveObject):
    def __init__(self, size: Union[list, Tuple[int, int]],
                 pos: Union[list, Tuple[int, int]]):
        InteractiveObject.__init__(self, size, pos)
        self.change_bg_color('grey')
        self.layer = 10
        self.access = False
        self._is_transparent = False

    def interaction(self):
        if self._is_transparent:
            return
        self._is_transparent = True
        self.inventory.add_to_free_space(self, 60)
        print(self.inventory.dict)


class Boat(GameObject):
    def __init__(self, size: Union[list, Tuple[int, int]],
                 pos: Union[list, Tuple[int, int]]):
        GameObject.__init__(self, size, pos)


class DefaultGround(Ground):
    def __init__(self, size: Union[list, Tuple[int, int]],
                 pos: Union[list, Tuple[int, int]]):
        Ground.__init__(self, size, pos)
        self.layer = 0
        self.multiplier = 1
        self.change_bg_color('#30475e')


class Water(Ground, InteractiveObject):
    def __init__(self, size: Union[list, Tuple[int, int]],
                 pos: Union[list, Tuple[int, int]]):
        Ground.__init__(self, size, pos)
        InteractiveObject.__init__(self, size, pos)
        self.change_bg_color('blue')
        self.multiplier = 2
        self.layer = 2

    def inventory_access(self):
        for key in self.inventory.dict:
            if isinstance(self.inventory.dict[key]['object'], Boat):
                print("It works !!")
                return True
        return False

    def interaction(self) -> None:
        pass

    def access_to_enter(self):
        return self.inventory_access()


class Land(Ground):
    def __init__(self, size: Union[list, Tuple[int, int]],
                 pos: Union[list, Tuple[int, int]]):
        Ground.__init__(self, size, pos)
        self.change_bg_color('green')
        self.multiplier = 2


class Sand(Ground):
    def __init__(self, size: Union[list, Tuple[int, int]],
                 pos: Union[list, Tuple[int, int]]):
        Ground.__init__(self, size, pos)
        self.change_bg_color('yellow')
        self.multiplier = 0.8
