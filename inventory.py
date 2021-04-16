from pygame import Surface, sprite, Rect, font, image, transform


class Inventory(sprite.Sprite):
    inventory = None

    def __init__(self, num_of_cells: int):
        sprite.Sprite.__init__(self)
        self.image = Surface((250, 250))
        self.image.fill('#F4DEC4')

        self.rect = Rect(100, 10, self.image.get_width(), self.image.get_height())

        self.num_cells = num_of_cells
        self.max_number_of_item_in_cell = 100
        self.cell_size = 50

        self.arial_font = font.match_font('Arial')
        self.cell_name_font = font.Font(self.arial_font, 15)
        self.numbers_font = font.Font(self.arial_font, 25)
        self.header_font = font.Font(self.arial_font, 35)
        self.dict = {
            x: {
                'object': None,
                'count': 0
            } for x in range(self.num_cells)
        }
        self._generate_image()

    def _fill_cell(self, key, value, count):
        assert key in self.dict, 'Несуществующий ключ словаря инвентаря'
        assert type(self.dict[key]['object']) == type(value) or self.dict[key]['object'] is None

        if self.dict[key]['object'] is None:
            self.dict[key]['object'] = value

        max_count = self.dict[key]['count'] + count - self.max_number_of_item_in_cell
        if max_count <= 0:
            self.dict[key]['count'] += count
            return 0
        else:
            self.dict[key]['count'] = self.max_number_of_item_in_cell
            return max_count

    def add_to_free_space(self, value, count):

        for key, val in self.dict.items():
            if type(val['object']) is type(value) and val['count'] < self.max_number_of_item_in_cell:
                count = self._fill_cell(key, value, count)
                self._generate_image()
                if count == 0:
                    return
        for key, val in self.dict.items():
            if val['object'] is None:
                count = self._fill_cell(key, value, count)
                self._generate_image()
                if count == 0:
                    return

    @staticmethod
    def _shift_to_centering(rect1: Rect, rect2: Rect):
        """ Вычисляем расстояние от центра одного прямоугольника до центра другого прямоугольника """
        rect1_center_x = rect1.centerx
        rect2_center_x = rect2.centerx
        if rect1_center_x > rect2_center_x:
            return rect1_center_x - rect2_center_x
        else:
            return rect2_center_x - rect1_center_x

    def _generate_cells_rect(self, header_rect: Rect):
        """ Так как у нас инвентарь делится на заголовок и часть с клетками,
        то надо получить верхнюю часть инвентаря т.е. заголовок, чтобы мы могли правильно заполнить клетки """
        content_rect = Rect(0, header_rect.h,
                            self.image.get_width(), self.image.get_height() * 0.8)
        cells_rects = []
        for i in range(content_rect.w // self.cell_size):  # Идем по строкам
            for j in range(content_rect.h // self.cell_size):  # Идем по столмцам привет
                cells_rects.append(Rect(self.cell_size * i,
                                        self.cell_size * j + header_rect.h, self.cell_size - 1,
                                        self.cell_size - 1))
        return cells_rects

    def _generate_cell_image(self, cell: dict, cell_rect: Rect):
        """ Генерируем картинку клеточки по ее содержимому и прямоугольнику, в котором она должна находиться """
        val, count = cell['object'], str(cell['count'])
        img, pos, size = None, (cell_rect.x, cell_rect.y), (cell_rect.w, cell_rect.h)

        name = self.cell_name_font.render(str(val), True, [0, 0, 0])  # Навзвание предмета
        number = self.numbers_font.render(count, True, [0, 0, 0])  # Количество предмета

        # Достаем картинку из папки resources/pictures с названием класса и делаем ей размер прямоугольника
        if val is not None:
            img = transform.scale(image.load('resources/pictures/%s.png' % str(val).lower()), size)

        self.image.blit(img, pos) if img else self.image.blit(Surface(size), pos)  # Рисуем картинка которую мы достали
        self.image.blit(name, (name.get_rect().x + self._shift_to_centering(cell_rect, name.get_rect()),
                               pos[1]))  # Рисуем название объекта
        self.image.blit(number, (cell_rect.right - number.get_rect().w,
                                 cell_rect.bottom - number.get_rect().h + 5))  # Рисуем количество предмета

    def _generate_image(self):
        header = self.header_font.render('Inventory', True, [0, 0, 0])  # Создаем заголовок инвентаря
        header_rect = Rect(0, 0, header.get_width(),
                           self.image.get_height() * 0.2)  # Создаем прямоугольник для заголовка
        cells_rects = self._generate_cells_rect(header_rect)  # Создаем сетку прямоугольников

        for i in self.dict:  # Вызываем для каждой клетки создание картинки
            try:
                self._generate_cell_image(self.dict[i], cells_rects[i])
            except IndexError:  # Если в self.dict элементов больше чем в cells_rects кидаем ошибку
                except_string = 'Инвентарь не может вместить больше чем %d предметов' % i
                raise Exception(except_string)

        self.image.blit(header, (self._shift_to_centering(header_rect, self.image.get_rect()),
                                 header_rect.y))  # Рисуем заголовок

    @classmethod
    def get_inventory(cls, num_of_cells=None):
        if cls.inventory is None:
            cls.inventory = cls(num_of_cells)
        return cls.inventory
