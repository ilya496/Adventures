import pygame
from typing import Union


class Ground(pygame.sprite.Sprite):
    def __init__(self, size: list, pos: list):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(),
                                self.image.get_height())

    def change_bg_color(self, color: Union[str, list]):
        self.image.fill(pygame.Color(color))

    def collide_point(self, point):
        return self.rect.collidepoint(point)

    def move_player_x(self, start_pos, distance):
        raise Exception('Method must be overridden')

    def move_player_y(self, start_pos, distance):
        raise Exception('Method must be overridden')

    def max_move_player_x(self, start_pos, distance):
        if self.rect.right - start_pos[0] <= distance or self.rect.left - start_pos[0] >= distance:
            if distance >= 0:
                return [self.rect.right - 1, start_pos[1]]
            else:
                return [self.rect.left + 1, start_pos[1]]
        else:
            return self.move_player_x(start_pos, distance)

    def max_move_player_y(self, start_pos, distance):
        if self.rect.bottom - start_pos[1] <= distance or self.rect.top - start_pos[1] >= distance:
            if distance >= 0:
                return [start_pos[0], self.rect.bottom - 1]
            else:
                return [start_pos[0], self.rect.top + 1]
        else:
            return self.move_player_y(start_pos, distance)

    def access_to_enter(self):
        raise Exception('Method must be overridden')


class Water(Ground):
    def __init__(self, size: list, pos: list):
        Ground.__init__(self, size, pos)
        self.change_bg_color('blue')

    def move_player_x(self, start_pos, distance):
        return [start_pos[0], start_pos[1]]

    def move_player_y(self, start_pos, distance):
        return [start_pos[0], start_pos[1]]

    def access_to_enter(self):
        return False


class Land(Ground):
    def __init__(self, size: list, pos: list):
        Ground.__init__(self, size, pos)
        self.change_bg_color('green')

    def move_player_x(self, start_pos, distance):
        return [start_pos[0] + distance * 1.2, start_pos[1]]

    def move_player_y(self, start_pos, distance):
        return [start_pos[0], start_pos[1] + distance * 1.2]

    def access_to_enter(self):
        return True


class Sand(Ground):
    def __init__(self, size: list, pos: list):
        Ground.__init__(self, size, pos)
        self.change_bg_color('yellow')

    def move_player_x(self, start_pos, distance):
        return [start_pos[0] + distance * 0.8, start_pos[1]]

    def move_player_y(self, start_pos, distance):
        return [start_pos[0], start_pos[1] + distance * 0.8]

    def access_to_enter(self):
        return True
