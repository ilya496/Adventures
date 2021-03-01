import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, player_step, ground_sprites):
        pygame.sprite.Sprite.__init__(self)

        self.step = player_step
        self.step_copy = player_step

        self.image_orig = pygame.image.load('resources/pictures/main_player.png').convert_alpha()
        self.rect = pygame.rect.Rect(500, 500, self.image_orig.get_width(), self.image_orig.get_height())
        # self.hp = 100
        # self.damage = 5
        self.ground_sprites = ground_sprites
        self.central_point = self.get_central_point()

        self.flipped_x = 'right'
        self.flipped_y = False
        self.image = self.get_image('right')

    def flip_image(self, direction_to_flip):
        if direction_to_flip == 'right' and self.flipped_x == 'left':
            self.image = self.get_image(direction_to_flip)
            self.flipped_x = 'right'
        elif direction_to_flip == 'left' and self.flipped_x == 'right':
            self.image = self.get_image(direction_to_flip)
            self.flipped_x = 'left'

    def get_image(self, direction):
        copy_img = self.image_orig.copy()

        if direction == 'right':
            copy_img = self.image_orig.copy()
        elif direction == 'left':
            copy_img = pygame.transform.flip(self.image_orig, True, False)

        pygame.draw.circle(copy_img, '#ff0000', self.central_point, 3)

        return copy_img

    def get_central_point(self):
        return [self.rect.w / 2, self.rect.h / 2 + 27]

    def get_central_point_pos(self):
        return [self.rect.x + self.central_point[0], self.rect.y + self.central_point[1]]

    def set_central_point(self, point):
        self.rect.x = point[0] - self.central_point[0]
        self.rect.y = point[1] - self.central_point[1]

    def find_cur_ground(self, point=None):
        for i in self.ground_sprites:
            if point is None:
                if i.collide_point(self.get_central_point_pos()):
                    return i
            elif i.collide_point(point):
                return i

    def move_rect_x(self, amount: int):
        central_point_pos = self.get_central_point_pos()
        cur_ground = self.find_cur_ground()

        if cur_ground is not None:  # Если мы стоим на какой-либо земле
            res_point = cur_ground.move_player_x(central_point_pos, amount)  # Ищем точку куда хотим переместиться
            next_ground = self.find_cur_ground(res_point)  # Ищем следующую землю
            # Проверяем если нет следующей земли или мы идем по той же самой
            if next_ground is None or next_ground == cur_ground:
                self.set_central_point(res_point)  # то просто идем
            # Иначе если нас впускают
            elif next_ground.access_to_enter():
                self.set_central_point(res_point)  # то просто идем
            # Если на не впускают
            else:
                res_point = cur_ground.max_move_player_x(central_point_pos, amount)
                self.set_central_point(res_point)  # Ставим на макс. возможную точку в пределах границ

        else:  # Если мы не стоим на какой-либо земле
            # То повторяем пред. алгоритм, только без эффектов передвижения(замедления, ускорения ..)
            next_ground = self.find_cur_ground([central_point_pos[0] + amount, central_point_pos[1]])
            if next_ground is None:
                self.rect.x += amount
            elif next_ground.access_to_enter():
                self.rect.x += amount

        if amount >= 0:
            self.flip_image('right')
        else:
            self.flip_image('left')

    def move_rect_y(self, amount: int):
        central_point_pos = self.get_central_point_pos()
        cur_ground = self.find_cur_ground()

        if cur_ground is not None:
            res_point = cur_ground.move_player_y(central_point_pos, amount)
            next_ground = self.find_cur_ground(res_point)
            if next_ground is None or next_ground == cur_ground:
                self.set_central_point(res_point)
            elif next_ground.access_to_enter():
                self.set_central_point(res_point)
            else:
                res_point = cur_ground.max_move_player_y(central_point_pos, amount)
                self.set_central_point(res_point)
        else:
            next_ground = self.find_cur_ground([central_point_pos[0], central_point_pos[1] + amount])
            if next_ground is None:
                self.rect.y += amount
            elif next_ground.access_to_enter():
                self.rect.y += amount

    def lock_moving(self):
        self.step = 0

    def unlock_moving(self):
        self.step = self.step_copy

    def process_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.move_rect_y(-self.step)
                elif event.key == pygame.K_a:
                    self.move_rect_x(-self.step)
                elif event.key == pygame.K_s:
                    self.move_rect_y(self.step)
                elif event.key == pygame.K_d:
                    self.move_rect_x(self.step)
