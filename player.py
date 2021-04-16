import pygame

from game_object import InteractiveObject, Ground
from settings import KEYS_INTERACTION, KEYS_LEFT, KEYS_UP, KEYS_DOWN, KEYS_RIGHT


class Player(pygame.sprite.Sprite):
    def __init__(self, player_step, player_max_hp, all_game_objects):
        """ Начальное объявление всех переменных """
        pygame.sprite.Sprite.__init__(self)

        self.step = player_step
        self.step_copy = player_step

        self.image_orig = pygame.image.load('resources/pictures/main_player.png').convert_alpha()
        self.rect = pygame.rect.Rect(0, 0, self.image_orig.get_width(), self.image_orig.get_height())
        self.x = self.rect.x
        self.y = self.rect.y
        self.interact_rect = pygame.rect.Rect(self.rect.x, self.rect.y, self.rect.w + 150, self.rect.h + 300)
        self.hp_callback = None
        self.max_hp = player_max_hp
        self.current_hp = self.max_hp
        self.damage = 5
        self.game_objects = all_game_objects
        self.central_point = self.get_central_point()

        self.flipped_x = 'right'
        self.image = self.get_image('right')

    def get_image(self, direction_to_flip):
        """ Функция, в которой получаем повернутую картинку от оригинала """
        copy_img = self.image_orig.copy()

        if direction_to_flip == 'right':
            copy_img = self.image_orig.copy()
        elif direction_to_flip == 'left':
            copy_img = pygame.transform.flip(self.image_orig, True, False)

        return copy_img

    def flip_image(self, direction_to_flip):
        """ Функция, которая поворачивает картинку если это требуется """
        if direction_to_flip == 'right' and self.flipped_x == 'left':
            self.image = self.get_image(direction_to_flip)
            self.flipped_x = 'right'
        elif direction_to_flip == 'left' and self.flipped_x == 'right':
            self.image = self.get_image(direction_to_flip)
            self.flipped_x = 'left'

    def flip_image_by_amount(self, amount):
        """ Функция, которая поворачивает картинку по числу """
        if amount >= 0:
            self.flip_image('right')
        elif amount < 0:
            self.flip_image('left')

    def set_hp_callback(self, callback):
        """ Функция, которая ставит callback-функцию для ХП бара """
        self.hp_callback = callback

    def get_central_point(self):
        """ Функция, которая возвращает центральную точку персонажа относительно себя """
        return [self.rect.w / 2, self.rect.h / 2 + 27]

    def get_central_point_pos(self):
        """ Функция, которая возвращает центральную точку персонажа относительно всего экрана """

        return [self.x + self.central_point[0], self.y + self.central_point[1]]

    def set_central_point(self, point):
        """ Функция, которая ставит центральную точку персонажа на определенную точку """
        self.x = point[0] - self.central_point[0]
        self.y = point[1] - self.central_point[1]
        self.rect.x = self.x
        self.rect.y = self.y

    def find_ground(self, point=None):
        """ Функция, которая находит землю по точке, если она есть, иначе по центральной точке """
        point_to_find = point if point is not None else self.get_central_point_pos()
        for i in self.game_objects.sprites()[::-1]:
            if isinstance(i, Ground):
                if i.collide_point(point_to_find) and not i.is_transparent():
                    return i

    def lock_moving(self):
        """ Функция, которая блокирует движение """
        self.step = 0

    def unlock_moving(self):
        """ Функция, которая разблокирует движение """
        self.step = self.step_copy

    def set_hp(self, hp):
        """ Функция, которая ставит определенное ХП персонажу """
        self.current_hp = hp
        if callable(self.hp_callback):
            self.hp_callback(hp)
        print(self.max_hp, self.current_hp)

    def interact_with_objects(self):
        """ Функция, которая взаимодейстувет с какими-либо объектами в игре """
        for i in self.game_objects.sprites()[::-1]:
            if issubclass(type(i), InteractiveObject) and i.collide_rect(self.rect):
                i.interaction()
                break

    def _set_max_move_player(self, next_ground, axis, amount):
        central_point_pos = self.get_central_point_pos()
        max_move_player = next_ground.max_move_player_x if axis else next_ground.max_move_player_y
        self.set_central_point(max_move_player(central_point_pos, amount))

    def _move_rect(self, amount: int, axis: bool):
        """" Функция, которая двигает персонажа по любой из осей """
        central_point_pos = self.get_central_point_pos()
        cur_ground = self.find_ground()

        move_player = cur_ground.move_player_x if axis else cur_ground.move_player_y

        res_point = move_player(central_point_pos, amount)
        next_ground = self.find_ground(res_point)
        if next_ground is None or next_ground == cur_ground or next_ground.access_to_enter():
            self.set_central_point(res_point)
        else:
            self._set_max_move_player(next_ground, axis, amount)

    def move_rect_x(self, amount: int):
        """ Движение по оси 'x' равно True """
        self._move_rect(amount, True)
        self.flip_image_by_amount(amount)

    def move_rect_y(self, amount: int):
        """ Движение по оси 'y' равно False """
        self._move_rect(amount, False)

    @staticmethod
    def _check_pressed_keys(keys):
        """ Проверяем нажатие клавиш """
        pressed = pygame.key.get_pressed()
        for i in keys:
            if pressed[i]:
                return True
        return False

    def process_events(self, events):
        """ Функция, которая обрабатывает все события персонажа """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in KEYS_INTERACTION:
                    self.interact_with_objects()

        if self._check_pressed_keys(KEYS_LEFT): self.move_rect_x(-self.step)
        if self._check_pressed_keys(KEYS_UP): self.move_rect_y(-self.step)
        if self._check_pressed_keys(KEYS_RIGHT): self.move_rect_x(self.step)
        if self._check_pressed_keys(KEYS_DOWN): self.move_rect_y(self.step)
